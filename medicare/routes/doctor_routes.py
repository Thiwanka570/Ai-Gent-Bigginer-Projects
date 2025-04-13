from flask import Blueprint, request, jsonify
from models.Doctor import Doctor

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctors', methods=['POST'])
def add_doctor():
    try:
        data = request.get_json()
        
        # Handle both single doctor and bulk upload
        doctors_list = data if isinstance(data, list) else [data]
        
        inserted_ids = []
        duplicates = 0
        
        for doctor in doctors_list:
            # Validate required fields
            if not all(key in doctor for key in ["doctor_id", "name", "specialty"]):
                return jsonify({"error": "Missing required fields (doctor_id, name, specialty)"}), 400
            
            # Check for existing doctor_id
            if Doctor.collection.find_one({"doctor_id": doctor["doctor_id"]}):
                duplicates += 1
                continue
                
            # Insert new doctor
            result = Doctor.create(doctor)
            inserted_ids.append(str(result.inserted_id))
        
        response = {
            "message": f"Successfully added {len(inserted_ids)} doctors",
            "inserted_ids": inserted_ids
        }
        
        if duplicates > 0:
            response["warning"] = f"Skipped {duplicates} duplicate doctors"
            
        return jsonify(response), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@doctor_bp.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.get_all()
    return jsonify(doctors), 200