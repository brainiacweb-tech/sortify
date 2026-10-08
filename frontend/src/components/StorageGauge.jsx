import React from 'react';

export default function StorageGauge({ percentage = 78, totalSpace = "System Disk", usedSpace = "571 files sorted" }) {
  const radius = 64;
  const strokeWidth = 14;
  const normalizedRadius = radius - strokeWidth * 0.5;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h4 style={{ fontSize: '0.8rem', fontWeight: 800, letterSpacing: '0.06em', color: 'var(--text-muted)', alignSelf: 'flex-start', marginBottom: '16px', textTransform: 'uppercase' }}>
        Storage & Sorting Health
      </h4>

      {/* SVG Donut Ring */}
      <div style={{ position: 'relative', width: '160px', height: '160px', margin: '10px 0' }}>
        <svg height="160" width="160" style={{ transform: 'rotate(-90deg)' }}>
          {/* Background Track */}
          <circle
            stroke="var(--border-card)"
            fill="transparent"
            strokeWidth={strokeWidth}
            r={normalizedRadius}
            cx="80"
            cy="80"
          />
          {/* Progress Arc */}
          <circle
            stroke="url(#sortify-gradient)"
            fill="transparent"
            strokeWidth={strokeWidth}
            strokeDasharray={circumference + ' ' + circumference}
            style={{ strokeDashoffset, transition: 'stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1)' }}
            strokeLinecap="round"
            r={normalizedRadius}
            cx="80"
            cy="80"
          />
          <defs>
            <linearGradient id="sortify-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#2563EB" />
              <stop offset="60%" stopColor="#10B981" />
              <stop offset="100%" stopColor="#F97316" />
            </linearGradient>
          </defs>
        </svg>

        {/* Center Text */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <span style={{ fontSize: '1.9rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.03em' }}>{percentage}%</span>
          <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary-blue)' }}>Organized</span>
        </div>
      </div>

      {/* Metrics Row */}
      <div style={{ display: 'flex', width: '100%', justifyContent: 'space-between', marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--border-card)' }}>
        <div>
          <p style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)' }}>Target Storage</p>
          <p style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--text-primary)' }}>{totalSpace}</p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <p style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)' }}>Triage Status</p>
          <p style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--accent-emerald)' }}>{usedSpace}</p>
        </div>
      </div>
    </div>
  );
}
