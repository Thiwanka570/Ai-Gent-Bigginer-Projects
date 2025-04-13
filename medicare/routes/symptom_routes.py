from flask import Blueprint, request, jsonify
from models.Symptom import Symptom
from datetime import datetime

symptom_bp = Blueprint('symptom', __name__)

@symptom_bp.route('/symptoms', methods=['POST'])
def add_symptoms():
    try:
        data = request.get_json()

        # Validate request format
        if not data:
            return jsonify({"error": "Request body cannot be empty"}), 400

        # Handle both single and bulk symptom uploads
        symptoms_list = data if isinstance(data, list) else [data]

        inserted_ids = []
        errors = []

        for idx, symptom_data in enumerate(symptoms_list):
            # Validate required fields
            if 'patient_id' not in symptom_data:
                errors.append(f"Entry {idx}: Missing 'patient_id'")
                continue
            if 'symptoms' not in symptom_data or not isinstance(symptom_data['symptoms'], list):
                errors.append(f"Entry {idx}: 'symptoms' must be a list")
                continue

            # Add timestamp and validate symptom format
            symptom_record = {
                "patient_id": symptom_data['patient_id'],
                "symptoms": [s.strip().lower() for s in symptom_data['symptoms']],
                "timestamp": datetime.utcnow(),
                "status": "recorded"  # Can be 'recorded', 'processed', 'diagnosed' etc.
            }

            # Optional: Additional metadata
            if 'notes' in symptom_data:
                symptom_record['notes'] = symptom_data['notes']
            if 'severity' in symptom_data:
                symptom_record['severity'] = symptom_data['severity']

            # Insert into database
            try:
                result = Symptom.collection.insert_one(symptom_record)
                inserted_ids.append(str(result.inserted_id))
            except Exception as e:
                errors.append(f"Entry {idx}: Database error - {str(e)}")
                continue

        # Prepare response
        response = {
            "message": f"Successfully recorded {len(inserted_ids)} symptom entries",
            "inserted_ids": inserted_ids
        }

        if errors:
            response["errors"] = errors
            response["error_count"] = len(errors)

        status_code = 201 if inserted_ids else 400 if not errors else 207  # Multi-status
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@symptom_bp.route('/patients/<patient_id>/symptoms', methods=['GET'])
def get_patient_symptoms(patient_id):
    symptoms = Symptom.get_by_patient(patient_id)
    return jsonify(symptoms), 200