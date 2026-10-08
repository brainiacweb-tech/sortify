import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon }) {
  return (
    <div className="glass-card" style={{
      padding: '16px 20px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      borderRadius: 'var(--rounded-sm)'
    }}>
      <div>
        <p style={{ fontFamily: 'var(--font-heading)', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
          {title}
        </p>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)', margin: '4px 0 0 0' }}>
          {value}
        </h3>
        {subtitle && (
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', fontWeight: 400, color: 'var(--text-secondary)', marginTop: '2px' }}>
            {subtitle}
          </p>
        )}
      </div>
      <div style={{
        width: '40px',
        height: '40px',
        borderRadius: 'var(--rounded-sm)',
        backgroundColor: 'rgb(217, 241, 225)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--colors-link)',
        flexShrink: 0
      }}>
        <Icon size={20} />
      </div>
    </div>
  );
}
