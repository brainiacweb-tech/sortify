import React from 'react';
import { Search, User, Moon, Sun, Upload } from 'lucide-react';

export default function Header({ searchQuery, setSearchQuery, theme, toggleTheme, onFileUploadClick, userInfo }) {
  const name = userInfo?.name || 'Local User';
  const initials = userInfo?.initials || 'LU';

  return (
    <header style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: '20px',
      marginBottom: '24px'
    }}>
      {/* Search Bar Input */}
      <div style={{ position: 'relative', flex: 1, maxWidth: '480px' }}>
        <Search 
          size={16} 
          color="var(--text-muted)" 
          style={{ position: 'absolute', left: '14.4px', top: '50%', transform: 'translateY(-50%)' }} 
        />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search files or rules..."
          style={{
            width: '100%',
            height: '37.8px',
            padding: '8px 14.4px 8px 40px',
            borderRadius: 'var(--rounded-sm)',
            border: '1px solid var(--border-card)',
            backgroundColor: 'var(--bg-card)',
            color: 'var(--text-primary)',
            fontFamily: 'var(--font-body)',
            fontSize: '13.2px',
            outline: 'none',
            boxShadow: 'var(--card-shadow)'
          }}
        />
      </div>

      {/* Right Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button className="btn-primary" onClick={onFileUploadClick}>
          <Upload size={16} />
          <span>Upload Files</span>
        </button>

        <button
          onClick={toggleTheme}
          style={{
            width: '38.5px',
            height: '37.8px',
            borderRadius: 'var(--rounded-sm)',
            border: '1px solid var(--border-card)',
            backgroundColor: 'var(--bg-card)',
            color: 'var(--text-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer'
          }}
          title="Toggle Theme"
        >
          {theme === 'dark' ? <Sun size={18} color="#F59E0B" /> : <Moon size={18} color="var(--colors-primary)" />}
        </button>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '4px 10px',
          borderRadius: 'var(--rounded-sm)',
          border: '1px solid var(--border-card)',
          backgroundColor: 'var(--bg-card)',
          boxShadow: 'var(--card-shadow)'
        }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: 'var(--rounded-sm)',
            backgroundColor: 'var(--colors-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFFFFF',
            fontFamily: 'var(--font-body)',
            fontWeight: 500,
            fontSize: '12px'
          }}>
            {initials}
          </div>
          <span style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', fontWeight: 500, color: 'var(--text-primary)' }}>{name}</span>
        </div>
      </div>
    </header>
  );
}
