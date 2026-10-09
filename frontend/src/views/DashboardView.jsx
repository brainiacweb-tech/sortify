import React, { useState, useEffect } from 'react';
import { 
  Folder, 
  FolderSearch, 
  Upload, 
  Table, 
  ArrowRight,
  CheckCircle2
} from 'lucide-react';
import { API_BASE } from '../apiConfig';

export default function DashboardView({ selectedFolder, setSelectedFolder, onNavigateOrganize, onNavigateDuplicates, onNavigateHistory, onFileUploadClick, stats }) {
  const [realHistory, setRealHistory] = useState([]);
  const [realStats, setRealStats] = useState(stats || {});
  const [defaultFolders, setDefaultFolders] = useState({
    downloads: '',
    desktop: '',
    documents: '',
    pictures: ''
  });
  const fileInputRef = React.useRef(null);

  useEffect(() => {
    fetch(`${API_BASE}/stats`)
      .then(res => res.json())
      .then(data => setRealStats(data))
      .catch(() => {});

    fetch(`${API_BASE}/default-folders`)
      .then(res => res.json())
      .then(data => {
        setDefaultFolders(data);
        if (data && data.downloads && !selectedFolder) {
          setSelectedFolder(data.downloads);
        }
      })
      .catch(() => {});

    fetch(`${API_BASE}/history`)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setRealHistory(data);
      })
      .catch(() => {});
  }, [stats]);

  const handleBrowseFolder = async () => {
    try {
      if (window.pywebview && window.pywebview.api && window.pywebview.api.select_folder) {
        const res = await window.pywebview.api.select_folder(selectedFolder || '');
        if (res && res.folder) {
          setSelectedFolder(res.folder);
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
        body: JSON.stringify({ initial: selectedFolder })
      });
      if (res.ok) {
        const data = await res.json();
        if (data && data.folder) {
          setSelectedFolder(data.folder);
          return;
        }
        if (data && data.cancelled) return;
      }
    } catch (err) {
      console.error('API folder select failed, triggering input element:', err);
    }
    // Fallback to HTML directory input picker
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleDirectoryInputChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const firstFile = e.target.files[0];
      if (firstFile.path) {
        const folderPath = firstFile.path.substring(0, Math.max(firstFile.path.lastIndexOf('\\'), firstFile.path.lastIndexOf('/')));
        if (folderPath) setSelectedFolder(folderPath);
      } else if (firstFile.webkitRelativePath) {
        const relDir = firstFile.webkitRelativePath.split('/')[0];
        if (relDir) setSelectedFolder(relDir);
      }
    }
  };

  const recentMoves = [];
  if (Array.isArray(realHistory)) {
    for (const batch of realHistory) {
      if (batch.moves && Array.isArray(batch.moves)) {
        for (const m of batch.moves) {
          if (m.status === 'SUCCESS' && !m.restored) {
            recentMoves.push({
              name: m.source ? m.source.split('\\').pop().split('/').pop() : 'File',
              category: m.original_category || 'Organized',
              time: batch.timestamp || 'Recent'
            });
            if (recentMoves.length >= 5) break;
          }
        }
      }
      if (recentMoves.length >= 5) break;
    }
  }

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Page Title */}
      <div>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)' }}>
          Dashboard
        </h2>
        <p style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Organize files automatically into clean, structured directories.
        </p>
      </div>

      {/* 4 Clean Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
        <div className="glass-card" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderRadius: 'var(--rounded-sm)' }}>
          <div>
            <p style={{ fontFamily: 'var(--font-heading)', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>FILES SORTED</p>
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)', marginTop: '2px' }}>
              {realStats.total_files_organized || 0}
            </h3>
          </div>
          <div style={{ width: '40px', height: '40px', borderRadius: 'var(--rounded-sm)', backgroundColor: 'rgb(217, 241, 225)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--colors-link)' }}>
            <CheckCircle2 size={20} />
          </div>
        </div>

        <div className="glass-card" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderRadius: 'var(--rounded-sm)' }}>
          <div>
            <p style={{ fontFamily: 'var(--font-heading)', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>TIMES USED</p>
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)', marginTop: '2px' }}>
              {realStats.total_runs || 0}
            </h3>
          </div>
          <div style={{ width: '40px', height: '40px', borderRadius: 'var(--rounded-sm)', backgroundColor: 'rgb(217, 241, 225)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--colors-link)' }}>
            <Folder size={20} />
          </div>
        </div>

        <div className="glass-card" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderRadius: 'var(--rounded-sm)' }}>
          <div>
            <p style={{ fontFamily: 'var(--font-heading)', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>DUPLICATES</p>
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)', marginTop: '2px' }}>
              {realStats.duplicates_found || 0}
            </h3>
          </div>
          <div style={{ width: '40px', height: '40px', borderRadius: 'var(--rounded-sm)', backgroundColor: 'rgb(217, 241, 225)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--colors-link)' }}>
            <FolderSearch size={20} />
          </div>
        </div>

        <div className="glass-card" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderRadius: 'var(--rounded-sm)' }}>
          <div>
            <p style={{ fontFamily: 'var(--font-heading)', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>CATEGORIES</p>
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)', marginTop: '2px' }}>
              {realStats.categories_count ?? Object.keys(realStats.category_breakdown || {}).length}
            </h3>
          </div>
          <div style={{ width: '40px', height: '40px', borderRadius: 'var(--rounded-sm)', backgroundColor: 'rgb(217, 241, 225)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--colors-link)' }}>
            <Table size={20} />
          </div>
        </div>
      </div>

      {/* Main Organize Action Card */}
      <div className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px', borderRadius: 'var(--rounded-sm)' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '16.5px', fontWeight: 600, color: 'var(--text-primary)' }}>
          Organize Target Directory
        </h3>
        <p style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-secondary)' }}>
          Select any folder on your machine to preview dry-run classification and execute safe sorting.
        </p>

        {/* Path Bar */}
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
            value={selectedFolder}
            onChange={(e) => setSelectedFolder(e.target.value)}
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
          <button className="btn-primary" onClick={onNavigateOrganize}>
            <span>Start Organizing</span>
            <ArrowRight size={16} />
          </button>
        </div>

        {/* Quick Folder Shortcuts */}
        {defaultFolders && (
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap', paddingTop: '4px' }}>
            <span style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', fontWeight: 500, color: 'var(--text-muted)' }}>Quick Select:</span>
            <button className="btn-secondary" style={{ height: '30px', padding: '4px 10px', fontSize: '12px' }} onClick={() => setSelectedFolder(defaultFolders.downloads)}>
              Downloads
            </button>
            <button className="btn-secondary" style={{ height: '30px', padding: '4px 10px', fontSize: '12px' }} onClick={() => setSelectedFolder(defaultFolders.desktop)}>
              Desktop
            </button>
            <button className="btn-secondary" style={{ height: '30px', padding: '4px 10px', fontSize: '12px' }} onClick={() => setSelectedFolder(defaultFolders.documents)}>
              Documents
            </button>
            <button className="btn-secondary" style={{ height: '30px', padding: '4px 10px', fontSize: '12px' }} onClick={() => setSelectedFolder(defaultFolders.pictures)}>
              Pictures
            </button>
            <button className="btn-secondary" style={{ height: '30px', padding: '4px 10px', fontSize: '12px' }} onClick={onFileUploadClick}>
              <Upload size={14} /> Upload Files
            </button>
          </div>
        )}
      </div>

      {/* Recent Files Table */}
      <div className="glass-card" style={{ padding: '20px', borderRadius: 'var(--rounded-sm)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '16.5px', fontWeight: 600, color: 'var(--text-primary)' }}>Recently Sorted Files</h3>
          <button className="btn-secondary" style={{ height: '30px', padding: '4px 10px', fontSize: '12px' }} onClick={onNavigateHistory}>
            View All History →
          </button>
        </div>

        {recentMoves.length === 0 ? (
          <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '13.2px' }}>
            No recent file activity yet. Select a directory above to start organizing.
          </div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '13.2px' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-card)', color: 'var(--text-muted)', fontSize: '12px', fontFamily: 'var(--font-heading)', fontWeight: 600, textTransform: 'uppercase' }}>
                <th style={{ padding: '10px 12px' }}>File Name</th>
                <th style={{ padding: '10px 12px' }}>Folder Category</th>
                <th style={{ padding: '10px 12px', textAlign: 'right' }}>Time</th>
              </tr>
            </thead>
            <tbody>
              {recentMoves.map((file, i) => (
                <tr key={i} style={{ borderBottom: '1px solid var(--border-card)' }}>
                  <td style={{ padding: '10px 12px', fontWeight: 500, color: 'var(--text-primary)' }}>{file.name}</td>
                  <td style={{ padding: '10px 12px' }}>
                    <span className="badge" style={{ backgroundColor: 'rgb(217, 241, 225)', color: 'var(--colors-link)' }}>
                      {file.category}
                    </span>
                  </td>
                  <td style={{ padding: '10px 12px', textAlign: 'right', color: 'var(--text-muted)' }}>{file.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
