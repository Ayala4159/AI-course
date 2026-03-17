# החלטות טכנולוגיות - Backend

## טכנולוגיה
- **Framework:** Flask (Python).
- **Frontend:** HTML5/CSS3 עם JavaScript וניל (Vanilla).

## מבנה הנתונים (Task Schema)
כל משימה במערכת מכילה:
- `task_id`: מזהה ייחודי.
- `title`: כותרת המשימה.
- `description`: תיאור נוסף (אופציונלי).
- `priority`: עדיפות (LOW, MEDIUM, HIGH, CRITICAL).
- `status`: מצב המשימה (pending, completed).

## ארכיטקטורה
המערכת משתמשת ב-Client-side rendering פשוט: הדף נטען, ושואב את המשימות ב-AJAX מנתיב `/tasks` בכל 3 שניות (Polling) כדי לשמור על סנכרון. 