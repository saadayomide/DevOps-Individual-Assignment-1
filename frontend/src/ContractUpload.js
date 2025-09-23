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
      setDrafts(res.drafts || []);
      setError(null);
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed to parse file');
    } finally {
      setParsing(false);
    }
  };

  const fixCategory = (idx, categoryName) => {
    setDrafts(prev => prev.map((d, i) => i === idx ? { ...d, category_name: categoryName } : d));
  };

  const fixField = (idx, field, value) => {
    setDrafts(prev => prev.map((d, i) => i === idx ? { ...d, [field]: value } : d));
  };

  const createProposal = async (d) => {
    try {
      if (!d.valid) { return; }
      await proposalAPI.create({
        ministry: d.ministry,
        category_id: d.category_id,
        title: d.title,
        description: d.description || null,
        requested_amount: d.requested_amount
      });
      onCreated && onCreated();
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed to create proposal from draft');
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
                      disabled={!d.valid}
                      onClick={() => createProposal(d)}
                    >
                      Create Proposal
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className='form-actions' style={{ marginTop: 10 }}>
        <button className='btn btn-primary' onClick={async () => {
          for (const d of drafts) { if (d.valid) { try { await createProposal(d); } catch(e){} } }
        }}>Create All Valid</button>
      </div>
    </div>
  );
};

export default ContractUpload;
