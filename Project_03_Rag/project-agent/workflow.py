import os
import json
from typing import List, Optional
from llama_index.core.workflow import Event, Workflow, step, StartEvent, StopEvent
from llama_index.core.schema import NodeWithScore, TextNode
from llama_index.core import Settings

# --- הגדרת אירועים (Events) ---
class InputAcceptedEvent(Event):
    query: str

class StructuredSearchEvent(Event):
    query: str
    category: str 
    keywords: List[str]

class SemanticSearchEvent(Event):
    query: str

class RetrievalCompleteEvent(Event):
    nodes: List[NodeWithScore]
    query: str

class ValidationPassedEvent(Event):
    nodes: List[NodeWithScore]
    query: str


# --- מחלקת ה-Workflow המלאה ---
class ProjectRAGWorkflow(Workflow):
    def __init__(self, retriever, synthesizer, timeout=60):
        super().__init__(timeout=timeout)
        self.retriever = retriever
        self.synthesizer = synthesizer
        self.json_path = "extracted_data.json"

    @step
    async def validate_input(self, ev: StartEvent) -> InputAcceptedEvent | StopEvent:
        """שלב 1: בדיקת תקינות הקלט"""
        user_query = ev.get("query")
        if not user_query or len(user_query.strip()) < 2:
            return StopEvent(result="❌ השאלה קצרה מדי.")
        return InputAcceptedEvent(query=user_query)

    @step
    async def route_query(self, ev: InputAcceptedEvent) -> StructuredSearchEvent | SemanticSearchEvent:
        """שלב 2: נתב חכם עם מנגנון הגנה לשאלות 'מדוע/איך'"""
        print(f"--- [Step 2: Intelligent Routing] ---")
        
        # פרומפט משופר שמסביר ל-LLM מתי לבחור סמנטי
        prompt = (
            f"Analyze the user query: '{ev.query}'\n"
            f"1. Determine category: 'decisions', 'rules', 'warnings', or 'semantic'.\n"
            f"2. IMPORTANT: If the user asks 'WHY', 'HOW', or for an EXPLANATION, ALWAYS choose 'semantic'.\n"
            f"3. Extract 2-3 core keywords for filtering (in English).\n"
            f"Respond in JSON format: {{\"category\": \"...\", \"keywords\": [\"...\", \"...\"]}}"
        )
        
        response = await Settings.llm.acomplete(prompt)
        try:
            # ניקוי פורמט למקרה שהמודל מחזיר Markdown
            clean_res = response.text.replace("```json", "").replace("```", "").strip()
            res_data = json.loads(clean_res)
            category = res_data.get("category", "semantic").lower()
            keywords = res_data.get("keywords", [])
        except:
            category = "semantic"
            keywords = []

        # מנגנון הגנה ידני (Hardcoded) - אם השאלה בעברית/אנגלית כוללת מילות הסבר
        semantic_triggers = ["מדוע", "איך", "למה", "why", "how", "explain", "תסביר", "סיכום"]
        if any(word in ev.query.lower() for word in semantic_triggers):
            category = "semantic"

        if category in ['decisions', 'rules', 'warnings']:
            print(f"Routing to STRUCTURED search. Category: {category}, Keywords: {keywords}")
            return StructuredSearchEvent(query=ev.query, category=category, keywords=keywords)
        else:
            print("Routing to SEMANTIC search (Pinecone)")
            return SemanticSearchEvent(query=ev.query)

    @step
    async def structured_retrieval(self, ev: StructuredSearchEvent) -> RetrievalCompleteEvent:
        """שלב 3א: שליפה מה-JSON עם סינון חכם"""
        print(f"--- [Step 3a: Filtered Retrieval from JSON] ---")
        
        if not os.path.exists(self.json_path):
            return RetrievalCompleteEvent(nodes=[], query=ev.query)

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        all_items = data.get("items", {}).get(ev.category, [])
        
        filtered_items = []
        if not ev.keywords:
            filtered_items = all_items[-10:] # ברירת מחדל אם אין מילות מפתח
        else:
            for item in all_items:
                item_text = str(item).lower()
                if any(kw.lower() in item_text for kw in ev.keywords):
                    filtered_items.append(item)
            
            # אם הסינון היה אגרסיבי מדי ולא מצא כלום, ניקח את האחרונים
            if not filtered_items:
                filtered_items = all_items[-5:]

        filtered_items = filtered_items[:15] # הגבלה למניעת עומס

        nodes = []
        for item in filtered_items:
            # יצירת טקסט עשיר עם כותרות ברורות ל-LLM
            content = f"--- DATABASE RECORD ({ev.category.upper()}) ---\n"
            if ev.category == 'rules':
                content += f"RULE: {item.get('rule')}\nSCOPE: {item.get('scope')}"
            elif ev.category == 'decisions':
                content += f"DECISION: {item.get('title')}\nSUMMARY: {item.get('summary')}"
            elif ev.category == 'warnings':
                content += f"WARNING: {item.get('message')}\nSEVERITY: {item.get('severity')}"
            
            # ציון גבוה מאוד כי זה מידע מובנה ומדויק
            nodes.append(NodeWithScore(node=TextNode(text=content), score=1.0))
            
        print(f"Found {len(nodes)} relevant items in JSON after filtering.")
        return RetrievalCompleteEvent(nodes=nodes, query=ev.query)

    @step
    async def semantic_retrieval(self, ev: SemanticSearchEvent) -> RetrievalCompleteEvent:
        """שלב 3ב: שליפה סמנטית מ-Pinecone"""
        print(f"--- [Step 3b: Semantic Retrieval from Pinecone] ---")
        nodes = self.retriever.retrieve(ev.query)
        return RetrievalCompleteEvent(nodes=nodes, query=ev.query)

    @step
    async def evaluate_confidence(self, ev: RetrievalCompleteEvent) -> ValidationPassedEvent | StopEvent:
        """שלב 4: בדיקת איכות המידע שנשלף"""
        if not ev.nodes:
            return StopEvent(result="❌ לא נמצא מידע רלוונטי במערכת.")

        top_score = ev.nodes[0].score
        print(f"--- [Step 4: Confidence Check] Top Score: {top_score:.2f} ---")
        
        # רף ביטחון - אם המידע רחוק מדי מהשאלה
        if top_score < 0.35:
            return StopEvent(result="⚠️ המידע שנמצא אינו מספיק רלוונטי. נסי לשאול בצורה אחרת.")
            
        return ValidationPassedEvent(nodes=ev.nodes, query=ev.query)

    @step
    async def generate_response(self, ev: ValidationPassedEvent) -> StopEvent:
        """שלב 5: יצירת תשובה סופית (Synthesis)"""
        print(f"--- [Step 5: Generating Response] ---")
        response = self.synthesizer.synthesize(query=ev.query, nodes=ev.nodes)
        return StopEvent(result=str(response))