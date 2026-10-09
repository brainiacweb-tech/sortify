import React, { useState } from 'react';
import { 
  FolderCheck, 
  ShieldCheck, 
  Lock, 
  RotateCcw, 
  Sparkles, 
  ArrowRight, 
  X, 
  HelpCircle,
  HardDrive
} from 'lucide-react';

export default function WelcomeModal({ isOpen, onClose, onStartOrganizing, onOpenGuide }) {
  const [dontShowAgain, setDontShowAgain] = useState(false);

  if (!isOpen) return null;

  const handleClose = () => {
    if (dontShowAgain) {
      localStorage.setItem('sortify_welcomed', 'true');
    }
    onClose();
  };

  const handleStart = () => {
    localStorage.setItem('sortify_welcomed', 'true');
    if (onStartOrganizing) onStartOrganizing();
    onClose();
  };

  const handleGuide = () => {
    localStorage.setItem('sortify_welcomed', 'true');
    if (onOpenGuide) onOpenGuide();
    onClose();
  };

  return (
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        backdropFilter: 'blur(8px)',
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px'
      }}
    >
      <div 
        className="glass-card animate-scale-up"
        style={{
          maxWidth: '640px',
          width: '100%',
          backgroundColor: 'var(--bg-card)',
          borderRadius: '16px',
          border: '1px solid var(--border-card)',
          padding: '32px',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.4)',
          position: 'relative'
        }}
      >
        {/* Close button */}
        <button
          onClick={handleClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'none',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '4px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <X size={20} />
        </button>

        {/* Brand Badge & Header */}
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <div 
            style={{ 
              display: 'inline-flex', 
              alignItems: 'center', 
              gap: '6px', 
              padding: '6px 14px', 
              borderRadius: '20px', 
              backgroundColor: 'rgba(99, 102, 241, 0.12)', 
              color: 'var(--colors-primary)', 
              fontSize: '12px', 
              fontWeight: 700,
              marginBottom: '12px'
            }}
          >
            <Sparkles size={14} />
            <span>SORTIFY 1.0 — 100% OFFLINE & PRIVATE</span>
          </div>

          <h2 style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em', margin: 0 }}>
            Welcome to Sortify!
          </h2>
          <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
            Your smart desktop assistant for organizing cluttered folders, finding duplicate files, and managing local storage.
          </p>
        </div>

        {/* 4 Feature Highlights Grid */}
        <div 
          style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(2, 1fr)', 
            gap: '12px', 
            marginBottom: '28px' 
          }}
        >
          <div 
            style={{ 
              padding: '14px', 
              borderRadius: '10px', 
              backgroundColor: 'var(--bg-dark)', 
              border: '1px solid var(--border-card)',
              display: 'flex',
              gap: '12px',
              alignItems: 'flex-start'
            }}
          >
            <FolderCheck size={22} color="var(--colors-primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                Automated Smart Triage
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px', lineHeight: 1.35 }}>
                Sort Downloads, Desktop & Documents into category folders instantly.
              </p>
            </div>
          </div>

          <div 
            style={{ 
              padding: '14px', 
              borderRadius: '10px', 
              backgroundColor: 'var(--bg-dark)', 
              border: '1px solid var(--border-card)',
              display: 'flex',
              gap: '12px',
              alignItems: 'flex-start'
            }}
          >
            <ShieldCheck size={22} color="var(--colors-success)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                Collision-Free Safety
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px', lineHeight: 1.35 }}>
                Zero file overwrite risk, Recycle Bin deletion, and 1-Click batch Undo.
              </p>
            </div>
          </div>

          <div 
            style={{ 
              padding: '14px', 
              borderRadius: '10px', 
              backgroundColor: 'var(--bg-dark)', 
              border: '1px solid var(--border-card)',
              display: 'flex',
              gap: '12px',
              alignItems: 'flex-start'
            }}
          >
            <Lock size={22} color="var(--colors-purple)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                AES-256 & Duplicates
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px', lineHeight: 1.35 }}>
                Find byte-for-byte SHA-256 duplicates and create encrypted password ZIPs.
              </p>
            </div>
          </div>

          <div 
            style={{ 
              padding: '14px', 
              borderRadius: '10px', 
              backgroundColor: 'var(--bg-dark)', 
              border: '1px solid var(--border-card)',
              display: 'flex',
              gap: '12px',
              alignItems: 'flex-start'
            }}
          >
            <HardDrive size={22} color="var(--colors-info)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                Storage Analytics
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px', lineHeight: 1.35 }}>
                Scan disk space hoggers and view Top 25 largest files in seconds.
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          <button 
            className="btn-primary" 
            onClick={handleStart}
            style={{ flex: 1, padding: '12px', justifyContent: 'center', fontSize: '0.95rem' }}
          >
            <span>Start Organizing My Files</span>
            <ArrowRight size={16} />
          </button>

          <button 
            className="btn-secondary" 
            onClick={handleGuide}
            style={{ padding: '12px 18px', justifyContent: 'center', fontSize: '0.9rem' }}
          >
            <HelpCircle size={16} />
            <span>User Guide</span>
          </button>
        </div>

        {/* Don't show again checkbox */}
        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'inline-flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={dontShowAgain} 
              onChange={(e) => setDontShowAgain(e.target.checked)} 
              style={{ accentColor: 'var(--colors-primary)' }}
            />
            <span>Do not show this welcome screen on startup</span>
          </label>
        </div>
      </div>
    </div>
  );
}
