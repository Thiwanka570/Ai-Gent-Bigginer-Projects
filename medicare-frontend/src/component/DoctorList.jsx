import React from 'react';
import { Card, Row, Col, Spinner, Alert, Badge } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faUserMd,
  faStar,
  faClock,
  faCalendarAlt
} from '@fortawesome/free-solid-svg-icons';
import './DoctorList.css'; // We'll create this CSS file

const DoctorList = ({ doctors, specialty, isLoading }) => {
  // Function to group doctors by availability
  const groupDoctorsByAvailability = () => {
    const grouped = {};
    
    doctors.forEach(doctor => {
      doctor.availability.forEach(slot => {
        if (!grouped[slot]) {
          grouped[slot] = [];
        }
        grouped[slot].push(doctor);
      });
    });
    
    return grouped;
  };

  const availabilityGroups = groupDoctorsByAvailability();
  const availableSlots = Object.keys(availabilityGroups).slice(0, 5); // Get first 5 time slots

  return (
    <Card className="doctors-card border-0 shadow-sm">
      <Card.Header className="bg-dark text-white">
        <h5 className="mb-0">
          <FontAwesomeIcon icon={faUserMd} className="me-2" />
          {specialty ? `${specialty} Specialists` : "Available Doctors"}
        </h5>
      </Card.Header>
      
      <Card.Body className="p-4">
        {isLoading ? (
          <div className="text-center py-4">
            <Spinner animation="border" variant="primary" />
            <p className="mt-2">Finding available doctors...</p>
          </div>
        ) : availableSlots.length > 0 ? (
          <div className="time-slots-container">
            <h6 className="mb-3 text-muted">
              <FontAwesomeIcon icon={faClock} className="me-2" />
              Available Time Slots
            </h6>
            
            {availableSlots.map((slot, slotIndex) => (
              <div key={slotIndex} className="time-slot-group mb-4">
                <div className="time-slot-header mb-2">
                  <Badge bg="primary" pill>
                    <FontAwesomeIcon icon={faCalendarAlt} className="me-1" />
                    {slot}
                  </Badge>
                </div>
                
                <Row className="g-3">
                  {availabilityGroups[slot].map((doctor, doctorIndex) => (
                    <Col key={doctorIndex} >
                      <Card className="h-100 doctor-card">
                        <Card.Body>
                          <div className="d-flex align-items-start mb-3">
                            <div className="doctor-avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3">
                              {doctor.name.charAt(0)}
                            </div>
                            <div>
                              <h6 className="mb-0">{doctor.name}</h6>
                              <small className="text-muted">{doctor.specialty}</small>
                            </div>
                          </div>
                          
                          <div className="doctor-rating mb-2">
                            {[...Array(5)].map((_, i) => (
                              <FontAwesomeIcon 
                                key={i}
                                icon={faStar}
                                className={i < Math.floor(doctor.rating) ? "text-warning" : "text-muted"}
                                size="sm"
                              />
                            ))}
                            <span className="ms-2 text-muted small">{doctor.rating.toFixed(1)}</span>
                          </div>
                          
                          <div className="d-grid">
                            <button className="btn btn-outline-primary btn-sm">
                              Book This Slot
                            </button>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </div>
            ))}
          </div>
        ) : (
          <Alert variant="light" className="text-center py-4">
            <FontAwesomeIcon icon={faUserMd} size="2x" className="mb-3 text-muted" />
            <h5>
              {specialty 
                ? `No ${specialty} specialists available` 
                : "Complete your symptom analysis"}
            </h5>
            <p className="text-muted">
              {specialty
                ? "Please check back later or try a different time"
                : "We'll recommend the right doctors for your symptoms"}
            </p>
          </Alert>
        )}
      </Card.Body>
    </Card>
  );
};

export default DoctorList;