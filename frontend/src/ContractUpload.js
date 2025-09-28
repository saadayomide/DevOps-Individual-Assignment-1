import React, { useState } from 'react';
import { uploadAPI, proposalAPI } from './api';

const ContractUpload = ({ onCreated }) => {
  const [file, setFile] = useState(null);
  const [drafts, setDrafts] = useState([]);
  const [error, setError] = useState(null);
  const [parsing, setParsing] = useState(false);

  const onSelect = (e) => {
    setFile(e.target.files[0] || null);
    setDrafts([]);
    setError(null);
  };

    const onParse = async () => {
    if (!file) { setError('Please choose a JSON or CSV file.'); return; }
    try {
      setParsing(true);
      const res = await uploadAPI.parse(file);
      
      // Get existing proposals to check for duplicates
      const existingProposals = await proposalAPI.getAll();
      
      // Initialize row-level flags and check for existing proposals
      const initializedDrafts = (res.drafts || []).map(d => {
        const isExisting = existingProposals.some(existing => 
          existing.ministry === d.ministry && 
          existing.title === d.title && 
          existing.requested_amount === d.requested_amount
        );
        
        return { 
          ...d, 
          isCreating: false, 
          isCreated: isExisting  // Mark as created if it already exists
        };
      });
      
      setDrafts(initializedDrafts);
      setError(null);
    } catch (e) {
      // Handle different error formats
      let errorMessage = 'Failed to parse file';
      
      if (e?.response?.data) {
        const errorData = e.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    } finally {
      setParsing(false);
    }
  };

  const createProposal = async (d, idx) => {
    try {
      if (!d.valid) { return; }
      // Guard: skip if already created or being created
      if (d.isCreating || d.isCreated) { return; }

      // Mark as creating
      setDrafts(prev => prev.map((x, i) => i === idx ? { ...x, isCreating: true } : x));

      await proposalAPI.create({
        ministry: d.ministry,
        category_id: d.category_id,
        title: d.title,
        description: d.description || null,
        requested_amount: d.requested_amount
      });

      // Mark as created
      setDrafts(prev => prev.map((x, i) => i === idx ? { ...x, isCreating: false, isCreated: true } : x));
      onCreated && onCreated();
    } catch (e) {
      // Reset creating flag on error
      setDrafts(prev => prev.map((x, i) => i === idx ? { ...x, isCreating: false } : x));

      // Handle different error formats
      let errorMessage = 'Failed to create proposal from draft';
      
      if (e?.response?.data) {
        const errorData = e.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  return (
    <div className="form-container" style={{ marginTop: 20 }}>
      <h3>Contract Upload</h3>
      {error && <div className="error">{error}</div>}
      <div className="form-group">
        <input type="file" accept=".json,.csv" onChange={onSelect} />
      </div>
      <div className="form-actions">
        <button className="btn btn-primary" onClick={onParse} disabled={parsing}>
          {parsing ? 'Parsing...' : 'Parse'}
        </button>
      </div>

      {drafts.length > 0 && (
        <div className="categories-table" style={{ marginTop: 20 }}>
          <h3>Parsed Drafts</h3>
          <table>
            <thead>
              <tr>
                <th>Valid</th>
                <th>Ministry</th>
                <th>Category</th>
                <th>Title</th>
                <th>Requested</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {drafts.map((d, i) => (
                <tr key={i}>
                  <td>{d.valid ? 'Yes' : 'No'}</td>
                  <td>{d.ministry || '-'}</td>
                  <td>{d.category_name || '-'}</td>
                  <td>{d.title || '-'}</td>
                  <td>{d.requested_amount != null ? new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(d.requested_amount) : '-'}</td>
                  <td>
                    <button
                      className="btn btn-small btn-primary"
                      disabled={!d.valid || d.isCreating || d.isCreated}
                      onClick={() => createProposal(d, i)}
                    >
                      {d.isCreated ? 'Created' : (d.isCreating ? 'Creating…' : 'Create Proposal')}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className='form-actions' style={{ marginTop: 10 }}>
        <button className="btn btn-secondary" onClick={() => { setDrafts([]); setFile(null); setError(null); }}>
          Clear All
        </button>
      </div>
    </div>
  );
};

export default ContractUpload;
