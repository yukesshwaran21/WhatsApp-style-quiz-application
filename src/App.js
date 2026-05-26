import React, { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import ExamFlow from './ExamFlow';
import QuizScreen from './QuizScreen';
import AnalyticsDashboard from './AnalyticsDashboard';
import './index.css';

function App() {
  const [view, setView] = useState('home'); // 'home' | 'quiz' | 'analytics'
  const [quizSession, setQuizSession] = useState(null);
  const [quizContext, setQuizContext] = useState(null);

  const handleSessionStart = (session, context) => {
    setQuizSession(session);
    setQuizContext(context);
    setView('quiz');
  };

  const handleFinish = () => {
    setQuizSession(null);
    setQuizContext(null);
    setView('home');
  };

  const handleRetry = () => {
    setQuizSession(null);
    setQuizContext(null);
    setView('home');
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--wa-bg)' }}>
      <Toaster
        position="top-center"
        toastOptions={{
          style: {
            background: '#ffffff',
            color: '#0f172a',
            border: '1px solid #e2e8f0',
            fontSize: '14px',
            fontWeight: '600',
            borderRadius: '10px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
          },
        }}
      />

      {/* ─── Navigation Bar ─────────────────────────────────── */}
      <nav className="navbar">
        <div
          className="navbar-brand"
          onClick={() => { setView('home'); setQuizSession(null); setQuizContext(null); }}
          style={{ cursor: 'pointer' }}
        >
          <div className="navbar-logo">📱</div>
          <div>
            <div className="navbar-title">QuizBytes</div>
            <div className="navbar-subtitle">Smart Quiz Platform</div>
          </div>
        </div>

        <div className="navbar-actions">
          <button
            className={`nav-btn ${view === 'home' || view === 'quiz' ? 'active' : ''}`}
            onClick={() => { setView('home'); setQuizSession(null); setQuizContext(null); }}
          >
            🏠 Home
          </button>
          <button
            className={`nav-btn ${view === 'analytics' ? 'active' : ''}`}
            onClick={() => setView('analytics')}
          >
            📊 Analytics
          </button>
        </div>
      </nav>

      {/* ─── Main Content ──────────────────────────────────── */}
      <main>
        {view === 'home' && (
          <ExamFlow onSessionStart={handleSessionStart} />
        )}

        {view === 'quiz' && quizSession && (
          <QuizScreen
            session={quizSession}
            context={quizContext}
            onFinish={handleFinish}
            onRetry={handleRetry}
          />
        )}

        {view === 'analytics' && (
          <AnalyticsDashboard />
        )}
      </main>
    </div>
  );
}

export default App;
