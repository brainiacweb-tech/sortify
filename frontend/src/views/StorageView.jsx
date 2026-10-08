import React, { useState, useEffect } from 'react';
import { HardDrive, PieChart, FileText, Trash2, ArrowRight, AlertTriangle, ShieldCheck, Folder } from 'lucide-react';

export default function StorageView({ targetFolder }) {
  const [folder, setFolder] = useState(targetFolder || 'C:/Users/USER/Downloads');
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAnalytics(folder);
  }, [folder]);

  const loadAnalytics = async (dir) => {
    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:5000/api/storage/analytics?folder=${encodeURIComponent(dir)}`);
      const data = await res.json();
      if (data) {
        setAnalytics(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleRecycleFile = async (path) => {
    if (!window.confirm("Move this large file to Windows Recycle Bin?")) return;
    try {
      const res = await fetch('http://127.0.0.1:5000/api/files/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'recycle', paths: [path] })
      });
      const data = await res.json();
      if (data.count) {
        loadAnalytics(folder);
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
          Storage Analytics & Large Files
        </h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Analyze disk consumption, identify top space-hogging files, and reclaim wasted hard drive storage.
        </p>
      </div>

      {/* Overview Cards Row */}
      {analytics && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          <div className="glass-card" style={{ padding: '20px' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>TOTAL STORAGE USED</span>
            <p style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '4px' }}>{analytics.total_size}</p>
            <span style={{ fontSize: '11px', color: 'var(--colors-link)' }}>{analytics.total_files} files scanned</span>
          </div>

          <div className="glass-card" style={{ padding: '20px' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>CATEGORIES ANALYZED</span>
            <p style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--colors-primary)', marginTop: '4px' }}>{analytics.categories?.length || 0}</p>
            <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Extension breakdown</span>
          </div>
        </div>
      )}

      {/* Category Disk Space Distribution */}
      {analytics && analytics.categories && (
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <PieChart size={18} color="var(--colors-primary)" />
            <span>Disk Space Breakdown by Category</span>
          </h3>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '12px' }}>
            {analytics.categories.map((cat, idx) => (
              <div key={idx} style={{ padding: '12px 14px', borderRadius: '4px', backgroundColor: 'var(--bg-dark)', border: '1px solid var(--border-card)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--text-primary)', textTransform: 'capitalize' }}>{cat.category}</span>
                  <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{cat.count} items</p>
                </div>
                <span style={{ fontSize: '13px', fontWeight: 800, color: 'var(--colors-link)' }}>{cat.size}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Top 25 Largest Files Table */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <HardDrive size={18} color="var(--colors-primary)" />
          <span>Top 25 Largest Files</span>
        </h3>

        {loading ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>Scanning large files...</p>
        ) : !analytics || !analytics.top_largest_files || analytics.top_largest_files.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>No large files detected in this folder.</p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-card)', fontSize: '12px', color: 'var(--text-secondary)' }}>
                  <th style={{ padding: '10px 12px' }}>File Name</th>
                  <th style={{ padding: '10px 12px' }}>Category</th>
                  <th style={{ padding: '10px 12px' }}>Size</th>
                  <th style={{ padding: '10px 12px', textAlign: 'right' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {analytics.top_largest_files.map((f, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid var(--border-card)' }}>
                    <td style={{ padding: '10px 12px', fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)' }}>{f.name}</td>
                    <td style={{ padding: '10px 12px' }}>
                      <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--colors-link)', backgroundColor: '#F3FFF7', padding: '2px 6px', borderRadius: '3px' }}>
                        {f.category}
                      </span>
                    </td>
                    <td style={{ padding: '10px 12px', fontSize: '13px', fontWeight: 800, color: '#DC2626' }}>{f.size}</td>
                    <td style={{ padding: '10px 12px', textAlign: 'right' }}>
                      <button className="btn-secondary" style={{ padding: '4px 8px', fontSize: '11px', color: '#DC2626' }} onClick={() => handleRecycleFile(f.path)}>
                        <Trash2 size={13} /> Recycle
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
