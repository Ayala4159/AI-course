import openai
import json
import todo_service
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    base_url="URL",
    api_key="OPENAI_API_KEY"
)

MODEL = "MODEL_NAME"

def agent(query, history=[]):
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    logic_prompt = f"""
    Today is {today}. Tomorrow is {tomorrow}.
    Extract the user's intent into JSON.
    If the user says "I need to do X" or "Remind me Y", you MUST use action "add".
    
    Format:
    - {{"action": "add", "params": {{"title": "The task", "start_date": "YYYY-MM-DD"}}}}
    - {{"action": "get", "params": {{"date_filter": "YYYY-MM-DD"}}}}
    - {{"action": "chat", "reply": "answer"}}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": logic_prompt}, {"role": "user", "content": query}],
            response_format={"type": "json_object"}
        )
        
        decision = json.loads(response.choices[0].message.content)
        action = decision.get("action")
        params = decision.get("params", {})
        system_output = ""

        if action == "add":
            title = params.get("title")
            date = params.get("start_date", tomorrow if "מחר" in query else today)
            if title:
                system_output = todo_service.add_task(title=title, start_date=date)
            else:
                system_output = "לא הצלחתי להבין מה לרשום."

        elif action == "get":
            date = params.get("date_filter", tomorrow if "מחר" in query else today)
            tasks = todo_service.get_tasks(date_filter=date)
            system_output = f"משימות לתאריך {date}: {tasks}" if tasks else "המחברת ריקה לתאריך הזה."

        else:
            system_output = decision.get("reply", "סתם שיחה")

        grandma_prompt = f"""
        את סבתא מרוקאית חמה, מצחיקה וחכמה. 
        הנכדה שלך שואלת אותך שאלות. 
        
        הנתונים האמיתיים מהמחברת הם: {system_output}
        
        חוקי המענה:
        1. אם המשתמשת שואלת "מה אני צריכה לעשות" או שואלת על משימות, את חייבת לפרט את המשימות שמופיעות בנתונים לעיל! 
        2. אל תגידי רק "רשמתי", תגידי *מה* רשום. למשל: "בניתי, רשום לנו מחר להכין אוכל".
        3. אם המערכת אומרת שהמשימה נוספה בהצלחה, תאשרי לה: "רשמתי לך במחברת שצריך {query}, שלא תשכחי נסיכה".
        4. דברי רק בנקבה.
        """

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": grandma_prompt},
                {"role": "user", "content": f"שאילתה: {query}. מידע מהמערכת: {system_output}"}
            ]
        )
        return final_response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "אוי בניתי, נהיה לי בלאגן בראש, תשאלי שוב כפרה?"