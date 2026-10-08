import React, { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import confetti from 'canvas-confetti';

const API_BASE = 'http://127.0.0.1:5000/api';

export default function RulesView() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newCatName, setNewCatName] = useState('');
  const [newCatExts, setNewCatExts] = useState('');

  const fetchRules = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/rules`);
      const data = await res.json();
      setLoading(false);
      if (Array.isArray(data)) setCategories(data);
    } catch (err) {
      setLoading(false);
      console.error(err);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const handleAddRule = async () => {
    if (!newCatName || !newCatExts) return;
    const exts = newCatExts.split(',').map(e => e.trim().startsWith('.') ? e.trim() : `.${e.trim()}`);

    try {
      const res = await fetch(`${API_BASE}/rules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category: newCatName, extensions: exts })
      });
      const data = await res.json();
      if (res.ok) {
        confetti({ particleCount: 50, spread: 50 });
        setCategories(data);
        setNewCatName('');
        setNewCatExts('');
      } else {
        alert('Error: ' + (data.error || 'Failed to add rule'));
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
          File Rules
        </h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Customize how files are grouped into folders based on file extensions.
        </p>
      </div>

      {/* Add Rule Form */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)' }}>Add New Folder Rule</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 100px', gap: '12px' }}>
          <input
            type="text"
            placeholder="Folder Name (e.g. Code)"
            value={newCatName}
            onChange={(e) => setNewCatName(e.target.value)}
            style={{ padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', color: 'var(--text-primary)', outline: 'none' }}
          />
          <input
            type="text"
            placeholder="File types (e.g. .js, .py, .html)"
            value={newCatExts}
            onChange={(e) => setNewCatExts(e.target.value)}
            style={{ padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', color: 'var(--text-primary)', outline: 'none' }}
          />
          <button className="btn-primary" onClick={handleAddRule}>
            <Plus size={16} />
            <span>Add</span>
          </button>
        </div>
      </div>

      {/* Rules Grid */}
      {loading ? (
        <div style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading rules...</div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
          {categories.map((cat, idx) => (
            <div key={idx} className="glass-card" style={{ padding: '18px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <h4 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--text-primary)' }}>{cat.name}</h4>
                <span className="badge" style={{ backgroundColor: 'var(--primary-blue-light)', color: 'var(--primary-blue)' }}>
                  Folder: {cat.folder}
                </span>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {cat.extensions && cat.extensions.map((ext, i) => (
                  <span key={i} style={{ padding: '3px 9px', borderRadius: '6px', backgroundColor: 'var(--bg-card-hover)', border: '1px solid var(--border-card)', fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                    {ext}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
