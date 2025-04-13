from flask import Flask
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.symptom_routes import symptom_bp
from routes.chat_routes import chat_bp
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Register blueprints
app.register_blueprint(patient_bp, url_prefix='/api')
app.register_blueprint(doctor_bp, url_prefix='/api')
app.register_blueprint(symptom_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)