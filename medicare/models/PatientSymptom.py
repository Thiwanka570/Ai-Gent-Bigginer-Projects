from datetime import datetime
from pymongo import IndexModel
from config import Config

db = Config.get_db()

class PatientSymptom:
    collection = db["patient_symptoms"]  # More standard naming
    
    # Create indexes (only needs to run once)
    collection.create_indexes([
        IndexModel([("patient_id", 1)]),  # Faster patient queries
        IndexModel([("timestamp", -1)]),  # Recent first sorting
        IndexModel([("symptoms.name", "text")])  # Text search on symptom names
    ])

    @classmethod
    def create(cls, patient_id: str, symptoms: list):
        """
        Save structured symptom data
        Args:
            patient_id: Unique patient identifier
            symptoms: List of symptom dictionaries with:
                - name (str): Symptom name (e.g., "headache")
                - duration_hours (int): How long symptom has lasted
                - severity (int 1-10): Severity rating
                - location (str): Body location (optional)
                - notes (str): Additional details (optional)
        """
        document = {
            "patient_id": patient_id,
            "symptoms": cls._validate_symptoms(symptoms),
            "timestamp": datetime.utcnow(),  # Always use UTC
            "status": "recorded"  # Can be: recorded, reviewed, diagnosed
        }
        return cls.collection.insert_one(document)

    @classmethod
    def _validate_symptoms(cls, symptoms):
        """Ensure symptom data meets requirements"""
        validated = []
        for symptom in symptoms:
            if not isinstance(symptom, dict):
                raise ValueError("Each symptom must be a dictionary")
                
            if "name" not in symptom:
                raise ValueError("Symptom missing required 'name' field")
                
            # Set defaults for optional fields
            symptom.setdefault("duration_hours", 0)
            symptom.setdefault("severity", 1)
            symptom.setdefault("location", "general")
            
            validated.append(symptom)
        return validated

    @classmethod
    def get_by_patient(cls, patient_id: str, limit: int = 10):
        """Get patient's symptoms sorted newest first"""
        return list(cls.collection.find(
            {"patient_id": patient_id},
            {"_id": 0}
        ).sort("timestamp", -1).limit(limit))

    @classmethod
    def get_recent_by_symptom(cls, symptom_name: str, days: int = 7):
        """Find recent cases of a specific symptom"""
        return list(cls.collection.find({
            "symptoms.name": symptom_name,
            "timestamp": {"$gte": datetime.utcnow() - timedelta(days=days)}
        }, {"_id": 0}))

    @classmethod
    def add_followup_notes(cls, record_id: str, notes: str):
        """Add follow-up information to existing symptom record"""
        return cls.collection.update_one(
            {"_id": record_id},
            {"$set": {"status": "reviewed", "doctor_notes": notes}}
        )