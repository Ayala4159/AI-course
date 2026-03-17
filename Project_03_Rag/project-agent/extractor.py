import json
import os
from datetime import datetime
from llama_index.core import Settings, PromptTemplate 
from models import ExtractionResult
import asyncio

async def run_extraction(nodes):
    llm = Settings.llm
    output_file = "extracted_data.json"
    
    # --- טעינת נתונים קיימים כדי לא לדרוס ---
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            final_data = json.load(f)
        print(f"📂 נמצא קובץ קיים. ממשיך להוסיף עליו...")
    else:
        final_data = {
            "schema_version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "items": {
                "decisions": [],
                "rules": [],
                "warnings": []
            }
        }

    # פרומפט משופר עם הוראת פורמט נוקשה
    prompt_t = PromptTemplate(
            "ROLE: System Architect Analyst\n"
            "TASK: Extract ACTUAL engineering data from the provided text. DO NOT use examples from instructions.\n\n"
            "INSTRUCTIONS:\n"
            "1. Identify real architectural choices made in the code (e.g., specific libraries used, class structures).\n"
            "2. Identify strict coding rules or patterns visible in the text.\n"
            "3. Identify technical debt, missing documentation, or risks.\n\n"
            "STRICT RULES:\n"
            "- If no data is found for a category, return an empty list [].\n"
            "- Use the actual filename provided in the context.\n"
            "- 'observed_at' must be a valid ISO date (2026-03-16).\n"
            "- Strictly return a SINGLE JSON object. No multiple tool calls.\n" # מונע שגיאה 400
            "- DO NOT mention 'FastAPI' or 'RTL' unless they actually appear in the text.\n\n"
            "TEXT TO ANALYZE:\n{text}"
        )

    print(f"🚀 מתחיל חילוץ עמוק מ-{len(nodes)} קטעים...")
        
    for i, node in enumerate(nodes):
            # תיקון נתיב הקובץ: לוקח רק את שם הקובץ כדי למנוע בעיות עברית ב-JSON
            full_path = node.metadata.get('file_path', 'Unknown File')
            file_name = os.path.basename(full_path) 
            
            content = f"FILE PATH: {file_name}\n---\n{node.get_content()}"
            
            try:
                # המתנה יזומה כדי לא להיחסם
                await asyncio.sleep(7.5) 
                
                result = await llm.astructured_predict(
                    ExtractionResult,
                    prompt=prompt_t,
                    text=content 
                )

                if hasattr(result, 'decisions'):
                    # הזרקת IDs ייחודיים
                    for idx, d in enumerate(result.decisions):
                        d.id = f"dec-{i}-{idx}"
                    for idx, r in enumerate(result.rules):
                        r.id = f"rule-{i}-{idx}"
                    for idx, w in enumerate(result.warnings):
                        w.id = f"warn-{i}-{idx}"

                    # הוספה (Append) לנתונים הקיימים
                    final_data["items"]["decisions"].extend([d.dict() for d in result.decisions])
                    final_data["items"]["rules"].extend([r.dict() for r in result.rules])
                    final_data["items"]["warnings"].extend([w.dict() for w in result.warnings])

                    # שמירה לקובץ אחרי כל קטע
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(final_data, f, ensure_ascii=False, indent=4)

                    print(f"✅ מעבד קטע {i + 1}/{len(nodes)}... (נשמר!)")
                else:
                    print(f"⚠️ קטע {i+1}: המודל לא החזיר מבנה תקין, מדלג...")

            except Exception as e:
                if "429" in str(e):
                    print(f"🛑 עומס ב-Groq (קטע {i+1}). מחכה 20 שניות...")
                    await asyncio.sleep(20)
                else:
                    print(f"❌ שגיאה בקטע {i+1}: {e}")

    print(f"\n✨ התהליך הסתיים! הנתונים נמצאים ב-{output_file}")