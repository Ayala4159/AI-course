<div dir="rtl" style="direction: rtl; text-align: right;">

# Project 01: Moroccan Grandma Task Manager

### תיאור הפרויקט
פרויקט זה פותח במסגרת קורס AI Agents בהנחיית מלכה ברוק. המערכת מציגה סוכן בינה מלאכותית המנהל משימות עבור המשתמש תוך שימוש בפרסונה ייחודית של סבתא מרוקאית.

---

### ארכיטקטורת הסוכן (Models & Logic)
<ul style="list-style-position: inside; padding-right: 0;">
  <li><strong>Agent Service:</strong> ה"מוח" של המערכת, המבוסס על מודל שפה גדול.</li>
  <li><strong>Persona:</strong> הגדרת אישיות הסבתא באמצעות הנדסת פרומפט (System Prompt) הכוללת חום, דאגה וניואנסים תרבותיים.</li>
  <li><strong>NLP Parsing:</strong> יכולת ניתוח טקסט חופשי והמרתו למשימות מובנות הכוללות כותרת ותוכן.</li>
  <li><strong>Context Awareness:</strong> שמירה על הקשר השיחה והגבה רלוונטית בהתאם לדחיפות המטלות.</li>
  <li><strong>Task Logic:</strong> ניהול רשימת המשימות הכולל כותרת, פירוט וסטטוס ביצוע (New / In Progress / Completed).</li>
</ul>

---

### תצוגת מסכי המערכת
![Grandma Interface](./screenshots/GrandmaTaskManager.png)

**הוספת משימה בשפה טבעית וקבלת תגובה מהסוכן.**

---

### טכנולוגיות בשימוש
<ul style="list-style-position: inside; padding-right: 0;">
  <li><strong>Backend:</strong> שפת Python (שימוש ב-python-dotenv לניהול סביבה).</li>
  <li><strong>AI Engine:</strong> מודל שפה גדול (LLM) וטכניקות הנדסת פרומפט.</li>
  <li><strong>Frontend:</strong> פיתוח ממשק מודרני ב-React / Node.js.</li>
  <li><strong>Version Control:</strong> ניהול גרסאות באמצעות Git & GitHub.</li>
</ul>

---

### הוראות הרצה
1. **Agent:** כניסה לתיקיית Agent, התקנת ספריות והרצת `python main.py`.
2. **Config:** העתקת קובץ `.env.example` ל-`.env` והזנת מפתח API מתאים.
3. **Client:** כניסה לתיקיית task-manager-client, הרצת `npm install` ופתיחת הממשק ע"י `npm start`.

---

</div>