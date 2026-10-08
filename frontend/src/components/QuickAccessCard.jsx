import React from 'react';

export default function QuickAccessCard({ title, extTag, countText, color, icon: Icon, onClick }) {
  const gradientMap = {
    '#2563EB': 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)',
    '#10B981': 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
    '#8B5CF6': 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)',
    '#F97316': 'linear-gradient(135deg, #F97316 0%, #EA580C 100%)'
  };

  const bg = gradientMap[color] || color;

  return (
    <div 
      className="glass-card" 
      onClick={onClick}
      style={{
        padding: '16px',
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        transition: 'all 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
      }}
    >
      <div style={{
        height: '46px',
        borderRadius: '12px',
        background: bg,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 14px',
        color: '#FFFFFF',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
      }}>
        <Icon size={20} />
        <span style={{ fontSize: '0.72rem', fontWeight: 800, letterSpacing: '0.06em' }}>{extTag}</span>
      </div>
      <div>
        <h4 style={{ fontSize: '0.98rem', fontWeight: 800, color: 'var(--text-primary)' }}>{title}</h4>
        <p style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)', marginTop: '2px' }}>{countText}</p>
      </div>
    </div>
  );
}
