from flask import Blueprint, request, jsonify
from models.Patient import Patient

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    result = Patient.create(data)
    return jsonify({"message": "Patient created", "patient_id": str(result.inserted_id)}), 201

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.get_all()
    return jsonify(patients), 200