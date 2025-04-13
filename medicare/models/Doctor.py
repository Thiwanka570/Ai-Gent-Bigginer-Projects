from config import Config

db = Config.get_db()

class Doctor:
    collection = db["doctors"]

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)
    
    @classmethod
    def get_all(cls):
        return list(cls.collection.find({}, {"_id": 0}))
    
    @classmethod
    def get_by_specialty(cls, specialty):
        return list(cls.collection.find({"specialty": specialty}, {"_id": 0}))