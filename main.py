import os
from flask import Flask, request
import google.generativeai as genai

app = Flask(__name__)

# הגדרת ה-API של גוגל דרך משתנה סביבה (נציב אותו בהמשך ב-Render)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Server is running!"

@app.route('/voice', methods=['GET', 'POST'])
def voice():
    # קבלת הטקסט מימות המשיח
    user_input = request.args.get('ApiText', '')
    
    if not user_input:
        return "id_list_message=t-לא שמעתי שאמרת משהו"

    try:
        # שליחה לבינה המלאכותית
        response = model.generate_content(user_input)
        ai_text = response.text.replace('*', '') # ניקוי תווים מיוחדים
        
        # החזרה לימות המשיח בפורמט הקראה
        return f"id_list_message=t-{ai_text}"
    except Exception as e:
        return f"id_list_message=t-אירעה שגיאה בעיבוד הנתונים"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
