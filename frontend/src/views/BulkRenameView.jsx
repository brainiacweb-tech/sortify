import React, { useState, useEffect } from 'react';
import { Play } from 'lucide-react';
import confetti from 'canvas-confetti';
import { API_BASE } from '../apiConfig';

export default function BulkRenameView({ targetFolder, setTargetFolder }) {
  const [prefix, setPrefix] = useState('');
  const [suffix, setSuffix] = useState('');
  const [searchPattern, setSearchPattern] = useState('');
  const [replacePattern, setReplacePattern] = useState('');
  const [filesToRename, setFilesToRename] = useState([]);
  const [isRenaming, setIsRenaming] = useState(false);
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

  const handleScanFolderFiles = async () => {
    try {
      const res = await fetch(`${API_BASE}/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder: targetFolder, recursive: false, check_duplicates: false })
      });
      const data = await res.json();
      if (res.ok && data.items) {
        setFilesToRename(data.items.map(i => i.filename));
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (targetFolder) handleScanFolderFiles();
  }, [targetFolder]);

  const transformName = (original) => {
    let name = original;
    const extIdx = name.lastIndexOf('.');
    let stem = extIdx !== -1 ? name.substring(0, extIdx) : name;
    let ext = extIdx !== -1 ? name.substring(extIdx) : '';

    if (searchPattern) stem = stem.replaceAll(searchPattern, replacePattern);
    return `${prefix}${stem}${suffix}${ext}`;
  };

  const handleApplyRename = async () => {
    if (!targetFolder || isRenaming) return;
    setIsRenaming(true);

    try {
      const res = await fetch(`${API_BASE}/rename`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          folder: targetFolder,
          prefix: prefix,
          suffix: suffix,
          search: searchPattern,
          replace: replacePattern
        })
      });
      const data = await res.json();
      setIsRenaming(false);

      if (res.ok) {
        confetti({ particleCount: 70, spread: 60 });
        alert(`Successfully renamed ${data.renamed_count} files.`);
        handleScanFolderFiles();
      } else {
        alert('Error: ' + (data.error || 'Failed to rename files.'));
      }
    } catch (err) {
      setIsRenaming(false);
      alert('Error: ' + err.message);
    }
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)' }}>
          Rename Files
        </h2>
        <p style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Rename multiple files at once by adding prefixes, suffixes, or replacing text.
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
          value={targetFolder}
          onChange={(e) => setTargetFolder(e.target.value)}
          placeholder="Select folder..."
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
      </div>

      <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)' }}>Rename Options</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '14px' }}>
          <div>
            <label style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>ADD TO START</label>
            <input
              type="text"
              value={prefix}
              onChange={(e) => setPrefix(e.target.value)}
              placeholder="e.g. 2026_"
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', color: 'var(--text-primary)', outline: 'none' }}
            />
          </div>
          <div>
            <label style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>ADD TO END</label>
            <input
              type="text"
              value={suffix}
              onChange={(e) => setSuffix(e.target.value)}
              placeholder="e.g. _final"
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', color: 'var(--text-primary)', outline: 'none' }}
            />
          </div>
          <div>
            <label style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>FIND TEXT</label>
            <input
              type="text"
              value={searchPattern}
              onChange={(e) => setSearchPattern(e.target.value)}
              placeholder="e.g. draft"
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', color: 'var(--text-primary)', outline: 'none' }}
            />
          </div>
          <div>
            <label style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>REPLACE WITH</label>
            <input
              type="text"
              value={replacePattern}
              onChange={(e) => setReplacePattern(e.target.value)}
              placeholder="e.g. ready"
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-card)', backgroundColor: 'var(--bg-dark)', color: 'var(--text-primary)', outline: 'none' }}
            />
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', paddingTop: '8px' }}>
          <button className="btn-orange" onClick={handleApplyRename} disabled={isRenaming || filesToRename.length === 0}>
            <Play size={16} />
            <span>{isRenaming ? 'Renaming...' : 'Rename Files'}</span>
          </button>
        </div>
      </div>

      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '16px' }}>
          Preview ({filesToRename.length} files)
        </h3>

        {filesToRename.length === 0 ? (
          <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>
            No files found in selected folder.
          </div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-card)', color: 'var(--text-muted)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                <th style={{ padding: '10px 12px' }}>Current Name</th>
                <th style={{ padding: '10px 12px' }}>→</th>
                <th style={{ padding: '10px 12px' }}>New Name</th>
              </tr>
            </thead>
            <tbody>
              {filesToRename.slice(0, 15).map((file, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid var(--border-card)' }}>
                  <td style={{ padding: '10px 12px', color: 'var(--text-muted)' }}>{file}</td>
                  <td style={{ padding: '10px 12px', color: 'var(--accent-orange)', fontWeight: 700 }}>→</td>
                  <td style={{ padding: '10px 12px', fontWeight: 700, color: 'var(--primary-blue)' }}>{transformName(file)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
