import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME
from backend.logger import logger

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)

def generate_response(system_prompt, user_input, history):
    try:
        prompt = system_prompt + "\nConversation:\n"

        for msg in history:
            prompt += f"{msg['role']}: {msg['content']}\n"

        prompt += f"user: {user_input}"

        response = model.generate_content(prompt)

        logger.info("Gemini API success")
        return response.text

    except Exception as e:
        logger.error(e)
        print("FULL ERROR:", e)   # ⭐ SHOW REAL ERROR IN TERMINAL
        return f"⚠️ ERROR: {e}"