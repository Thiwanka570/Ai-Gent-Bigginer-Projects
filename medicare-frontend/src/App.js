import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import ChatInterface from './component/ChatInterface';
import DoctorList from './component/DoctorList';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRobot } from '@fortawesome/free-solid-svg-icons';

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [currentSpecialty, setCurrentSpecialty] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [patientId, setPatientId] = useState('');

  // Initialize patient session
  useEffect(() => {
    // Generate or get patient ID from localStorage
    const storedId = localStorage.getItem('patientId') || `pat${Math.floor(1000 + Math.random() * 9000)}`;
    localStorage.setItem('patientId', "pat1001");
    setPatientId(storedId);
  }, []);

  return (
    <Container fluid className="app-container">
      <Row>
        <Col md={8} className="chat-column">
          <ChatInterface
            patientId={"pat1001"}
            chatHistory={chatHistory}
            setChatHistory={setChatHistory}
            setDoctors={setDoctors}
            setCurrentSpecialty={setCurrentSpecialty}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />
        </Col>
        <Col md={4} className="doctors-column px-3 py-4">
          {doctors.length == 0 ? (
            <div className="ai-agent-info text-center p-4">
            <div className="ai-agent-animation">
              <FontAwesomeIcon icon={faRobot} size="2x" className="mb-3 text-success" />
              
              <p className="typing-text">
                <span className="line">
                  <strong>Our AI-powered Medical Assistant</strong> is analyzing your symptoms...
                </span>
                <br />
                <span className="line delay">
                  <strong>Matching you</strong> with the most suitable doctors for your condition.
                </span>
                <br />
                <span className="line delay2">
                  Once matched, you can <strong>instantly schedule an appointment</strong> — no wait, no hassle.
                </span>
              </p>
              
              <div className="loading-dots mt-4">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
          

          ) : (

            <DoctorList
              doctors={doctors}
              specialty={currentSpecialty}
              isLoading={isLoading}
            />
          )}
        </Col>

      </Row>
    </Container>
  );
}

export default App;