import React, { useState, useEffect } from 'react';
import { RotateCcw, CheckCircle, AlertCircle } from 'lucide-react';
import confetti from 'canvas-confetti';

const API_BASE = 'http://127.0.0.1:5000/api';

export default function HistoryView() {
  const [historyBatches, setHistoryBatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isUndoing, setIsUndoing] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/history`);
      const data = await res.json();
      setLoading(false);
      if (Array.isArray(data)) setHistoryBatches(data);
    } catch (err) {
      setLoading(false);
      console.error(err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleUndoBatch = async (batchId) => {
    if (isUndoing) return;
    setIsUndoing(batchId);

    try {
      const res = await fetch(`${API_BASE}/undo`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ batch_id: batchId })
      });
      const data = await res.json();
      setIsUndoing(null);

      if (res.ok) {
        confetti({ particleCount: 70, spread: 60 });
        alert(`Undone! Restored ${data.restored_count} files back to their original folders.`);
        fetchHistory();
      } else {
        alert('Error: ' + (data.error || 'Could not restore files.'));
      }
    } catch (err) {
      setIsUndoing(null);
      alert('Error: ' + err.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
          History & Undo
        </h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Review past organized folders and undo changes with 1 click.
        </p>
      </div>

      {loading ? (
        <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading history...</div>
      ) : historyBatches.length === 0 ? (
        <div className="glass-card" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
          <AlertCircle size={32} style={{ marginBottom: '8px' }} />
          <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)' }}>No Organized Folders Yet</h4>
          <p style={{ fontSize: '0.85rem', marginTop: '4px' }}>When you organize folders, they will appear here so you can undo anytime.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {historyBatches.map((batch) => (
            <div key={batch.id} className="glass-card" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', borderBottom: '1px solid var(--border-card)', paddingBottom: '10px' }}>
                <div>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    Organized on {batch.timestamp}
                  </h3>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {batch.total_moves} files moved
                  </p>
                </div>
                <button 
                  className="btn-secondary"
                  onClick={() => handleUndoBatch(batch.id)}
                  disabled={isUndoing === batch.id}
                  style={{ borderColor: 'var(--accent-amber)', color: 'var(--accent-amber)' }}
                >
                  <RotateCcw size={15} />
                  <span>{isUndoing === batch.id ? 'Restoring...' : 'Undo This Action'}</span>
                </button>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {batch.moves && batch.moves.map((move, idx) => {
                  const srcName = move.source ? move.source.split('\\').pop().split('/').pop() : 'File';
                  const restored = move.restored;

                  return (
                    <div key={idx} style={{ fontSize: '0.85rem', color: restored ? 'var(--text-muted)' : 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <CheckCircle size={14} color={restored ? 'var(--text-muted)' : 'var(--accent-emerald)'} />
                      <span style={{ textDecoration: restored ? 'line-through' : 'none' }}>
                        {srcName} → {move.original_category || 'Folder'}
                      </span>
                      {restored && <span className="badge" style={{ backgroundColor: 'var(--border-card)', color: 'var(--text-muted)' }}>Restored</span>}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
