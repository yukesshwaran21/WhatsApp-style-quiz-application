import React, { useState, useEffect } from 'react';
import { getExams, getSubjects, getChapters, getUsers, startSession } from './api';

export default function ExamFlow({ onSessionStart }) {
  const [step, setStep] = useState('user'); // user → exam → subject → chapter
  const [users, setUsers] = useState([]);
  const [exams, setExams] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [chapters, setChapters] = useState([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [selectedExam, setSelectedExam] = useState(null);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [, setSelectedChapter] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getExams().then(setExams).catch(console.error);
    getUsers().then(u => { setUsers(u); if (u.length > 0) setSelectedUser(u[0].id); }).catch(console.error);
  }, []);

  const handleExamSelect = async (exam) => {
    setSelectedExam(exam);
    setLoading(true);
    try {
      const subs = await getSubjects(exam.id);
      setSubjects(subs);
      setStep('subject');
    } finally {
      setLoading(false);
    }
  };

  const handleSubjectSelect = async (subject) => {
    setSelectedSubject(subject);
    setLoading(true);
    try {
      const chaps = await getChapters(subject.id);
      setChapters(chaps);
      setStep('chapter');
    } finally {
      setLoading(false);
    }
  };

  const handleChapterSelect = async (chapter) => {
    setSelectedChapter(chapter);
    setLoading(true);
    try {
      const session = await startSession({
        user_id: selectedUser,
        exam_id: selectedExam.id,
        subject_id: selectedSubject.id,
        chapter_id: chapter.id,
      });
      onSessionStart(session, { exam: selectedExam, subject: selectedSubject, chapter });
    } catch (err) {
      alert('Failed to start quiz. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const goBack = () => {
    if (step === 'subject') setStep('exam');
    else if (step === 'chapter') setStep('subject');
    else if (step === 'exam') setStep('user');
  };

  const Breadcrumb = () => (
    <div className="breadcrumb">
      <span className={`breadcrumb-item ${step === 'user' ? 'active' : ''}`}>User</span>
      <span className="breadcrumb-sep">›</span>
      <span className={`breadcrumb-item ${step === 'exam' ? 'active' : ''}`}>
        {selectedExam ? selectedExam.name : 'Exam'}
      </span>
      <span className="breadcrumb-sep">›</span>
      <span className={`breadcrumb-item ${step === 'subject' ? 'active' : ''}`}>
        {selectedSubject ? selectedSubject.name : 'Subject'}
      </span>
      <span className="breadcrumb-sep">›</span>
      <span className={`breadcrumb-item ${step === 'chapter' ? 'active' : ''}`}>Chapter</span>
    </div>
  );

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p className="loading-text">Loading...</p>
      </div>
    );
  }

  // ─── Step: User Selection ─────────────────────────────────────────────────
  if (step === 'user') {
    return (
      <div className="page animate-fade-up">
        <div style={{ textAlign: 'center', padding: '20px 0 28px' }}>
          <div style={{ fontSize: 64, marginBottom: 12 }}>📱</div>
          <h1 style={{ fontSize: 26, fontWeight: 800, marginBottom: 6, color: 'var(--wa-text)' }}>
            WhatsApp Quiz
          </h1>
          <p style={{ color: 'var(--wa-text-secondary)', fontSize: 14 }}>
            Smart learning, one question at a time
          </p>
        </div>

        <div className="card" style={{ marginBottom: 20 }}>
          <label style={{ fontSize: 13, color: 'var(--wa-text-secondary)', display: 'block', marginBottom: 8 }}>
            👤 Select your profile
          </label>
          <select
            className="user-selector"
            style={{ width: '100%' }}
            value={selectedUser}
            onChange={e => setSelectedUser(e.target.value)}
          >
            {users.map(u => (
              <option key={u.id} value={u.id}>{u.name}</option>
            ))}
          </select>
        </div>

        <button
          className="btn-primary"
          onClick={() => setStep('exam')}
          disabled={!selectedUser}
        >
          🚀 Start Learning
        </button>

        <div style={{ marginTop: 20, display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          {['JEE', 'NEET', 'UPSC', 'CAT', 'GATE'].map(tag => (
            <span key={tag} className="badge badge-green">{tag}</span>
          ))}
        </div>
      </div>
    );
  }

  // ─── Step: Exam Selection ─────────────────────────────────────────────────
  if (step === 'exam') {
    return (
      <div className="page">
        <Breadcrumb />
        <div className="section-header">
          <h2 className="section-title">📚 Choose Exam</h2>
          <p className="section-subtitle">Select the exam you're preparing for</p>
        </div>
        <div className="card-grid">
          {exams.map((exam, idx) => (
            <div
              key={exam.id}
              className="select-card animate-fade-up"
              style={{ animationDelay: `${idx * 60}ms` }}
              onClick={() => handleExamSelect(exam)}
            >
              <div className="card-icon" style={{ background: `${exam.color}20` }}>
                {exam.icon}
              </div>
              <div className="card-content">
                <h3>{exam.name}</h3>
                <p>{exam.description}</p>
              </div>
              <span className="card-arrow">›</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // ─── Step: Subject Selection ──────────────────────────────────────────────
  if (step === 'subject') {
    return (
      <div className="page">
        <Breadcrumb />
        <button
          onClick={goBack}
          style={{ background: 'none', border: 'none', color: 'var(--wa-text-secondary)', cursor: 'pointer', marginBottom: 16, fontSize: 14, display: 'flex', alignItems: 'center', gap: 4 }}
        >
          ← Back
        </button>
        <div className="section-header">
          <h2 className="section-title">🎯 {selectedExam?.name} — Subjects</h2>
          <p className="section-subtitle">Pick a subject to study</p>
        </div>
        <div className="card-grid">
          {subjects.map((sub, idx) => (
            <div
              key={sub.id}
              className="select-card animate-fade-up"
              style={{ animationDelay: `${idx * 60}ms` }}
              onClick={() => handleSubjectSelect(sub)}
            >
              <div className="card-icon">{sub.icon}</div>
              <div className="card-content">
                <h3>{sub.name}</h3>
              </div>
              <span className="card-arrow">›</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // ─── Step: Chapter Selection ──────────────────────────────────────────────
  if (step === 'chapter') {
    return (
      <div className="page">
        <Breadcrumb />
        <button
          onClick={goBack}
          style={{ background: 'none', border: 'none', color: 'var(--wa-text-secondary)', cursor: 'pointer', marginBottom: 16, fontSize: 14, display: 'flex', alignItems: 'center', gap: 4 }}
        >
          ← Back
        </button>
        <div className="section-header">
          <h2 className="section-title">📖 {selectedSubject?.name} — Chapters</h2>
          <p className="section-subtitle">Choose a chapter to quiz</p>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {chapters.map((chap, idx) => (
            <div
              key={chap.id}
              className="select-card animate-fade-up"
              style={{ animationDelay: `${idx * 50}ms` }}
              onClick={() => handleChapterSelect(chap)}
            >
              <div className="card-icon">📝</div>
              <div className="card-content">
                <h3>{chap.name}</h3>
                <p>{chap.question_count || '10+'} questions</p>
              </div>
              <span className="badge badge-green">{chap.question_count}Q</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return null;
}
