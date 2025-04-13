from flask import Blueprint, request, jsonify
from agents.symptom_agent import SymptomChatAgent
from agents.doctorSpecialitySelectionAgent import DoctorSpecialitySelectionAgent
from models.PatientSymptom import PatientSymptom
from models.Doctor import Doctor
from datetime import datetime
import json

chat_bp = Blueprint('chat', __name__)

# Initialize sessions with test patient
TEST_PATIENT = "pat1001"
active_sessions = {
    "symptom": {TEST_PATIENT: SymptomChatAgent()},  # Symptom collection sessions
    "specialty": {}                                  # Specialty selection sessions
}

@chat_bp.route('/chat/start', methods=['POST'])
def start_chat():
    data = request.get_json()
    patient_id = data.get('patient_id', TEST_PATIENT)
    
    # Clear any existing sessions for this patient
    if patient_id in active_sessions["symptom"]:
        del active_sessions["symptom"][patient_id]
    if patient_id in active_sessions["specialty"]:
        del active_sessions["specialty"][patient_id]
    
    # Create new symptom collection session
    agent = SymptomChatAgent()
    greeting = agent.start_session(patient_id)
    
    active_sessions["symptom"][patient_id] = agent
    return jsonify({
        "response": greeting,
        "session_type": "symptom_collection",
        "is_test_session": patient_id == TEST_PATIENT,
        "patient_id": patient_id
    })

@chat_bp.route('/chat/continue', methods=['POST'])
def continue_chat():
    data = request.get_json()
    patient_id = data.get('patient_id')
    
    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400
    
    user_input = data['message']
    
    # Check active sessions in priority order
    if patient_id in active_sessions["symptom"]:
        agent = active_sessions["symptom"][patient_id]
        response = agent.continue_chat(user_input)
        
        if response["mode"] == "completed":
            try:
                # Process and save symptoms
                symptom_data = json.loads(response["data"])
                symptom_data.update({
                    "timestamp": datetime.utcnow().isoformat(),
                    "is_test_data": patient_id == TEST_PATIENT
                })
                
                # Only save to DB if not test data
                if patient_id != TEST_PATIENT:
                    result = PatientSymptom.collection.insert_one(symptom_data)
                    symptom_data["record_id"] = str(result.inserted_id)
                else:
                    print("Test data would save:", symptom_data)
                
                # Transition to specialty selection
                specialty_agent = DoctorSpecialitySelectionAgent()
                specialty_agent.start_session(patient_id)
                active_sessions["specialty"][patient_id] = specialty_agent
                del active_sessions["symptom"][patient_id]
                
                # Get initial specialty recommendation
                specialty_response = specialty_agent.fetch_matching_speciality(symptom_data)
                
                if specialty_response.get("status") != "success":
                    return jsonify({
                        "error": "Failed to get specialty recommendation",
                        "details": specialty_response.get("error", "Unknown error")
                    }), 500
                
                # Find available doctors
                recommended_specialty = specialty_response["recommendation"]["primary_specialty"]["name"]
                available_doctors = Doctor.get_by_specialty(recommended_specialty)
                
                return jsonify({
                    "status": "doctor_selection",
                    "message": "Here are suitable doctors for your symptoms:",
                    "specialty": recommended_specialty,
                    "doctors": available_doctors,
                    "recommendation": specialty_response["recommendation"],
                    "patient_id": patient_id,
                    "is_test_session": patient_id == TEST_PATIENT
                })
                
            except Exception as e:
                return jsonify({
                    "error": f"Failed to process symptoms: {str(e)}",
                    "details": str(response["data"]) if "data" in response else None
                }), 500
        else:
            return jsonify({
                "response": response["text"],
                "session_type": "symptom_collection",
                "patient_id": patient_id,
                "is_test_session": patient_id == TEST_PATIENT
            })
    
    elif patient_id in active_sessions["specialty"]:
        agent = active_sessions["specialty"][patient_id]
        response = agent.fetch_matching_speciality({"message": user_input})
        
        if response.get("status") == "success":
            # Refresh doctor list
            recommended_specialty = response["recommendation"]["primary_specialty"]["name"]
            available_doctors = Doctor.find_by_specialty(recommended_specialty)
            
            return jsonify({
                "status": "doctor_selection",
                "specialty": recommended_specialty,
                "doctors": available_doctors,
                "recommendation": response["recommendation"],
                "patient_id": patient_id,
                "is_test_session": patient_id == TEST_PATIENT
            })
        else:
            return jsonify({
                "error": response.get("error", "Failed to process specialty selection"),
                "details": response.get("details"),
                "patient_id": patient_id
            }), 400
    
    return jsonify({
        "error": "No active session found for this patient",
        "patient_id": patient_id,
        "suggestion": "Start a new session with /chat/start"
    }), 404

@chat_bp.route('/chat/test/reset', methods=['POST'])
def reset_test_session():
    """Reset test sessions"""
    active_sessions["symptom"][TEST_PATIENT] = SymptomChatAgent()
    if TEST_PATIENT in active_sessions["specialty"]:
        del active_sessions["specialty"][TEST_PATIENT]
    return jsonify({"status": "Test sessions reset"})

@chat_bp.route('/chat/status', methods=['GET'])
def chat_status():
    """Check active session status"""
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({"error": "patient_id parameter is required"}), 400
    
    session_type = None
    if patient_id in active_sessions["symptom"]:
        session_type = "symptom_collection"
    elif patient_id in active_sessions["specialty"]:
        session_type = "specialty_selection"
    
    return jsonify({
        "patient_id": patient_id,
        "active_session": session_type,
        "is_test_session": patient_id == TEST_PATIENT
    })