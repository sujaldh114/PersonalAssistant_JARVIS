import google.generativeai as genai
from engine.config import API_KEY

model = None
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("models/gemini-2.5-flash")


def ask_gemini(prompt):
    if model is None:
        message = "Gemini API key is not configured. Set GEMINI_API_KEY before using AI questions."
        print(message)
        return message

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini API Error:", e)
        return "Sorry, I couldn’t connect to Google AI right now."
