import axios from 'axios';

const API_BASE = 'https://whatsapp-style-quiz-application-4.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

export const getExams = () => api.get('/exams').then(r => r.data);
export const getSubjects = (examId) => api.get(`/subjects/${examId}`).then(r => r.data);
export const getChapters = (subjectId) => api.get(`/chapters/${subjectId}`).then(r => r.data);
export const getUsers = () => api.get('/users').then(r => r.data);

export const startSession = (data) => api.post('/session/start', data).then(r => r.data);
export const submitAnswer = (data) => api.post('/session/answer', data).then(r => r.data);
export const finishSession = (data) => api.post('/session/finish', data).then(r => r.data);

// Analytics
export const getAnalyticsOverview = () => api.get('/analytics/overview').then(r => r.data);
export const getDailyActiveUsers = () => api.get('/analytics/daily-active-users').then(r => r.data);
export const getWeeklyActiveUsers = () => api.get('/analytics/weekly-active-users').then(r => r.data);
export const getQuestionsStats = () => api.get('/analytics/questions-stats').then(r => r.data);
export const getAvgResponseTime = () => api.get('/analytics/avg-response-time').then(r => r.data);
export const getCompletionRate = () => api.get('/analytics/completion-rate').then(r => r.data);
export const getDropoffAnalysis = () => api.get('/analytics/dropoff').then(r => r.data);
export const getPeakHours = () => api.get('/analytics/peak-hours').then(r => r.data);
export const getAvgQuestionsPerSession = () => api.get('/analytics/avg-questions-per-session').then(r => r.data);

export default api;
