import React, { useState, useEffect } from 'react';
import {
  getAnalyticsOverview,
  getDailyActiveUsers,
  getWeeklyActiveUsers,
  getQuestionsStats,
  getAvgResponseTime,
  getCompletionRate,
  getDropoffAnalysis,
  getPeakHours,
  getAvgQuestionsPerSession,
} from './api';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend, 
} from 'recharts';

const COLORS = ['#16a34a', '#0d9488', '#0284c7', '#d97706', '#dc2626', '#7c3aed'];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: '#ffffff', border: '1px solid #e2e8f0',
        borderRadius: 8, padding: '10px 14px', fontSize: 13,
        boxShadow: '0 4px 12px rgba(15, 23, 42, 0.05)',
      }}>
        <p style={{ color: '#64748b', marginBottom: 4, fontWeight: 500 }}>{label}</p>
        {payload.map((entry, i) => (
          <p key={i} style={{ color: entry.color || '#16a34a', fontWeight: 600 }}>
            {entry.name}: {typeof entry.value === 'number' ? entry.value.toLocaleString() : entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

function OverviewCard({ icon, value, label, accent = '#16a34a' }) {
  return (
    <div className="overview-card" style={{ '--accent': accent }}>
      <div className="ov-icon">{icon}</div>
      <div className="ov-value">{typeof value === 'number' ? value.toLocaleString() : value}</div>
      <div className="ov-label">{label}</div>
    </div>
  );
}

export default function AnalyticsDashboard() {
  const [overview, setOverview] = useState(null);
  const [dau, setDau] = useState([]);
  const [wau, setWau] = useState([]);
  const [qStats, setQStats] = useState(null);
  const [responseTime, setResponseTime] = useState(null);
  const [completion, setCompletion] = useState(null);
  const [dropoff, setDropoff] = useState([]);
  const [peakHours, setPeakHours] = useState([]);
  const [avgQ, setAvgQ] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [ov, d, w, q, rt, cr, drop, ph, aq] = await Promise.all([
          getAnalyticsOverview(),
          getDailyActiveUsers(),
          getWeeklyActiveUsers(),
          getQuestionsStats(),
          getAvgResponseTime(),
          getCompletionRate(),
          getDropoffAnalysis(),
          getPeakHours(),
          getAvgQuestionsPerSession(),
        ]);
        setOverview(ov);
        setDau(d);
        setWau(w);
        setQStats(q);
        setResponseTime(rt);
        setCompletion(cr);
        setDropoff(drop);
        setPeakHours(ph);
        setAvgQ(aq);
      } catch (err) {
        console.error('Analytics fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p className="loading-text">Loading analytics...</p>
      </div>
    );
  }

  const overviewCards = [
    { icon: '👥', value: overview?.total_users || 0, label: 'Total Users', accent: '#16a34a' },
    { icon: '📅', value: overview?.daily_active_users || 0, label: 'Daily Active Users', accent: '#0d9488' },
    { icon: '📆', value: overview?.weekly_active_users || 0, label: 'Weekly Active Users', accent: '#0284c7' },
    { icon: '❓', value: overview?.total_questions_served || 0, label: 'Questions Served', accent: '#d97706' },
    { icon: '✅', value: overview?.total_correct || 0, label: 'Correct Answers', accent: '#16a34a' },
    { icon: '🎯', value: `${overview?.accuracy_rate || 0}%`, label: 'Accuracy Rate', accent: '#7c3aed' },
    { icon: '🏁', value: `${overview?.completion_rate || 0}%`, label: 'Completion Rate', accent: '#dc2626' },
    { icon: '⏱', value: `${overview?.avg_response_time_seconds || 0}s`, label: 'Avg Response Time', accent: '#0284c7' },
  ];

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1 className="analytics-title">📊 Analytics Dashboard</h1>
        <p className="analytics-subtitle">Real-time insights into quiz performance and user behavior</p>
      </div>

      {/* Overview Stats */}
      <div className="stats-overview">
        {overviewCards.map((card, i) => (
          <OverviewCard key={i} {...card} />
        ))}
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">

        {/* Daily Active Users */}
        <div className="chart-card">
          <div className="chart-title">📅 Daily Active Users</div>
          <div className="chart-subtitle">Unique users per day (last 30 days)</div>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={dau}>
              <defs>
                <linearGradient id="dauGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#16a34a" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#16a34a" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} tickFormatter={v => v?.slice(5)} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="users" stroke="#16a34a" fill="url(#dauGrad)" strokeWidth={2.5} name="Users" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Weekly Active Users */}
        <div className="chart-card">
          <div className="chart-title">📆 Weekly Active Users</div>
          <div className="chart-subtitle">Unique users per week (last 8 weeks)</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={wau}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="week" tick={{ fill: '#64748b', fontSize: 11 }} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="users" fill="#0d9488" radius={[4, 4, 0, 0]} name="Users" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Questions Served vs Correct */}
        <div className="chart-card">
          <div className="chart-title">❓ Questions Served & Correct</div>
          <div className="chart-subtitle">Daily activity for last 14 days</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={qStats?.daily || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} tickFormatter={v => v?.slice(5)} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontSize: 12, color: '#64748b' }} />
              <Bar dataKey="served" fill="#0284c7" radius={[4, 4, 0, 0]} name="Served" />
              <Bar dataKey="correct" fill="#16a34a" radius={[4, 4, 0, 0]} name="Correct" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Average Response Time */}
        <div className="chart-card">
          <div className="chart-title">⏱ Avg Response Time</div>
          <div className="chart-subtitle">
            Overall: {responseTime?.overall_avg_seconds}s per question
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={responseTime?.daily || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} tickFormatter={v => v?.slice(5)} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} unit="s" />
              <Tooltip content={<CustomTooltip />} />
              <Line type="monotone" dataKey="avg_seconds" stroke="#d97706" strokeWidth={2.5} dot={false} name="Avg Seconds" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Quiz Completion Rate by Exam */}
        <div className="chart-card">
          <div className="chart-title">🏁 Completion Rate by Exam</div>
          <div className="chart-subtitle">Overall: {completion?.rate}% completion</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={completion?.by_exam || []} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} unit="%" domain={[0, 100]} />
              <YAxis type="category" dataKey="exam" tick={{ fill: '#64748b', fontSize: 11 }} width={70} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="rate" radius={[0, 4, 4, 0]} name="Completion %" >
                {(completion?.by_exam || []).map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Drop-off Analysis */}
        <div className="chart-card">
          <div className="chart-title">📉 Drop-off Analysis</div>
          <div className="chart-subtitle">Where users stop in quizzes</div>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={dropoff}
                dataKey="count"
                nameKey="range"
                cx="50%"
                cy="50%"
                outerRadius={80}
                paddingAngle={3}
                label={({ range, percent }) => `${range} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {dropoff.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontSize: 12, color: '#64748b' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Peak Activity Hours */}
        <div className="chart-card">
          <div className="chart-title">🕐 Peak Activity Hours</div>
          <div className="chart-subtitle">When users are most active (UTC)</div>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={peakHours}>
              <defs>
                <linearGradient id="peakGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#7c3aed" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#7c3aed" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="hour" tick={{ fill: '#64748b', fontSize: 11 }} tickFormatter={v => `${v}h`} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="count" stroke="#7c3aed" fill="url(#peakGrad)" strokeWidth={2.5} name="Activity" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Avg Questions Per Session */}
        <div className="chart-card">
          <div className="chart-title">📊 Avg Questions Per Session</div>
          <div className="chart-subtitle">
            Overall avg: {avgQ?.avg_questions} questions | Total sessions: {avgQ?.total_sessions}
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={avgQ?.by_exam || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="exam" tick={{ fill: '#64748b', fontSize: 10 }} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="avg" name="Avg Questions" radius={[4, 4, 0, 0]}>
                {(avgQ?.by_exam || []).map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

      </div>
    </div>
  );
}
