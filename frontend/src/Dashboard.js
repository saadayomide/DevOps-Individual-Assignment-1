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
          <h2 className="page-title">Dashboard</h2>
          <p className="page-description">Financial overview and analytics</p>
        </div>
        <div className="loading-container">
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
          <h2 className="page-title">Dashboard</h2>
          <p className="page-description">Financial overview and analytics</p>
        </div>
        <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '12px' }}>
          {error}
        </div>
        <button className="btn btn-primary" onClick={load}>
          Retry
        </button>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="card dashboard-card">
        <div className="card-header">
          <h2 className="page-title">Dashboard</h2>
          <p className="page-description">Financial overview and analytics</p>
        </div>
        <div className="loading-container">
          <span>No data available</span>
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
    labels: summary.ministries.map(m => m.ministry_name || 'Unknown'),
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
        <h2 className="page-title">Dashboard</h2>
        <p className="page-description">Financial overview and analytics</p>
      </div>
      
      {/* KPI Summary */}
      <div className="kpi-summary" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        <div className="kpi-item" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Allocated</h3>
          <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>${summary.kpis.total_allocated.toLocaleString()}</p>
        </div>
        <div className="kpi-item" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Remaining</h3>
          <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>${summary.kpis.total_remaining.toLocaleString()}</p>
        </div>
        <div className="kpi-item" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Approved</h3>
          <p>${summary.kpis.total_approved.toLocaleString()}</p>
        </div>
        <div className="kpi-item" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Utilization Rate</h3>
          <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>{((summary.kpis.total_allocated - summary.kpis.total_remaining) / summary.kpis.total_allocated * 100).toFixed(1)}%</p>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="chart-section">
          <div className="chart-header">
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '4px', color: 'var(--color-text)' }}>Budget by Category</h3>
            <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: 0 }}>Allocated vs Remaining Budget</p>
          </div>
          <div className="chart-container">
            <Bar data={categoryChartData} options={chartOptions} />
          </div>
        </div>
        
        <div className="chart-section">
          <div className="chart-header">
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '4px', color: 'var(--color-text)' }}>Spending by Ministry</h3>
            <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: 0 }}>Requested vs Approved Amounts</p>
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
