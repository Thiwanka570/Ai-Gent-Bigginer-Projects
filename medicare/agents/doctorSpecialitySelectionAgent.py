import google.generativeai as genai
import json
from config import Config
from datetime import datetime
from .prompt import SPECIALTY_PROMPT

class DoctorSpecialitySelectionAgent:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            'gemini-1.5-pro',  # Recommended for better reasoning
            system_instruction=SPECIALTY_PROMPT  # Set as system instruction
        )
        self.chat = None

    def start_session(self, patient_id):
        """Initialize a new specialty recommendation session"""
        self.chat = self.model.start_chat()
        response = self.chat.send_message(
            f"New patient case for specialty recommendation.\nPatient ID: {patient_id}"
        )
        return {
            "status": "session_started",
            "response": response.text,
            "patient_id": patient_id
        }

    def fetch_matching_speciality(self, patient_data):
        """
        Analyze patient data and return specialty recommendations
        Args:
            patient_data: Dict containing patient symptoms in your standard format
        Returns:
            Dict with recommendation or error
        """
        if not self.chat:
            raise ValueError("Session not initialized. Call start_session() first.")
        
        if not isinstance(patient_data, dict):
            raise ValueError("patient_data must be a dictionary")
        
        try:
            # Convert patient data to string for the LLM
            patient_data_str = json.dumps(patient_data, indent=2)
            response = self.chat.send_message(
                f"Analyze these symptoms and recommend specialties:\n{patient_data_str}"
            )
            
            # Improved JSON extraction
            response_text = response.text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            # Validate JSON structure
            recommendation = json.loads(json_str)
            required_keys = ["primary_specialty", "secondary_options", "urgency"]
            if not all(key in recommendation for key in required_keys):
                raise ValueError("Incomplete recommendation format")
            
            return {
                "status": "success",
                "recommendation": recommendation,
                "raw_response": response_text  # For debugging
            }
            
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "error": f"Failed to parse response: {str(e)}",
                "response": response_text
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "response": response.text if 'response' in locals() else None
            }