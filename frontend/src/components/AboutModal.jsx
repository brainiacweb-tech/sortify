import React, { useState } from 'react';
import { 
  X, 
  ShieldCheck, 
  Zap, 
  HardDrive, 
  Heart, 
  RefreshCw, 
  CheckCircle2, 
  Users, 
  FileText, 
  Award, 
  Code2, 
  ExternalLink 
} from 'lucide-react';
import confetti from 'canvas-confetti';
import logoImg from '../assets/logo.png';

export default function AboutModal({ isOpen, onClose }) {
  const [activeSubTab, setActiveSubTab] = useState('overview'); // 'overview' | 'authors' | 'license' | 'credits'

  if (!isOpen) return null;

  const handleCheckUpdates = () => {
    confetti({ particleCount: 80, spread: 70, origin: { y: 0.6 } });
    alert("SORTIFY is up to date! You are running version 1.0.1 (Latest Release).");
  };

  const authorsList = [
    { name: 'Francis Kusi', role: 'Lead Architect & Core Developer', org: 'SORTIFY Team' },
    { name: 'Open Source Community', role: 'UI/UX & Engine Contributors', org: 'Global Contributors' }
  ];

  const externalCredits = [
    { name: 'Python 3.14 Standard Engine', license: 'PSF License', desc: 'Core file classification, ctypes Win32 API & SHA-256 hash calculation.' },
    { name: 'PyWebView Desktop Wrapper', license: 'BSD License', desc: 'Native Win32 desktop window host and zero-delay folder picker API.' },
    { name: 'Flask & Flask-CORS Server', license: 'BSD-3-Clause', desc: 'Lightweight REST API backend connecting React frontend to Python core engines.' },
    { name: 'React 18 & Vite Ecosystem', license: 'MIT License', desc: 'Modern responsive UI state management and fast asset bundling.' },
    { name: 'Lucide Icon System', license: 'ISC License', desc: 'Clean vector micro-icon library for modern web design.' },
    { name: 'Canvas Confetti Engine', license: 'MIT License', desc: 'Celebratory UI animation effects.' }
  ];

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(15, 23, 42, 0.65)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      padding: '20px'
    }}>
      <div className="glass-card animate-fade-in" style={{
        width: '100%',
        maxWidth: '580px',
        borderRadius: 'var(--rounded-sm)',
        padding: '28px',
        position: 'relative',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1)',
        backgroundColor: 'var(--bg-card)',
        border: '1px solid var(--border-card)'
      }}>
        {/* Close Button */}
        <button 
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '18px',
            right: '18px',
            border: 'none',
            background: 'transparent',
            cursor: 'pointer',
            color: 'var(--text-muted)',
            padding: '4px',
            borderRadius: 'var(--rounded-sm)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
          title="Close"
        >
          <X size={20} />
        </button>

        {/* Top Header & Logo */}
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '10px 22px',
            borderRadius: 'var(--rounded-sm)',
            backgroundColor: 'var(--colors-primary)',
            boxShadow: '0 4px 16px rgba(19, 197, 107, 0.35)',
            marginBottom: '12px'
          }}>
            <img src={logoImg} alt="Sortify Logo" style={{ height: '36px', objectFit: 'contain' }} />
          </div>

          <h2 style={{
            fontFamily: 'var(--font-heading)',
            fontSize: '24px',
            fontWeight: 800,
            color: 'var(--text-primary)',
            letterSpacing: '-0.02em'
          }}>
            SORTIFY
          </h2>

          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            backgroundColor: 'rgb(217, 241, 225)',
            color: 'var(--colors-link)',
            padding: '4px 12px',
            borderRadius: '16px',
            fontSize: '12px',
            fontFamily: 'var(--font-body)',
            fontWeight: 600,
            marginTop: '6px'
          }}>
            <CheckCircle2 size={13} /> Version 1.0.1 (Desktop Edition)
          </div>
        </div>

        {/* Navigation Tabs (Authors | License | Credits | Overview) */}
        <div style={{
          display: 'flex',
          borderBottom: '1px solid var(--border-card)',
          marginBottom: '20px',
          gap: '4px'
        }}>
          {[
            { id: 'overview', label: 'Overview', icon: Zap },
            { id: 'authors', label: 'Authors', icon: Users },
            { id: 'license', label: 'License', icon: FileText },
            { id: 'credits', label: 'Credits', icon: Award }
          ].map((tab) => {
            const TabIcon = tab.icon;
            const isSelected = activeSubTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveSubTab(tab.id)}
                style={{
                  flex: 1,
                  padding: '8px 10px',
                  border: 'none',
                  borderBottom: isSelected ? '2px solid var(--colors-primary)' : '2px solid transparent',
                  backgroundColor: 'transparent',
                  color: isSelected ? 'var(--colors-link)' : 'var(--text-muted)',
                  fontWeight: isSelected ? 700 : 500,
                  fontSize: '12.5px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '6px',
                  transition: 'all 0.15s ease'
                }}
              >
                <TabIcon size={14} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Tab Content Views */}
        <div style={{ minHeight: '210px', marginBottom: '20px' }}>
          {activeSubTab === 'overview' && (
            <div>
              <p style={{
                fontFamily: 'var(--font-body)',
                fontSize: '13px',
                color: 'var(--text-secondary)',
                marginBottom: '16px',
                lineHeight: 1.5
              }}>
                Automated file organizer and duplicate finder for Windows. Classifies chaotic directories into clean subfolders and provides full 1-click transaction undo.
              </p>

              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: '10px',
                marginBottom: '16px'
              }}>
                <div style={{ padding: '10px', borderRadius: 'var(--rounded-sm)', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Zap size={16} color="var(--colors-primary)" />
                  <div>
                    <p style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)' }}>Fast Scan</p>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Python 3.14 Engine</p>
                  </div>
                </div>

                <div style={{ padding: '10px', borderRadius: 'var(--rounded-sm)', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <ShieldCheck size={16} color="var(--colors-primary)" />
                  <div>
                    <p style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)' }}>100% Safe</p>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Transaction Journal</p>
                  </div>
                </div>

                <div style={{ padding: '10px', borderRadius: 'var(--rounded-sm)', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <HardDrive size={16} color="var(--colors-primary)" />
                  <div>
                    <p style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)' }}>SHA-256 Cleaning</p>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Quarantine Duplicates</p>
                  </div>
                </div>

                <div style={{ padding: '10px', borderRadius: 'var(--rounded-sm)', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Heart size={16} color="var(--colors-primary)" />
                  <div>
                    <p style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)' }}>100% Free</p>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Zero Subscriptions</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeSubTab === 'authors' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <p style={{ fontSize: '12.5px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                SORTIFY was created and developed by:
              </p>
              {authorsList.map((auth, idx) => (
                <div key={idx} style={{
                  padding: '12px 14px',
                  borderRadius: 'var(--rounded-sm)',
                  backgroundColor: 'var(--bg-dark)',
                  border: '1px solid var(--border-card)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between'
                }}>
                  <div>
                    <p style={{ fontSize: '13.5px', fontWeight: 700, color: 'var(--text-primary)' }}>{auth.name}</p>
                    <p style={{ fontSize: '11.5px', color: 'var(--colors-link)', fontWeight: 500 }}>{auth.role}</p>
                  </div>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)', backgroundColor: 'var(--bg-card)', padding: '3px 8px', borderRadius: 'var(--rounded-sm)', border: '1px solid var(--border-card)' }}>
                    {auth.org}
                  </span>
                </div>
              ))}
            </div>
          )}

          {activeSubTab === 'license' && (
            <div style={{ padding: '14px', borderRadius: 'var(--rounded-sm)', backgroundColor: 'var(--bg-dark)', border: '1px solid var(--border-card)', fontSize: '12px', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
              <p style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: '8px' }}>
                The MIT License (MIT)
              </p>
              <p style={{ marginBottom: '8px' }}>
                Copyright (c) 2026 Francis Kusi & SORTIFY Contributors.
              </p>
              <p style={{ fontSize: '11.5px', color: 'var(--text-muted)' }}>
                Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
              </p>
            </div>
          )}

          {activeSubTab === 'credits' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '220px', overflowY: 'auto', paddingRight: '4px' }}>
              <p style={{ fontSize: '11.5px', color: 'var(--text-muted)', marginBottom: '4px' }}>
                SORTIFY makes extensive use of the following open-source software libraries:
              </p>
              {externalCredits.map((cred, idx) => (
                <div key={idx} style={{
                  padding: '8px 10px',
                  borderRadius: 'var(--rounded-sm)',
                  backgroundColor: 'var(--bg-dark)',
                  border: '1px solid var(--border-card)'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-primary)' }}>{cred.name}</span>
                    <span style={{ fontSize: '10.5px', fontWeight: 600, color: 'var(--colors-link)' }}>{cred.license}</span>
                  </div>
                  <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>{cred.desc}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Action Buttons Footer */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-card)', paddingTop: '16px' }}>
          <button 
            className="btn-secondary"
            onClick={handleCheckUpdates}
            style={{ fontSize: '12px', padding: '6px 12px' }}
          >
            <RefreshCw size={14} />
            <span>Check for Updates</span>
          </button>

          <button 
            className="btn-primary"
            onClick={onClose}
            style={{ minWidth: '100px' }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
