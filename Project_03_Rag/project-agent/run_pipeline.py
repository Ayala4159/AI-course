import asyncio
import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.llms.groq import Groq # ייבוא Groq

# ייבוא הפונקציה מהקובץ החדש שיצרת
from extractor import run_extraction 

load_dotenv()

# הגדרת ה-LLM שבו נשתמש לחילוץ (Groq)
Settings.llm = Groq(
    model="llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY")
)

async def main():
    print("--- [שלב 1: טעינת קבצי MD] ---")
    # טעינת המסמכים מהתיקייה (וודאי שהנתיב נכון, אצלך זה כנראה "./data")
    reader = SimpleDirectoryReader("./data", recursive=True)
    documents = reader.load_data()
    
    # פירוק לקטעים (Nodes)
    parser = MarkdownNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    print(f"נוצרו {len(nodes)} קטעי טקסט לניתוח.")

    print("\n--- [שלב 2: חילוץ נתונים מובנים - Data Extraction] ---")
    # הפעלת החילוץ
    await run_extraction(nodes[300:400])
    
    print("\n✅ התהליך הסתיים! כעת בדקי אם נוצר קובץ 'extracted_data.json'.")

if __name__ == "__main__":
    asyncio.run(main())