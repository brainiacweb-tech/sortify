import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  FolderTree, 
  Copy, 
  History, 
  Sliders, 
  Settings, 
  Info, 
  Edit3,
  HelpCircle,
  HardDrive,
  PieChart,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import logoImg from '../assets/logo.png';

export default function Sidebar({ activeTab, setActiveTab, onShowAbout, userInfo }) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const name = userInfo?.name || 'Local User';
  const initials = userInfo?.initials || 'LU';

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, color: '#13C56B' },
    { id: 'organize', label: 'Organize Files', icon: FolderTree, color: '#3B82F6' },
    { id: 'files', label: 'Files Manager', icon: HardDrive, color: '#10B981' },
    { id: 'duplicates', label: 'Duplicates', icon: Copy, color: '#F59E0B' },
    { id: 'storage', label: 'Storage Analytics', icon: PieChart, color: '#6366F1' },
    { id: 'history', label: 'History & Undo', icon: History, color: '#8B5CF6' },
    { id: 'rules', label: 'File Rules', icon: Sliders, color: '#10B981' },
    { id: 'rename', label: 'Rename Files', icon: Edit3, color: '#EC4899' },
    { id: 'guide', label: 'User Guide', icon: HelpCircle, color: '#007427' },
    { id: 'settings', label: 'Settings', icon: Settings, color: '#6B7280' },
  ];

  return (
    <aside style={{
      width: isCollapsed ? '72px' : '230px',
      backgroundColor: 'var(--bg-sidebar)',
      borderRight: '1px solid var(--border-card)',
      display: 'flex',
      flexDirection: 'column',
      justify: 'space-between',
      padding: isCollapsed ? '20px 0 20px 8px' : '20px 0 20px 14px',
      height: '100vh',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      transition: 'all 0.22s cubic-bezier(0.16, 1, 0.3, 1)'
    }}>
      <div>
        {/* Brand Header & Toggle */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: isCollapsed ? 'center' : 'space-between',
          marginBottom: '28px',
          paddingRight: isCollapsed ? '8px' : '14px'
        }}>
          {!isCollapsed ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{
                padding: '6px 12px',
                borderRadius: 'var(--rounded-sm)',
                backgroundColor: 'var(--colors-primary)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 2px 8px rgba(19, 197, 107, 0.25)'
              }}>
                <img 
                  src={logoImg} 
                  alt="Sortify" 
                  style={{ height: '22px', objectFit: 'contain' }} 
                />
              </div>
            </div>
          ) : (
            <div style={{
              width: '38px',
              height: '38px',
              borderRadius: '50%',
              backgroundColor: 'var(--colors-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 2px 8px rgba(19, 197, 107, 0.3)'
            }} title="Sortify">
              <FolderTree size={20} color="#FFFFFF" />
            </div>
          )}

          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            style={{
              border: 'none',
              background: 'transparent',
              cursor: 'pointer',
              color: 'var(--text-muted)',
              padding: '6px',
              borderRadius: 'var(--rounded-sm)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
            title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
          >
            {isCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
          </button>
        </div>

        {/* Navigation Rail with Organic Curved Cutouts */}
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                title={isCollapsed ? item.label : ''}
                className={`curved-nav-item ${isActive ? 'active' : ''}`}
                style={{
                  padding: isCollapsed ? '8px 0 8px 10px' : '8px 12px',
                  justifyContent: isCollapsed ? 'flex-start' : 'flex-start',
                  gap: '12px'
                }}
              >
                {/* Floating Colored Circle Icon Badge */}
                <div style={{
                  width: '38px',
                  height: '38px',
                  borderRadius: '50%',
                  backgroundColor: isActive ? item.color : 'transparent',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: isActive ? '#FFFFFF' : 'var(--text-muted)',
                  boxShadow: isActive ? `0 4px 12px ${item.color}40` : 'none',
                  transition: 'all 0.2s ease',
                  flexShrink: 0
                }}>
                  <Icon size={19} color={isActive ? '#FFFFFF' : 'var(--text-muted)'} />
                </div>

                {!isCollapsed && (
                  <span style={{
                    fontFamily: 'var(--font-heading)',
                    fontSize: '12px',
                    fontWeight: isActive ? 700 : 600,
                    letterSpacing: '0.04em',
                    textTransform: 'uppercase',
                    color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)'
                  }}>
                    {item.label}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Profile / User Card */}
      <div style={{ paddingRight: isCollapsed ? '8px' : '14px' }}>
        <div 
          onClick={onShowAbout}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            padding: isCollapsed ? '8px' : '10px 12px',
            borderRadius: 'var(--rounded-sm)',
            border: '1px solid var(--border-card)',
            backgroundColor: 'var(--bg-card)',
            cursor: 'pointer',
            justifyContent: isCollapsed ? 'center' : 'flex-start'
          }}
          title="About Sortify"
        >
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            backgroundColor: 'var(--colors-primary)',
            color: '#FFFFFF',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '12px',
            fontWeight: 700,
            fontFamily: 'var(--font-heading)',
            flexShrink: 0
          }}>
            {initials}
          </div>

          {!isCollapsed && (
            <div style={{ overflow: 'hidden', whiteSpace: 'nowrap' }}>
              <p style={{ fontFamily: 'var(--font-heading)', fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)' }}>{name}</p>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '11px', color: 'var(--colors-link)', fontWeight: 500 }}>SORTIFY v1.0.2</p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
