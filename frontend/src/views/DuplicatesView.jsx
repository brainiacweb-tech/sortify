import React, { useState, useEffect } from 'react';
import { Search, ShieldCheck, Copy, Check } from 'lucide-react';
import confetti from 'canvas-confetti';

const API_BASE = 'http://127.0.0.1:5000/api';

export default function DuplicatesView({ targetDir, setTargetDir }) {
  const [isScanning, setIsScanning] = useState(false);
  const [duplicatesData, setDuplicatesData] = useState(null);
  const [isQuarantining, setIsQuarantining] = useState(false);
  const fileInputRef = React.useRef(null);

  useEffect(() => {
    fetch(`${API_BASE}/default-folders`)
      .then(res => res.json())
      .then(data => {
        if (data && data.downloads && !targetDir) setTargetDir(data.downloads);
      })
      .catch(() => {});
  }, []);

  const handleBrowseFolder = async () => {
    try {
      if (window.pywebview && window.pywebview.api && window.pywebview.api.select_folder) {
        const res = await window.pywebview.api.select_folder(targetDir || '');
        if (res && res.folder) {
          setTargetDir(res.folder);
          return;
        }
        if (res && res.cancelled) return;
      }
    } catch (e) {
      console.error('PyWebView native dialog error:', e);
    }

    try {
      const res = await fetch(`${API_BASE}/select-folder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initial: targetDir })
      });
      if (res.ok) {
        const data = await res.json();
        if (data && data.folder) {
          setTargetDir(data.folder);
          return;
        }
        if (data && data.cancelled) return;
      }
    } catch (err) {
      console.error('API select-folder error:', err);
    }
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleDirectoryInputChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const firstFile = e.target.files[0];
      if (firstFile.path) {
        const folderPath = firstFile.path.substring(0, Math.max(firstFile.path.lastIndexOf('\\'), firstFile.path.lastIndexOf('/')));
        if (folderPath) setTargetDir(folderPath);
      } else if (firstFile.webkitRelativePath) {
        const relDir = firstFile.webkitRelativePath.split('/')[0];
        if (relDir) setTargetDir(relDir);
      }
    }
  };

  const handleScan = async () => {
    if (!targetDir) return;
    setIsScanning(true);
    setDuplicatesData(null);

    try {
      const res = await fetch(`${API_BASE}/duplicates`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder: targetDir })
      });
      const data = await res.json();
      setIsScanning(false);

      if (res.ok) {
        setDuplicatesData(data);
      } else {
        alert('Error: ' + (data.error || 'Failed to check duplicates.'));
      }
    } catch (err) {
      setIsScanning(false);
      alert('Error: ' + err.message);
    }
  };

  const handleQuarantine = async () => {
    if (!targetDir || isQuarantining) return;
    setIsQuarantining(true);

    try {
      const res = await fetch(`${API_BASE}/quarantine`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder: targetDir })
      });
      const data = await res.json();
      setIsQuarantining(false);

      if (res.ok) {
        confetti({ particleCount: 70, spread: 60 });
        alert(`Cleaned up ${data.moved_count} duplicate files into "Duplicates" folder.`);
        handleScan();
      } else {
        alert('Error: ' + (data.error || 'Failed to move duplicates.'));
      }
    } catch (err) {
      setIsQuarantining(false);
      alert('Error: ' + err.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)' }}>
          Find Duplicates
        </h2>
        <p style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Find copy files on your computer and safely move them to a separate folder.
        </p>
      </div>

      <div className="glass-card" style={{ padding: '20px', display: 'flex', gap: '12px', alignItems: 'center', borderRadius: 'var(--rounded-sm)' }}>
        <input
          type="file"
          ref={fileInputRef}
          webkitdirectory="true"
          directory="true"
          style={{ display: 'none' }}
          onChange={handleDirectoryInputChange}
        />
        <input
          type="text"
          value={targetDir}
          onChange={(e) => setTargetDir(e.target.value)}
          placeholder="Select folder to check..."
          style={{
            flex: 1,
            height: '37.8px',
            padding: '8px 14.4px',
            borderRadius: 'var(--rounded-sm)',
            border: '1px solid var(--border-card)',
            backgroundColor: 'var(--bg-card)',
            color: 'var(--text-primary)',
            fontFamily: 'var(--font-body)',
            fontSize: '13.2px',
            outline: 'none'
          }}
        />
        <button className="btn-secondary" onClick={handleBrowseFolder}>Browse...</button>
        <button className="btn-primary" onClick={handleScan} disabled={isScanning || !targetDir}>
          <Search size={16} />
          <span>{isScanning ? 'Checking...' : 'Find Duplicates'}</span>
        </button>
      </div>

      {duplicatesData && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div className="glass-card" style={{ padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                {duplicatesData.duplicate_count === 0
                  ? `Clean! No duplicate files found in ${duplicatesData.total_scanned} files.`
                  : `Found ${duplicatesData.duplicate_count} duplicate files (${duplicatesData.wasted_space} wasted space)`}
              </h4>
            </div>
            {duplicatesData.duplicate_count > 0 && (
              <button
                className="btn-orange"
                onClick={handleQuarantine}
                disabled={isQuarantining}
              >
                <ShieldCheck size={18} />
                <span>{isQuarantining ? 'Cleaning...' : 'Clean Duplicates'}</span>
              </button>
            )}
          </div>

          {duplicatesData.groups && duplicatesData.groups.map((group, idx) => (
            <div key={idx} className="glass-card" style={{ padding: '18px' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '10px' }}>
                Size: {group.size}
              </div>

              {/* Original */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 12px', borderRadius: '8px', backgroundColor: 'rgba(16, 185, 129, 0.1)', marginBottom: '6px' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Check size={16} />
                  <span>Original: {group.original}</span>
                </span>
                <span className="badge" style={{ backgroundColor: 'var(--accent-emerald)', color: '#FFFFFF' }}>Keep</span>
              </div>

              {/* Copies */}
              {group.copies && group.copies.map((copy, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 12px', borderRadius: '8px', backgroundColor: 'rgba(245, 158, 11, 0.08)', marginTop: '4px' }}>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-primary)' }}>
                    Duplicate: {copy}
                  </span>
                  <span className="badge" style={{ backgroundColor: 'var(--accent-amber)', color: '#FFFFFF' }}>Copy</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
