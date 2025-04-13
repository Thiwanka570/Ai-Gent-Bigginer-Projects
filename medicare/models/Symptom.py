from config import Config

db = Config.get_db()

class Symptom:
    collection = db["symptoms"]

    @classmethod
    def create(cls, patient_id, symptoms):
        return cls.collection.insert_one({
            "patient_id": patient_id,
            "symptoms": symptoms,
            "timestamp": datetime.now()
        })
    
    @classmethod
    def get_by_patient(cls, patient_id):
        return list(cls.collection.find({"patient_id": patient_id}, {"_id": 0}))