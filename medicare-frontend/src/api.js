import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
});

export const startChat = (patientId) => api.post('/chat/start', { patient_id: patientId });
export const continueChat = (patientId, message) => api.post('/chat/continue', { patient_id: patientId, message });
export const resetTestSession = () => api.post('/chat/test/reset');

export default api;