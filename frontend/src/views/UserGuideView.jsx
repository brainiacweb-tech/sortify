import React from 'react';
import { 
  FolderTree, 
  Copy, 
  History, 
  Sliders, 
  Edit3, 
  Settings, 
  CheckCircle2, 
  ArrowRight, 
  ShieldCheck, 
  HelpCircle,
  Zap,
  Sparkles,
  FileText,
  Image,
  Code2,
  Music,
  Film,
  Archive,
  Table,
  Cpu,
  Layers,
  Lock,
  RotateCcw,
  Eye,
  Check,
  HardDrive,
  PieChart,
  Trash2,
  Folder,
  Calendar,
  Sparkle
} from 'lucide-react';

export default function UserGuideView({ onNavigate }) {
  const steps = [
    {
      num: '01',
      title: 'Select Directory & Mode',
      desc: 'Click "Browse..." or pick a shortcut (Downloads, Desktop, Documents). Choose Standard, Smart Arrange, or Date Arrange mode.',
      icon: FolderTree,
      color: '#3B82F6'
    },
    {
      num: '02',
      title: 'Preview Dry-Run Scan',
      desc: 'Sortify safely analyzes all files, categorizes them automatically, and flags duplicate collisions before touching disk.',
      icon: Eye,
      color: '#13C56B'
    },
    {
      num: '03',
      title: 'Execute Safe Operations',
      desc: 'Click "Start Organizing" or manage files in Files Manager (Move, Copy, ZIP, Password Encrypt, Hide, Recycle Bin).',
      icon: CheckCircle2,
      color: '#007427'
    },
    {
      num: '04',
      title: '1-Click Undo & History Journal',
      desc: 'Every file operation is logged in your local audit journal. Click 1-Click Restore to undo any run instantly.',
      icon: RotateCcw,
      color: '#8B5CF6'
    }
  ];

  const categories = [
    { name: 'Documents', folder: 'Documents/', exts: '.pdf, .docx, .txt, .xlsx, .pptx', icon: FileText, color: '#3B82F6' },
    { name: 'Images & Photos', folder: 'Images/', exts: '.png, .jpg, .svg, .gif, .webp', icon: Image, color: '#EC4899' },
    { name: 'Source Code', folder: 'Code/', exts: '.py, .js, .cpp, .html, .css, .json', icon: Code2, color: '#8B5CF6' },
    { name: 'Audio & Music', folder: 'Audio/', exts: '.mp3, .wav, .flac, .aac, .ogg', icon: Music, color: '#F59E0B' },
    { name: 'Video & Movies', folder: 'Videos/', exts: '.mp4, .mkv, .avi, .mov, .webm', icon: Film, color: '#EF4444' },
    { name: 'Compressed Archives', folder: 'Archives/', exts: '.zip, .rar, .7z, .tar, .gz', icon: Archive, color: '#10B981' },
    { name: 'Spreadsheets', folder: 'Spreadsheets/', exts: '.csv, .xls, .xlsx, .ods', icon: Table, color: '#13C56B' },
    { name: 'Software Installers', folder: 'Executables/', exts: '.exe, .msi, .bat, .cmd, .iso', icon: Cpu, color: '#6366F1' },
    { name: '3D & Design Assets', folder: 'Graphics/', exts: '.blend, .psd, .ai, .fig, .stl', icon: Layers, color: '#14B8A6' },
  ];

  const features = [
    {
      id: 'organize',
      title: 'Smart & Date Folder Arrange',
      icon: FolderTree,
      color: '#3B82F6',
      badge: 'Core Engine',
      summary: 'Proposes clean nested folder hierarchies before moving files.',
      bullets: [
        { text: 'Smart Arrange: Documents/PDFs, Documents/Word, Documents/Spreadsheets', icon: Check },
        { text: 'Date Arrange: Automatically groups files into YYYY/Month folders', icon: Calendar },
        { text: 'Dry-Run Preview & Protected Locations validation (e.g. C:\\Windows blocking)', icon: ShieldCheck }
      ]
    },
    {
      id: 'files',
      title: 'Files Management Utility',
      icon: HardDrive,
      color: '#10B981',
      badge: 'File Utility',
      summary: 'Full Windows file manager with right-click menu & bulk action toolbar.',
      bullets: [
        { text: 'Move to Windows Recycle Bin natively (non-destructive delete)', icon: Trash2 },
        { text: 'ZIP & Password-Protected AES Encrypted archives (pyzipper)', icon: Lock },
        { text: 'Hide / Unhide Windows file attributes & Bulk Move/Copy/Rename', icon: Eye }
      ]
    },
    {
      id: 'duplicates',
      title: 'SHA-256 Duplicate Detector',
      icon: Copy,
      color: '#F59E0B',
      badge: 'Storage Saver',
      summary: 'Finds identical files regardless of file name or modified date.',
      bullets: [
        { text: 'Byte-by-byte SHA-256 cryptographic hash comparison', icon: Check },
        { text: 'Quarantine feature moves duplicates safely into "Duplicates/" folder', icon: HardDrive },
        { text: 'Reclaims gigabytes of wasted disk space with 1 click', icon: Sparkles }
      ]
    },
    {
      id: 'storage',
      title: 'Storage Analytics & Large Files',
      icon: PieChart,
      color: '#6366F1',
      badge: 'Disk Analyzer',
      summary: 'Identify space-hogging files and view category storage distribution.',
      bullets: [
        { text: 'Top 25 Largest Files Explorer table with 1-click recycle action', icon: Check },
        { text: 'Category disk space distribution charts & size metrics', icon: PieChart },
        { text: 'Identify disk consumption hotspots instantly', icon: Zap }
      ]
    },
    {
      id: 'history',
      title: '1-Click Undo & Operations Journal',
      icon: History,
      color: '#8B5CF6',
      badge: 'Safety First',
      summary: 'Every file operation is journaled into local audit history.',
      bullets: [
        { text: 'Complete audit trail of every organize run with exact timestamps', icon: Check },
        { text: '1-Click Restore moves every file back to its exact original location', icon: RotateCcw },
        { text: 'Never worry about misplacing files or wrong directory moves', icon: ShieldCheck }
      ]
    },
    {
      id: 'rules',
      title: 'Custom File Extension Rules',
      icon: Sliders,
      color: '#10B981',
      badge: 'Customization',
      summary: 'Define custom file extensions and map them to custom target folders.',
      bullets: [
        { text: 'Add rules like putting .blend or .obj files into "3D Models"', icon: Check },
        { text: 'Create rules for custom code, audio clips, or design files', icon: Layers },
        { text: 'Rules persist locally across app restarts', icon: Lock }
      ]
    }
  ];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      {/* Header Banner */}
      <div style={{
        padding: '28px 32px',
        borderRadius: 'var(--rounded-sm)',
        backgroundColor: 'var(--bg-card)',
        border: '1px solid var(--border-card)',
        boxShadow: 'var(--card-shadow)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ maxWidth: '650px', zIndex: 1 }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            padding: '5px 12px',
            borderRadius: 'var(--rounded-sm)',
            backgroundColor: '#F3FFF7',
            border: '1px solid var(--colors-primary)',
            color: 'var(--colors-link)',
            fontSize: '12px',
            fontWeight: 700,
            marginBottom: '12px'
          }}>
            <HelpCircle size={15} />
            <span>SORTIFY v1.0 USER GUIDELINES</span>
          </div>
          <h2 style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
            Sortify — Smart File Organizer & File Management Utility
          </h2>
          <p style={{ fontSize: '0.94rem', color: 'var(--text-secondary)', marginTop: '8px', lineHeight: 1.6 }}>
            Complete guide to automatic file organization, Smart & Date Arrange, Windows Recycle Bin, Password-Protected ZIPs, Hide/Unhide files, Storage Analytics, and 1-Click Undo History.
          </p>
        </div>

        <div style={{
          padding: '20px',
          borderRadius: 'var(--rounded-sm)',
          backgroundColor: 'var(--colors-primary)',
          color: '#FFFFFF',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '8px',
          boxShadow: '0 4px 16px rgba(19, 197, 107, 0.3)',
          zIndex: 1
        }}>
          <ShieldCheck size={32} />
          <span style={{ fontSize: '11px', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>100% Offline & Safe</span>
        </div>
      </div>

      {/* 4 Quick Start Steps */}
      <div>
        <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '18px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Zap size={20} color="var(--colors-primary)" />
          <span>Quick Start Workflow (4 Easy Steps)</span>
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '18px' }}>
          {steps.map((step) => {
            const Icon = step.icon;
            return (
              <div key={step.num} className="glass-card" style={{ padding: '22px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '1.5rem', fontWeight: 800, color: step.color, fontFamily: 'var(--font-heading)' }}>
                    {step.num}
                  </span>
                  <div style={{
                    width: '38px',
                    height: '38px',
                    borderRadius: '50%',
                    backgroundColor: `${step.color}15`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: step.color
                  }}>
                    <Icon size={20} />
                  </div>
                </div>
                <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>{step.title}</h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{step.desc}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Automatic File Categorization Cheatsheet with Icons */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FolderTree size={20} color="var(--colors-primary)" />
          <span>Automatic File Categorization Cheatsheet</span>
        </h3>
        <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginBottom: '20px' }}>
          Sortify automatically maps files into target subdirectories based on their exact file extensions:
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '14px' }}>
          {categories.map((cat, idx) => {
            const CatIcon = cat.icon;
            return (
              <div key={idx} style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 14px',
                borderRadius: 'var(--rounded-sm)',
                backgroundColor: 'var(--bg-dark)',
                border: '1px solid var(--border-card)'
              }}>
                <div style={{
                  width: '34px',
                  height: '34px',
                  borderRadius: 'var(--rounded-sm)',
                  backgroundColor: `${cat.color}18`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: cat.color,
                  flexShrink: 0
                }}>
                  <CatIcon size={18} />
                </div>
                <div style={{ overflow: 'hidden' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--text-primary)' }}>{cat.name}</span>
                    <span style={{ fontSize: '11px', fontWeight: 600, color: cat.color }}>({cat.folder})</span>
                  </div>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {cat.exts}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Feature Deep Dive Grid */}
      <div>
        <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '18px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Layers size={20} color="var(--colors-primary)" />
          <span>Core Modules & File Utility Tools</span>
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
          {features.map((feat) => {
            const Icon = feat.icon;
            return (
              <div key={feat.id} className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <div style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: 'var(--rounded-sm)',
                        backgroundColor: feat.color,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: '#FFFFFF'
                      }}>
                        <Icon size={22} />
                      </div>
                      <h4 style={{ fontSize: '1.08rem', fontWeight: 700, color: 'var(--text-primary)' }}>{feat.title}</h4>
                    </div>

                    <span style={{
                      fontSize: '11px',
                      fontWeight: 700,
                      padding: '4px 10px',
                      borderRadius: 'var(--rounded-sm)',
                      backgroundColor: `${feat.color}18`,
                      color: feat.color
                    }}>
                      {feat.badge}
                    </span>
                  </div>

                  <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginBottom: '16px', fontWeight: 500, lineHeight: 1.4 }}>
                    {feat.summary}
                  </p>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {feat.bullets.map((b, bIdx) => {
                      const BIcon = b.icon;
                      return (
                        <div key={bIdx} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                          <BIcon size={15} color={feat.color} style={{ flexShrink: 0, marginTop: '2px' }} />
                          <span style={{ fontSize: '0.83rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
                            {b.text}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {onNavigate && (
                  <button 
                    onClick={() => onNavigate(feat.id)} 
                    className="btn-secondary" 
                    style={{ marginTop: '20px', justifyContent: 'center', fontSize: '12.5px', width: '100%' }}
                  >
                    <span>Open {feat.title}</span>
                    <ArrowRight size={15} />
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Safety & Privacy Guarantees Box */}
      <div className="glass-card" style={{ padding: '24px', backgroundColor: 'var(--bg-card)', borderColor: 'var(--colors-primary)' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Lock size={20} color="var(--colors-primary)" />
          <span>Safety & Local Privacy Guarantees</span>
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px', marginTop: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
            <ShieldCheck size={18} color="var(--colors-primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h5 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)' }}>Protected System Paths</h5>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '2px' }}>System folders like C:\Windows and C:\Program Files are blocked from mass re-organization.</p>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
            <Trash2 size={18} color="var(--colors-primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h5 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)' }}>Windows Recycle Bin Deletion</h5>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '2px' }}>Deletion moves items safely to the Windows Recycle Bin instead of permanent data destruction.</p>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
            <RotateCcw size={18} color="var(--colors-primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h5 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)' }}>Full Transactional Undo</h5>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '2px' }}>Every organize batch is journaled so you can restore original folder paths with 1 click.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
