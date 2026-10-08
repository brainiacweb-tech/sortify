import React, { useState, useEffect } from 'react';
import { Settings, Moon, Sun, Monitor, AlertTriangle, User, Check } from 'lucide-react';

export default function SettingsView({ theme, setTheme, userInfo, setUserInfo }) {
  const [editingName, setEditingName] = useState(userInfo?.name || '');
  const [savedMsg, setSavedMsg] = useState(false);

  useEffect(() => {
    if (userInfo?.name) {
      setEditingName(userInfo.name);
    }
  }, [userInfo]);

  const handleSaveName = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/user-info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: editingName })
      });
      const data = await res.json();
      if (data && data.name) {
        if (setUserInfo) setUserInfo(data);
        setSavedMsg(true);
        setTimeout(() => setSavedMsg(false), 2500);
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
          Settings
        </h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Manage user profile, app theme, and organizing preferences.
        </p>
      </div>

      {/* User Profile Info Box */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <User size={18} color="var(--colors-primary)" />
          <span>User Profile Name</span>
        </h3>
        <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '16px' }}>
          Sortify automatically detects your Windows OS account name (no sign-up required). You can also edit it here anytime.
        </p>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center', maxWidth: '480px' }}>
          <input 
            type="text"
            value={editingName}
            onChange={(e) => setEditingName(e.target.value)}
            placeholder="Your Name..."
            style={{
              flex: 1,
              height: '38px',
              padding: '8px 12px',
              borderRadius: 'var(--rounded-sm)',
              border: '1px solid var(--border-card)',
              backgroundColor: 'var(--bg-dark)',
              color: 'var(--text-primary)',
              fontSize: '13.2px',
              outline: 'none'
            }}
          />
          <button className="btn-primary" onClick={handleSaveName}>
            {savedMsg ? <Check size={16} /> : null}
            <span>{savedMsg ? 'Saved!' : 'Save Name'}</span>
          </button>
        </div>
      </div>

      {/* Theme Selection Box */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '16px' }}>
          Appearance Theme
        </h3>
        <div style={{ display: 'flex', gap: '16px' }}>
          {[
            { id: 'light', label: 'Light Theme', icon: Sun },
            { id: 'dark', label: 'Dark Theme', icon: Moon },
            { id: 'system', label: 'System Default', icon: Monitor }
          ].map((t) => {
            const Icon = t.icon;
            const isSelected = theme === t.id;
            return (
              <button
                key={t.id}
                onClick={() => setTheme(t.id)}
                style={{
                  flex: 1,
                  padding: '14px',
                  borderRadius: '12px',
                  border: isSelected ? '2px solid var(--colors-primary)' : '1px solid var(--border-card)',
                  backgroundColor: isSelected ? 'var(--bg-card-hover)' : 'var(--bg-dark)',
                  color: isSelected ? 'var(--colors-link)' : 'var(--text-primary)',
                  fontWeight: 700,
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px'
                }}
              >
                <Icon size={18} />
                <span>{t.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Options Box */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)' }}>Organizing Options</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: 'var(--text-primary)', cursor: 'pointer' }}>
            <input type="checkbox" defaultChecked style={{ accentColor: 'var(--colors-primary)' }} />
            <span>Put unknown file types in an "Others" folder</span>
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: 'var(--text-primary)', cursor: 'pointer' }}>
            <input type="checkbox" defaultChecked style={{ accentColor: 'var(--colors-primary)' }} />
            <span>Show preview confirmation before moving files</span>
          </label>
        </div>
      </div>

      {/* Reset Box */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <button className="btn-secondary" style={{ color: '#DC2626', borderColor: '#DC2626' }} onClick={() => alert('Settings reset to defaults')}>
          <AlertTriangle size={16} />
          <span>Reset All Settings</span>
        </button>
      </div>
    </div>
  );
}
