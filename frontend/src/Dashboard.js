import React, { useEffect, useState } from 'react';
import { Pie, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const API_BASE_URL = 'http://localhost:8000';

const Dashboard = ({ refreshKey }) => {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  const load = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/dashboard/summary`);
      const data = await res.json();
      setSummary(data);
      setError(null);
    } catch (e) {
      setError('Failed to load dashboard');
    }
  };

  useEffect(() => { load(); }, [refreshKey]);

  if (!summary) {
    return <div className="loading">Loading dashboard...</div>;
  }

  const categoryLabels = summary.categories.map(c => c.name);
  const allocated = summary.categories.map(c => c.allocated_budget);
  const remaining = summary.categories.map(c => c.remaining_budget);

  const ministries = summary.ministries.map(m => m.ministry);
  const requested = summary.ministries.map(m => m.requested_total);
  const approved = summary.ministries.map(m => m.approved_total);

  return (
    <div className="form-container" style={{ marginTop: 20 }}>
      <h3>Dashboard</h3>
      {error && <div className="error">{error}</div>}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <div className="categories-table">
          <h3>Allocated vs Remaining (Categories)</h3>
          <Bar
            data={{
              labels: categoryLabels,
              datasets: [
                { label: 'Allocated', data: allocated, backgroundColor: 'rgba(52, 152, 219, 0.6)' },
                { label: 'Remaining', data: remaining, backgroundColor: 'rgba(46, 204, 113, 0.6)' },
              ],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
            height={300}
          />
        </div>
        <div className="categories-table">
          <h3>Requested vs Approved (Ministries)</h3>
          <Bar
            data={{
              labels: ministries,
              datasets: [
                { label: 'Requested', data: requested, backgroundColor: 'rgba(241, 196, 15, 0.7)' },
                { label: 'Approved', data: approved, backgroundColor: 'rgba(39, 174, 96, 0.8)' },
              ],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
            height={300}
          />
        </div>
      </div>

      <div style={{ display: 'flex', gap: 20, marginTop: 20 }}>
        <div className="form-container" style={{ flex: 1 }}>
          <h4>Totals</h4>
          <p>Total Allocated: {summary.kpis.total_allocated.toLocaleString()}</p>
          <p>Total Approved: {summary.kpis.total_approved.toLocaleString()}</p>
          <p>Total Remaining: {summary.kpis.total_remaining.toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
