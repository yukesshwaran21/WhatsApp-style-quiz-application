import React, { useState, useEffect, useRef } from 'react';
import { submitAnswer, finishSession } from './api';
import toast from 'react-hot-toast';

const OPTION_LABELS = ['A', 'B', 'C', 'D'];

function formatTime(seconds) {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0');
  const s = (seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

export default function QuizScreen({ session, context, onFinish, onRetry }) {
  const [currentQuestion, setCurrentQuestion] = useState(session.question);
  const [questionIndex, setQuestionIndex] = useState(session.question_index);
  const [totalQuestions, setTotalQuestions] = useState(session.total_questions);
  const [selectedOption, setSelectedOption] = useState(null);
  const [answerResult, setAnswerResult] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showTyping, setShowTyping] = useState(false);
  const [quizDone, setQuizDone] = useState(false);
  const [finalResult, setFinalResult] = useState(null);
  const [timer, setTimer] = useState(0);
  const [questionShownAt, setQuestionShownAt] = useState(new Date());
  const [, setScore] = useState(0);

  const timerRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    setQuestionShownAt(new Date());
    timerRef.current = setInterval(() => setTimer(t => t + 1), 1000);
    return () => clearInterval(timerRef.current);
  }, [currentQuestion]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [showFeedback, currentQuestion]);

  const handleOptionSelect = async (optionIdx) => {
    if (selectedOption !== null || isSubmitting) return;
    clearInterval(timerRef.current);

    const answeredAt = new Date();
    setSelectedOption(optionIdx);
    setIsSubmitting(true);

    try {
      const result = await submitAnswer({
        session_id: session.session_id,
        question_id: currentQuestion.id,
        selected_option: optionIdx,
        question_shown_at: questionShownAt.toISOString(),
        answer_submitted_at: answeredAt.toISOString(),
      });

      if (result.is_correct) {
        setScore(s => s + 1);
        toast.success('Correct! 🎉', { duration: 1500 });
      }

      setAnswerResult(result);
      setShowTyping(true);

      setTimeout(() => {
        setShowTyping(false);
        setShowFeedback(true);
      }, 1200);

    } catch (err) {
      console.error(err);
      toast.error('Error submitting answer');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNext = async () => {
    if (!answerResult) return;

    if (!answerResult.next_question) {
      // Quiz complete
      try {
        const result = await finishSession({ session_id: session.session_id });
        setFinalResult(result);
        setQuizDone(true);
      } catch (err) {
        console.error(err);
      }
      return;
    }

    setSelectedOption(null);
    setAnswerResult(null);
    setShowFeedback(false);
    setShowTyping(false);
    setCurrentQuestion(answerResult.next_question);
    setQuestionIndex(answerResult.question_index);
    setTotalQuestions(answerResult.total_questions);
    setTimer(0);
    setQuestionShownAt(new Date());
  };

  const progress = ((questionIndex) / totalQuestions) * 100;

  // ─── Results Screen ──────────────────────────────────────────────────────
  if (quizDone && finalResult) {
    const pct = finalResult.percentage;
    const emoji = pct >= 80 ? '🏆' : pct >= 60 ? '🎯' : pct >= 40 ? '📚' : '💪';
    const msg = pct >= 80 ? 'Excellent Work!' : pct >= 60 ? 'Great Job!' : pct >= 40 ? 'Keep Practicing!' : 'Never Give Up!';

    return (
      <div className="results-screen">
        <span className="results-emoji">{emoji}</span>
        <div
          className="score-circle"
          style={{ '--score-pct': pct }}
        >
          <div className="score-circle-inner">
            <span className="score-number">{pct}%</span>
            <span className="score-label">Score</span>
          </div>
        </div>
        <h2 className="results-title">{msg}</h2>
        <p className="results-subtitle">
          {context.exam?.name} · {context.subject?.name} · {context.chapter?.name}
        </p>

        <div className="results-stats">
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--wa-correct)' }}>
              {finalResult.score}
            </div>
            <div className="stat-name">Correct</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--wa-wrong)' }}>
              {finalResult.answered_questions - finalResult.score}
            </div>
            <div className="stat-name">Wrong</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{finalResult.answered_questions}</div>
            <div className="stat-name">Answered</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{finalResult.total_questions}</div>
            <div className="stat-name">Total</div>
          </div>
        </div>

        <button className="btn-primary" onClick={onRetry}>🔄 Try Again</button>
        <button className="btn-secondary" onClick={onFinish}>🏠 Back to Home</button>
      </div>
    );
  }

  // ─── Quiz Interface ──────────────────────────────────────────────────────
  return (
    <div className="quiz-screen">
      {/* Header */}
      <div className="quiz-header">
        <div className="quiz-meta">
          <div className="quiz-badge">
            <span>⚡</span>
            <span>{context.subject?.name}</span>
          </div>
          <div className="quiz-counter">
            {questionIndex + 1} / {totalQuestions}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: 'var(--wa-text-secondary)' }}>
            ⏱ {formatTime(timer)}
          </div>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
      </div>

      {/* Chat Bubble — Question */}
      <div className="chat-bubble-container">
        <div className="chat-avatar">🤖</div>
        <div className="chat-bubble">
          <div className="question-number">
            Question {questionIndex + 1}
          </div>
          <p className="question-text">{currentQuestion?.question_text}</p>
          <p className="chat-time">
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
      </div>

      {/* Options */}
      <div className="options-grid">
        {currentQuestion?.options?.map((opt, idx) => {
          let cls = 'option-btn';
          if (answerResult && selectedOption === idx) {
            cls += answerResult.is_correct ? ' selected-correct' : ' selected-wrong';
          } else if (answerResult && idx === answerResult.correct_option && !answerResult.is_correct) {
            cls += ' show-correct';
          }

          return (
            <button
              key={idx}
              className={cls}
              onClick={() => handleOptionSelect(idx)}
              disabled={selectedOption !== null}
            >
              <span className="option-label">{OPTION_LABELS[idx]}</span>
              <span className="option-text">{opt}</span>
              {answerResult && selectedOption === idx && (
                <span className="option-icon">
                  {answerResult.is_correct ? '✅' : '❌'}
                </span>
              )}
              {answerResult && idx === answerResult.correct_option && selectedOption !== idx && (
                <span className="option-icon">✅</span>
              )}
            </button>
          );
        })}
      </div>

      {/* Typing Indicator */}
      {showTyping && (
        <div className="typing-indicator">
          <div className="typing-dot" />
          <div className="typing-dot" />
          <div className="typing-dot" />
        </div>
      )}

      {/* Feedback Bubble */}
      {showFeedback && answerResult && (
        <div className="feedback-bubble">
          <span className="feedback-icon">
            {answerResult.is_correct ? '🎉' : '💡'}
          </span>
          <div className="feedback-text">
            <strong>{answerResult.is_correct ? 'Correct!' : 'Not quite!'}</strong>
            {answerResult.explanation || `The correct answer is option ${OPTION_LABELS[answerResult.correct_option]}.`}
          </div>
        </div>
      )}

      {/* Next Button */}
      {showFeedback && (
        <button className="next-btn" onClick={handleNext}>
          {!answerResult?.next_question ? '🏁 Finish Quiz' : 'Next Question ›'}
        </button>
      )}

      <div ref={chatEndRef} />
    </div>
  );
}
