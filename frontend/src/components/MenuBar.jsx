import React, { useState, useEffect, useRef } from 'react';
import { 
  Folder, 
  Upload, 
  XSquare, 
  Play, 
  RotateCcw, 
  Copy, 
  Edit3, 
  Sliders, 
  LayoutDashboard, 
  Sun, 
  Moon, 
  Maximize, 
  HelpCircle, 
  Info 
} from 'lucide-react';

export default function MenuBar({ 
  setActiveTab, 
  onSelectFolder, 
  onUploadClick, 
  toggleTheme, 
  theme, 
  onShowAbout 
}) {
  const [openMenu, setOpenMenu] = useState(null);
  const menuRef = useRef(null);

  // Close open dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpenMenu(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleMenuClick = (menuName) => {
    setOpenMenu(openMenu === menuName ? null : menuName);
  };

  const handleAction = (action) => {
    setOpenMenu(null);
    action();
  };

  const handleToggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  };

  const handleExitApp = () => {
    if (window.pywebview && window.pywebview.api && window.pywebview.api.close) {
      window.pywebview.api.close();
    } else {
      if (window.confirm("Exit SORTIFY Application?")) {
        window.close();
      }
    }
  };

  const menuStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    backgroundColor: 'var(--bg-card)',
    borderBottom: '1px solid var(--border-card)',
    padding: '4px 16px',
    fontSize: '13.2px',
    fontFamily: 'var(--font-body)',
    color: 'var(--text-primary)',
    userSelect: 'none',
    position: 'relative',
    zIndex: 900
  };

  const itemStyle = (isOpen) => ({
    padding: '4px 10px',
    borderRadius: 'var(--rounded-sm)',
    cursor: 'pointer',
    backgroundColor: isOpen ? 'rgb(217, 241, 225)' : 'transparent',
    color: isOpen ? 'var(--colors-link)' : 'var(--text-primary)',
    fontWeight: isOpen ? 600 : 400,
    transition: 'all 0.15s ease'
  });

  const dropdownStyle = {
    position: 'absolute',
    top: '100%',
    left: 0,
    marginTop: '2px',
    minWidth: '220px',
    backgroundColor: 'var(--bg-card)',
    border: '1px solid var(--border-card)',
    borderRadius: 'var(--rounded-sm)',
    boxShadow: 'var(--card-shadow)',
    padding: '4px 0',
    display: 'flex',
    flexDirection: 'column',
    zIndex: 1000
  };

  const optionStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '8px 14px',
    fontSize: '13.2px',
    fontFamily: 'var(--font-body)',
    color: 'var(--text-primary)',
    cursor: 'pointer',
    backgroundColor: 'transparent',
    transition: 'background-color 0.12s ease'
  };

  return (
    <div style={menuStyle} ref={menuRef}>
      {/* FILE MENU */}
      <div style={{ position: 'relative' }}>
        <div 
          style={itemStyle(openMenu === 'file')} 
          onClick={() => handleMenuClick('file')}
          onMouseEnter={() => openMenu && setOpenMenu('file')}
        >
          File
        </div>
        {openMenu === 'file' && (
          <div style={dropdownStyle}>
            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => onSelectFolder && onSelectFolder())}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Folder size={15} color="var(--colors-link)" /> Select Folder...
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Ctrl+O</span>
            </div>

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => onUploadClick && onUploadClick())}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Upload size={15} color="var(--colors-link)" /> Upload Files...
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Ctrl+U</span>
            </div>

            <div style={{ borderBottom: '1px solid var(--border-card)', margin: '4px 0' }} />

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(handleExitApp)}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#EF4444' }}>
                <XSquare size={15} /> Exit
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Alt+F4</span>
            </div>
          </div>
        )}
      </div>

      {/* ORGANIZE MENU */}
      <div style={{ position: 'relative' }}>
        <div 
          style={itemStyle(openMenu === 'organize')} 
          onClick={() => handleMenuClick('organize')}
          onMouseEnter={() => openMenu && setOpenMenu('organize')}
        >
          Organize
        </div>
        {openMenu === 'organize' && (
          <div style={dropdownStyle}>
            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => setActiveTab('organize'))}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Play size={15} color="var(--colors-link)" /> Organize Files View
              </span>
            </div>

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => setActiveTab('history'))}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <RotateCcw size={15} color="var(--colors-link)" /> History & Undo Batch
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Ctrl+Z</span>
            </div>
          </div>
        )}
      </div>

      {/* TOOLS MENU */}
      <div style={{ position: 'relative' }}>
        <div 
          style={itemStyle(openMenu === 'tools')} 
          onClick={() => handleMenuClick('tools')}
          onMouseEnter={() => openMenu && setOpenMenu('tools')}
        >
          Tools
        </div>
        {openMenu === 'tools' && (
          <div style={dropdownStyle}>
            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => setActiveTab('duplicates'))}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Copy size={15} color="var(--colors-link)" /> Find Duplicates
              </span>
            </div>

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => setActiveTab('rename'))}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Edit3 size={15} color="var(--colors-link)" /> Bulk File Rename
              </span>
            </div>

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => setActiveTab('rules'))}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Sliders size={15} color="var(--colors-link)" /> Custom Category Rules
              </span>
            </div>
          </div>
        )}
      </div>

      {/* VIEW MENU */}
      <div style={{ position: 'relative' }}>
        <div 
          style={itemStyle(openMenu === 'view')} 
          onClick={() => handleMenuClick('view')}
          onMouseEnter={() => openMenu && setOpenMenu('view')}
        >
          View
        </div>
        {openMenu === 'view' && (
          <div style={dropdownStyle}>
            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => setActiveTab('dashboard'))}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <LayoutDashboard size={15} color="var(--colors-link)" /> Dashboard
              </span>
            </div>

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => toggleTheme && toggleTheme())}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                {theme === 'dark' ? <Sun size={15} color="#F59E0B" /> : <Moon size={15} color="var(--colors-link)" />} 
                Toggle {theme === 'dark' ? 'Light' : 'Dark'} Theme
              </span>
            </div>

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(handleToggleFullscreen)}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Maximize size={15} color="var(--colors-link)" /> Fullscreen
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>F11</span>
            </div>
          </div>
        )}
      </div>

      {/* HELP MENU */}
      <div style={{ position: 'relative' }}>
        <div 
          style={itemStyle(openMenu === 'help')} 
          onClick={() => handleMenuClick('help')}
          onMouseEnter={() => openMenu && setOpenMenu('help')}
        >
          Help
        </div>
        {openMenu === 'help' && (
          <div style={dropdownStyle}>
            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => setActiveTab('guide'))}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <HelpCircle size={15} color="var(--colors-link)" /> User Guidelines & How to Use
              </span>
            </div>

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => setActiveTab('settings'))}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Sliders size={15} color="var(--colors-link)" /> User Preferences
              </span>
            </div>

            <div 
              style={optionStyle} 
              className="menu-option" 
              onClick={() => handleAction(() => onShowAbout && onShowAbout())}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Info size={15} color="var(--colors-link)" /> About SORTIFY
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
