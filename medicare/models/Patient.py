from config import Config

db = Config.get_db()

class Patient:
    collection = db["patients"]

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)
    
    @classmethod
    def get_all(cls):
        return list(cls.collection.find({}, {"_id": 0}))
    
    @classmethod
    def get_by_id(cls, patient_id):
        return cls.collection.find_one({"patient_id": patient_id}, {"_id": 0})