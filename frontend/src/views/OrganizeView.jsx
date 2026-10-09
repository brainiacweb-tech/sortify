import React, { useState, useEffect } from 'react';
import { FolderSearch, Play, AlertTriangle, CheckCircle2 } from 'lucide-react';
import confetti from 'canvas-confetti';
import { API_BASE } from '../apiConfig';

export default function OrganizeView({ targetFolder, setTargetFolder, onActivityUpdated }) {
  const [recursive, setRecursive] = useState(false);
  const [checkDuplicates, setCheckDuplicates] = useState(true);
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [isOrganizing, setIsOrganizing] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const fileInputRef = React.useRef(null);

  useEffect(() => {
    fetch(`${API_BASE}/default-folders`)
      .then(res => res.json())
      .then(data => {
        if (data && data.downloads && !targetFolder) setTargetFolder(data.downloads);
      })
      .catch(() => {});
  }, []);

  const handleBrowseFolder = async () => {
    try {
      if (window.pywebview && window.pywebview.api && window.pywebview.api.select_folder) {
        const res = await window.pywebview.api.select_folder(targetFolder || '');
        if (res && res.folder) {
          setTargetFolder(res.folder);
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
        body: JSON.stringify({ initial: targetFolder })
      });
      if (res.ok) {
        const data = await res.json();
        if (data && data.folder) {
          setTargetFolder(data.folder);
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
        if (folderPath) setTargetFolder(folderPath);
      } else if (firstFile.webkitRelativePath) {
        const relDir = firstFile.webkitRelativePath.split('/')[0];
        if (relDir) setTargetFolder(relDir);
      }
    }
  };

  const [arrangeMode, setArrangeMode] = useState('standard'); // 'standard' | 'smart' | 'date'

  const handleScan = async (overrideMode) => {
    if (!targetFolder) return;
    const modeToUse = overrideMode || arrangeMode;
    setIsScanning(true);
    setStatusMessage('Scanning files...');
    setScanResult(null);

    try {
      const res = await fetch(`${API_BASE}/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          folder: targetFolder,
          recursive: recursive,
          check_duplicates: checkDuplicates,
          arrange_mode: modeToUse
        })
      });
      const data = await res.json();
      setIsScanning(false);

      if (res.ok) {
        setScanResult(data);
        setStatusMessage(`Found ${data.total_files} files (${data.total_size}). Ready to organize.`);
      } else {
        alert('Error: ' + (data.error || 'Failed to scan folder.'));
        setStatusMessage('');
      }
    } catch (err) {
      setIsScanning(false);
      alert('Error: ' + err.message);
      setStatusMessage('');
    }
  };

  const handleOrganize = async () => {
    if (!scanResult || isOrganizing) return;
    setIsOrganizing(true);
    setStatusMessage('Organizing files safely...');

    try {
      const res = await fetch(`${API_BASE}/organize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await res.json();
      setIsOrganizing(false);

      if (res.ok) {
        confetti({ particleCount: 90, spread: 70, origin: { y: 0.6 } });
        alert(`Done! Successfully organized ${data.total_successful} files (${data.bytes_moved} moved).`);
        setScanResult(null);
        setStatusMessage('Organization finished successfully.');
        if (onActivityUpdated) onActivityUpdated();
      } else {
        alert('Error: ' + (data.error || 'Failed to organize files.'));
        setStatusMessage('');
      }
    } catch (err) {
      setIsOrganizing(false);
      alert('Error: ' + err.message);
      setStatusMessage('');
    }
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header */}
      <div>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)' }}>
          Organize Files
        </h2>
        <p style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Select a folder to scan and automatically move files into clean sub-folders.
        </p>
      </div>

      {/* Control Box */}
      <div className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px', borderRadius: 'var(--rounded-sm)' }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
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
            value={targetFolder}
            onChange={(e) => setTargetFolder(e.target.value)}
            placeholder="Select folder to scan..."
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
          <button className="btn-secondary" onClick={handleBrowseFolder}>
            Browse...
          </button>
        </div>

        {/* Checkbox Options */}
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-primary)' }}>
            <input
              type="checkbox"
              checked={recursive}
              onChange={(e) => setRecursive(e.target.checked)}
              style={{ accentColor: 'var(--colors-primary)' }}
            />
            <span>Include sub-folders</span>
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-primary)' }}>
            <input
              type="checkbox"
              checked={checkDuplicates}
              onChange={(e) => setCheckDuplicates(e.target.checked)}
              style={{ accentColor: 'var(--colors-primary)' }}
            />
            <span>Check for duplicate files</span>
          </label>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '4px' }}>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button className="btn-primary" onClick={handleScan} disabled={isScanning || !targetFolder}>
              <FolderSearch size={16} />
              <span>{isScanning ? 'Scanning...' : 'Scan Folder'}</span>
            </button>
            <button
              className="btn-primary"
              style={{ backgroundColor: 'var(--colors-link)', borderColor: 'var(--colors-link)' }}
              onClick={handleOrganize}
              disabled={!scanResult || scanResult.items.length === 0 || isOrganizing}
            >
              <Play size={16} />
              <span>{isOrganizing ? 'Organizing...' : 'Organize Files Now'}</span>
            </button>
          </div>

          <span style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-muted)' }}>
            {statusMessage || (scanResult ? `${scanResult.total_files} files ready` : 'Ready')}
          </span>
        </div>
      </div>

      {/* Preview Table */}
      {scanResult && (
        <div className="glass-card" style={{ padding: '20px', borderRadius: 'var(--rounded-sm)' }}>
          <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '16.5px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '16px' }}>
            Scan Preview ({scanResult.total_files} Files — {scanResult.total_size})
          </h3>

          {scanResult.items.length === 0 ? (
            <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '13.2px' }}>
              This folder is already clean and organized!
            </div>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '13.2px' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-card)', color: 'var(--text-muted)', fontSize: '12px', fontFamily: 'var(--font-heading)', fontWeight: 600, textTransform: 'uppercase' }}>
                  <th style={{ padding: '10px 12px' }}>File Name</th>
                  <th style={{ padding: '10px 12px' }}>Category</th>
                  <th style={{ padding: '10px 12px' }}>New Folder Location</th>
                  <th style={{ padding: '10px 12px' }}>Size</th>
                </tr>
              </thead>
              <tbody>
                {scanResult.items.map((file, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid var(--border-card)' }}>
                    <td style={{ padding: '10px 12px', fontWeight: 500, color: 'var(--text-primary)' }}>{file.filename}</td>
                    <td style={{ padding: '10px 12px', color: 'var(--colors-link)', fontWeight: 500 }}>{file.category}</td>
                    <td style={{ padding: '10px 12px', color: 'var(--text-secondary)' }}>{file.target_path}</td>
                    <td style={{ padding: '10px 12px', color: 'var(--text-muted)' }}>{file.size}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
