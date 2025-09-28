import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { dashboardAPI } from './api';

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const Dashboard = ({ refreshKey }) => {
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 3,
    layout: { padding: 0 },
    plugins: {
      legend: { 
        position: 'bottom', 
        labels: { 
          boxWidth: 12, 
          font: { size: 11, family: 'Inter' },
          padding: 15
        } 
      },
      tooltip: { 
        titleFont: { size: 12, family: 'Inter' }, 
        bodyFont: { size: 11, family: 'Inter' },
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        cornerRadius: 8
      }
    },
    scales: {
      x: { 
        ticks: { 
          font: { size: 10, family: 'Inter' },
          color: 'var(--color-text-secondary)'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      y: { 
        ticks: { 
          font: { size: 10, family: 'Inter' },
          color: 'var(--color-text-secondary)',
          callback: function(value) {
            return '$' + value.toLocaleString();
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      }
    }
  };
  
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await dashboardAPI.getSummary();
      setSummary(data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [refreshKey]);

  if (loading) {
    return (
      <div className="card dashboard-card">
        <div className="card-header">
          <h2>📊 Dashboard</h2>
          <p>Financial overview and analytics</p>
        </div>
        <div className="loading">
          <div className="loading-spinner"></div>
          <span>Loading dashboard data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card dashboard-card">
        <div className="card-header">
          <h2>📊 Dashboard</h2>
          <p>Financial overview and analytics</p>
        </div>
        <div className="error-message">
          <span>⚠️</span> {error}
        </div>
        <button className="btn btn-primary" onClick={load}>
          <span>🔄</span>
          Retry
        </button>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="card dashboard-card">
        <div className="card-header">
          <h2>📊 Dashboard</h2>
          <p>Financial overview and analytics</p>
        </div>
        <div className="error-message">
          <span>📭</span> No data available
        </div>
      </div>
    );
  }

  // Category budget chart
  const categoryChartData = {
    labels: summary.categories.map(c => c.name),
    datasets: [
      {
        label: 'Allocated Budget',
        data: summary.categories.map(c => c.allocated_budget),
        backgroundColor: 'rgba(37, 99, 235, 0.8)',
        borderColor: 'rgba(37, 99, 235, 1)',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      },
      {
        label: 'Remaining Budget',
        data: summary.categories.map(c => c.remaining_budget),
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      }
    ]
  };

  // Ministry spending chart
  const ministryChartData = {
    labels: summary.ministries.map(m => m.ministry),
    datasets: [
      {
        label: 'Requested Amount',
        data: summary.ministries.map(m => m.requested_total),
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      },
      {
        label: 'Approved Amount',
        data: summary.ministries.map(m => m.approved_total),
        backgroundColor: 'rgba(124, 58, 237, 0.8)',
        borderColor: 'rgba(124, 58, 237, 1)',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      }
    ]
  };

  return (
    <div className="card dashboard-card">
      <div className="card-header">
        <h2>📊 Dashboard</h2>
        <p>Financial overview and analytics</p>
      </div>
      
      {/* KPI Summary */}
      <div className="kpi-summary">
        <div className="kpi-item">
          <div className="kpi-icon">💰</div>
          <h3>Total Allocated</h3>
          <p>${summary.kpis.total_allocated.toLocaleString()}</p>
        </div>
        <div className="kpi-item">
          <div className="kpi-icon">💳</div>
          <h3>Total Remaining</h3>
          <p>${summary.kpis.total_remaining.toLocaleString()}</p>
        </div>
        <div className="kpi-item">
          <div className="kpi-icon">✅</div>
          <h3>Total Approved</h3>
          <p>${summary.kpis.total_approved.toLocaleString()}</p>
        </div>
        <div className="kpi-item">
          <div className="kpi-icon">📈</div>
          <h3>Utilization Rate</h3>
          <p>{((summary.kpis.total_allocated - summary.kpis.total_remaining) / summary.kpis.total_allocated * 100).toFixed(1)}%</p>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="chart-section">
          <div className="chart-header">
            <h3>📊 Budget by Category</h3>
            <p>Allocated vs Remaining Budget</p>
          </div>
          <div className="chart-container">
            <Bar data={categoryChartData} options={chartOptions} />
          </div>
        </div>
        
        <div className="chart-section">
          <div className="chart-header">
            <h3>🏢 Spending by Ministry</h3>
            <p>Requested vs Approved Amounts</p>
          </div>
          <div className="chart-container">
            <Bar data={ministryChartData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
