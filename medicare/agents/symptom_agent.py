import google.generativeai as genai
from config import Config
from datetime import datetime
from .prompt import SYSTEM_PROMPT

class SymptomChatAgent:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.chat = None

    def start_session(self, patient_id):
        self.chat = self.model.start_chat()
        response = self.chat.send_message(
            f"{SYSTEM_PROMPT}\nPatient ID: {patient_id}\nBegin conversation:"
        )
        return response.text

    def continue_chat(self, user_input):
        response = self.chat.send_message(user_input)
        
        try:
            if "```json" in response.text:
                # Extract JSON from markdown response
                json_str = response.text.split("```json")[1].split("```")[0]
                return {"mode": "completed", "data": json_str}
        except:
            pass
        
        return {"mode": "chat", "text": response.text}