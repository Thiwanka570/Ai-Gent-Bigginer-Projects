import React, { useState, useRef, useEffect } from 'react';
import {
    Form,
    Button,
    Card,
    ListGroup,
    Spinner,
    Badge,
    Container
} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
    faPaperPlane,
    faUser,
    faRobot,
    faCommentMedical
} from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import './ChatInterface.css'; // We'll create this CSS file

const ChatInterface = ({ patientId, chatHistory, setChatHistory, setDoctors, setCurrentSpecialty, isLoading, setIsLoading }) => {
    const [message, setMessage] = useState('');
    const messagesEndRef = useRef(null);
    const [isTyping, setIsTyping] = useState(false);

    // Auto-scroll to bottom of chat with smooth animation
    useEffect(() => {
        const scrollToBottom = () => {
            messagesEndRef.current?.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'start'
            });
        };

        const timer = setTimeout(scrollToBottom, 100);
        return () => clearTimeout(timer);
    }, [chatHistory]);

    // Start chat session when component mounts
    useEffect(() => {
        const startChat = async () => {
            if (chatHistory.length === 0) {
                setIsLoading(true);
                setIsTyping(true);
                try {
                    const response = await axios.post('http://localhost:5000/api/chat/start', {
                        patient_id: patientId
                    });

                    // Simulate typing effect
                    setTimeout(() => {
                        addMessage(response.data.response, 'agent');
                        setIsTyping(false);
                    }, 1500);

                } catch (error) {
                    addMessage("Sorry, I'm having trouble connecting. Please try again later.", 'agent');
                    setIsTyping(false);
                } finally {
                    setIsLoading(false);
                }
            }
        };
        startChat();
    }, [patientId]);

    const addMessage = (text, sender) => {
        const newMessage = {
            text,
            sender,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            id: Date.now() // Unique ID for each message
        };
        setChatHistory(prev => [...prev, newMessage]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!message.trim() || isLoading) return;

        // Add user message to chat
        addMessage(message, 'user');
        setMessage('');
        setIsLoading(true);
        setIsTyping(true);

        try {
            const response = await axios.post('http://localhost:5000/api/chat/continue', {
                patient_id: patientId,
                message: message
            });

            // Simulate typing delay
            setTimeout(() => {
                if (response.data.status === 'doctor_selection') {
                    setDoctors(response.data.doctors);
                    setCurrentSpecialty(response.data.specialty);
                    addMessage(response.data.message, 'agent');
                } else if (response.data.response) {
                    addMessage(response.data.response, 'agent');
                }
                setIsTyping(false);
            }, 1000);

        } catch (error) {
            addMessage("Sorry, something went wrong. Please try again.", 'agent');
            setIsTyping(false);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Container fluid className="p-0 h-100 chat-container">
            <Card className="border-0 rounded-0 h-100 d-flex flex-column ">
                <Card.Header className="d-flex justify-content-between align-items-center bg-success text-white p-3">
                    <div className="d-flex align-items-center">
                        <FontAwesomeIcon icon={faCommentMedical} className="me-2" />
                        <h5 className="mb-0">MediBot</h5>
                    </div>
                    <Badge bg="light" text="dark" pill>
                        {patientId}
                    </Badge>
                </Card.Header>

                {/* Message area */}
                <Card.Body className="chat-body">
                    <ListGroup variant="flush" className="message-list">
                        {chatHistory.map((msg) => (
                            <ListGroup.Item
                                key={msg.id}
                                className={`message ${msg.sender} border-0 bg-transparent px-2`}
                            >
                                <div className={`message-content d-flex ${msg.sender === 'user' ? 'justify-content-end ' : 'justify-content-start text-dark'}`}>
                                    <div className={`message-bubble ${msg.sender}`}>
                                        <div className="message-sender">
                                            <FontAwesomeIcon icon={msg.sender === 'user' ? faUser : faRobot} className="me-2" />
                                            {msg.sender === 'user' ? 'You' : 'MediBot'}
                                        </div>
                                        <div className="message-text">{msg.text}</div>
                                        <div className="message-time">{msg.time}</div>
                                    </div>
                                </div>
                            </ListGroup.Item>
                        ))}

                        {isTyping && (
                            <ListGroup.Item className="message agent border-0 bg-transparent px-2">
                                <div className="message-content d-flex justify-content-start">
                                    <div className="message-bubble agent typing">
                                        <div className="message-sender">
                                            <FontAwesomeIcon icon={faRobot} className="me-2" />
                                            MediBot
                                        </div>
                                        <div className="typing-indicator">
                                            <span></span>
                                            <span></span>
                                            <span></span>
                                        </div>
                                    </div>
                                </div>
                            </ListGroup.Item>
                        )}

                        <div ref={messagesEndRef} />
                    </ListGroup>
                </Card.Body>

                {/* Chat input */}

            </Card>
            <div className="chat-footer">
                <Form onSubmit={handleSubmit} className="message-form">
                    <Form.Group className="d-flex m-0">
                        <Form.Control
                            type="text"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="Type your message..."
                            disabled={isLoading}
                            className="border-0 rounded-start-pill shadow-none py-2 px-3"
                        />
                        <Button
                            variant="success"
                            type="submit"
                            disabled={isLoading || !message.trim()}
                            className="rounded-end-pill px-4"
                        >
                            {isLoading ? (
                                <Spinner animation="border" size="sm" role="status">
                                    <span className="visually-hidden">Sending...</span>
                                </Spinner>
                            ) : (
                                <FontAwesomeIcon icon={faPaperPlane} />
                            )}
                        </Button>
                    </Form.Group>
                </Form>
            </div>
        </Container>

    );
};

export default ChatInterface;