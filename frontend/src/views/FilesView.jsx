import React, { useState, useEffect, useRef } from 'react';
import { 
  Folder, 
  File, 
  Trash2, 
  Archive, 
  Lock, 
  Eye, 
  EyeOff, 
  Copy, 
  Move, 
  Edit3, 
  CornerUpLeft, 
  ChevronRight, 
  Search, 
  MoreVertical, 
  FileText, 
  Image, 
  Code, 
  Music, 
  Film, 
  Cpu, 
  CheckSquare, 
  Square,
  ExternalLink,
  ShieldCheck
} from 'lucide-react';
import { API_BASE } from '../apiConfig';

export default function FilesView({ initialFolder }) {
  const [currentFolder, setCurrentFolder] = useState(initialFolder || '');
  const [parentFolder, setParentFolder] = useState('');
  const [isProtected, setIsProtected] = useState(false);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedPaths, setSelectedPaths] = useState([]);
  const [filterQuery, setFilterQuery] = useState('');
  
  // Context Menu State
  const [contextMenu, setContextMenu] = useState(null); // { x, y, item }
  
  // Modals state
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false);
  const [zipPassword, setZipPassword] = useState('');
  const [zipArchiveName, setZipArchiveName] = useState('Archive.zip');

  const contextRef = useRef(null);

  useEffect(() => {
    loadFiles(currentFolder);
  }, [currentFolder]);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (contextRef.current && !contextRef.current.contains(e.target)) {
        setContextMenu(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const loadFiles = async (folder) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/files/list?folder=${encodeURIComponent(folder)}`);
      const data = await res.json();
      if (data && data.items) {
        setItems(data.items);
        setCurrentFolder(data.current_folder);
        setParentFolder(data.parent_folder);
        setIsProtected(data.is_protected || false);
        setSelectedPaths([]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSelectAll = () => {
    if (selectedPaths.length === filteredItems.length) {
      setSelectedPaths([]);
    } else {
      setSelectedPaths(filteredItems.map(i => i.path));
    }
  };

  const handleToggleSelect = (path) => {
    setSelectedPaths(prev => 
      prev.includes(path) ? prev.filter(p => p !== path) : [...prev, path]
    );
  };

  const handleAction = async (action, extraData = {}) => {
    const targets = extraData.paths || (selectedPaths.length > 0 ? selectedPaths : (contextMenu ? [contextMenu.item.path] : []));
    if (!targets || targets.length === 0) {
      alert("Please select at least one file or folder first.");
      return;
    }

    setContextMenu(null);

    try {
      const res = await fetch(`${API_BASE}/files/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action,
          paths: targets,
          destination: extraData.destination || currentFolder,
          password: extraData.password || zipPassword,
          new_name: extraData.new_name
        })
      });
      const data = await res.json();
      if (data.error) {
        alert(`Action Error: ${data.error}`);
      } else {
        setIsPasswordModalOpen(false);
        setZipPassword('');
        loadFiles(currentFolder);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleContextMenu = (e, item) => {
    e.preventDefault();
    setContextMenu({
      x: e.clientX,
      y: e.clientY,
      item
    });
  };

  const getFileIcon = (cat, isDir) => {
    if (isDir) return <Folder size={18} color="#F59E0B" />;
    switch (cat.toLowerCase()) {
      case 'documents': return <FileText size={18} color="#3B82F6" />;
      case 'images': return <Image size={18} color="#EC4899" />;
      case 'code': return <Code size={18} color="#8B5CF6" />;
      case 'audio': return <Music size={18} color="#F59E0B" />;
      case 'videos': return <Film size={18} color="#EF4444" />;
      case 'executables': return <Cpu size={18} color="#6366F1" />;
      case 'archives': return <Archive size={18} color="#10B981" />;
      default: return <File size={18} color="var(--text-muted)" />;
    }
  };

  const filteredItems = items.filter(item => 
    item.name.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header Title & Protection Warning */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
            Files Management Utility
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
            Browse, Move, Copy, ZIP, Password Encrypt, Hide, or Recycle files with safety-first preview.
          </p>
        </div>

        {isProtected && (
          <div style={{
            padding: '6px 12px',
            borderRadius: 'var(--rounded-sm)',
            backgroundColor: '#FEF2F2',
            border: '1px solid #EF4444',
            color: '#DC2626',
            fontSize: '12px',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <ShieldCheck size={16} />
            <span>Protected System Location</span>
          </div>
        )}
      </div>

      {/* Navigation Breadcrumb Bar & Quick Filter */}
      <div className="glass-card" style={{ padding: '12px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flex: 1, overflow: 'hidden' }}>
          <button 
            disabled={currentFolder === parentFolder}
            onClick={() => loadFiles(parentFolder)}
            className="btn-secondary"
            style={{ padding: '6px 10px', height: '32px' }}
            title="Go Up One Folder Level"
          >
            <CornerUpLeft size={16} />
          </button>
          <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
            {currentFolder}
          </span>
        </div>

        <div style={{ position: 'relative', width: '220px' }}>
          <Search size={14} color="var(--text-muted)" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)' }} />
          <input 
            type="text"
            value={filterQuery}
            onChange={(e) => setFilterQuery(e.target.value)}
            placeholder="Filter files..."
            style={{
              width: '100%',
              height: '32px',
              padding: '4px 10px 4px 30px',
              borderRadius: 'var(--rounded-sm)',
              border: '1px solid var(--border-card)',
              backgroundColor: 'var(--bg-dark)',
              color: 'var(--text-primary)',
              fontSize: '12px',
              outline: 'none'
            }}
          />
        </div>
      </div>

      {/* Bulk Action Toolbar */}
      {selectedPaths.length > 0 && (
        <div className="glass-card" style={{ padding: '10px 16px', backgroundColor: '#F3FFF7', borderColor: 'var(--colors-primary)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '12.5px', fontWeight: 700, color: 'var(--colors-link)' }}>
            {selectedPaths.length} item(s) selected
          </span>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="btn-secondary" style={{ height: '32px', fontSize: '12px' }} onClick={() => handleAction('zip')}>
              <Archive size={14} /> ZIP
            </button>
            <button className="btn-secondary" style={{ height: '32px', fontSize: '12px' }} onClick={() => setIsPasswordModalOpen(true)}>
              <Lock size={14} /> Password ZIP
            </button>
            <button className="btn-secondary" style={{ height: '32px', fontSize: '12px' }} onClick={() => handleAction('hide')}>
              <EyeOff size={14} /> Hide
            </button>
            <button className="btn-secondary" style={{ height: '32px', fontSize: '12px' }} onClick={() => handleAction('unhide')}>
              <Eye size={14} /> Unhide
            </button>
            <button className="btn-orange" style={{ height: '32px', fontSize: '12px' }} onClick={() => handleAction('recycle')}>
              <Trash2 size={14} /> Recycle Bin
            </button>
          </div>
        </div>
      )}

      {/* Files Table Explorer View */}
      <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ backgroundColor: 'var(--bg-dark)', borderBottom: '1px solid var(--border-card)', fontSize: '12px', fontWeight: 700, color: 'var(--text-secondary)' }}>
              <th style={{ padding: '12px 16px', width: '40px' }}>
                <div onClick={handleToggleSelectAll} style={{ cursor: 'pointer' }}>
                  {selectedPaths.length > 0 && selectedPaths.length === filteredItems.length ? <CheckSquare size={16} color="var(--colors-primary)" /> : <Square size={16} color="var(--text-muted)" />}
                </div>
              </th>
              <th style={{ padding: '12px 16px' }}>Name</th>
              <th style={{ padding: '12px 16px' }}>Size</th>
              <th style={{ padding: '12px 16px' }}>Date Modified</th>
              <th style={{ padding: '12px 16px' }}>Category</th>
              <th style={{ padding: '12px 16px', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading folder contents...</td>
              </tr>
            ) : filteredItems.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>No files or folders found.</td>
              </tr>
            ) : (
              filteredItems.map((item) => {
                const isSelected = selectedPaths.includes(item.path);
                return (
                  <tr 
                    key={item.path}
                    onContextMenu={(e) => handleContextMenu(e, item)}
                    style={{
                      borderBottom: '1px solid var(--border-card)',
                      backgroundColor: isSelected ? 'var(--bg-card-hover)' : 'transparent',
                      opacity: item.is_hidden ? 0.55 : 1,
                      transition: 'background-color 0.15s ease'
                    }}
                  >
                    <td style={{ padding: '10px 16px' }}>
                      <div onClick={() => handleToggleSelect(item.path)} style={{ cursor: 'pointer' }}>
                        {isSelected ? <CheckSquare size={16} color="var(--colors-primary)" /> : <Square size={16} color="var(--text-muted)" />}
                      </div>
                    </td>
                    <td style={{ padding: '10px 16px' }}>
                      <div 
                        onClick={() => item.is_dir && setCurrentFolder(item.path)}
                        style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: item.is_dir ? 'pointer' : 'default' }}
                      >
                        {getFileIcon(item.category, item.is_dir)}
                        <span style={{ fontWeight: item.is_dir ? 700 : 500, color: 'var(--text-primary)', fontSize: '13px' }}>
                          {item.name}
                        </span>
                        {item.is_hidden && <span style={{ fontSize: '10px', padding: '1px 5px', borderRadius: '2px', backgroundColor: 'var(--border-card)', color: 'var(--text-muted)' }}>Hidden</span>}
                      </div>
                    </td>
                    <td style={{ padding: '10px 16px', fontSize: '12.5px', color: 'var(--text-secondary)' }}>
                      {item.is_dir ? '—' : item.size}
                    </td>
                    <td style={{ padding: '10px 16px', fontSize: '12.5px', color: 'var(--text-muted)' }}>
                      {item.mtime}
                    </td>
                    <td style={{ padding: '10px 16px' }}>
                      <span style={{ fontSize: '11px', fontWeight: 600, textTransform: 'capitalize', color: 'var(--colors-link)', backgroundColor: '#F3FFF7', padding: '2px 8px', borderRadius: '4px' }}>
                        {item.category}
                      </span>
                    </td>
                    <td style={{ padding: '10px 16px', textAlign: 'right' }}>
                      <button 
                        onClick={(e) => handleContextMenu(e, item)}
                        style={{ border: 'none', background: 'transparent', cursor: 'pointer', color: 'var(--text-muted)', padding: '4px' }}
                      >
                        <MoreVertical size={16} />
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Right Click Context Menu */}
      {contextMenu && (
        <div 
          ref={contextRef}
          style={{
            position: 'fixed',
            top: contextMenu.y,
            left: contextMenu.x,
            zIndex: 3000,
            backgroundColor: 'var(--bg-card)',
            border: '1px solid var(--border-card)',
            borderRadius: 'var(--rounded-sm)',
            boxShadow: 'var(--card-shadow-hover)',
            padding: '6px 0',
            minWidth: '200px'
          }}
        >
          <div className="menu-option" style={{ padding: '6px 14px', cursor: 'pointer', fontSize: '12.5px' }} onClick={() => handleAction('rename', { paths: [contextMenu.item.path], new_name: prompt("New Name:", contextMenu.item.name) })}>
            Rename
          </div>
          <div className="menu-option" style={{ padding: '6px 14px', cursor: 'pointer', fontSize: '12.5px' }} onClick={() => handleAction('zip', { paths: [contextMenu.item.path], destination: contextMenu.item.path + '.zip' })}>
            Compress to ZIP
          </div>
          {contextMenu.item.name.endsWith('.zip') && (
            <div className="menu-option" style={{ padding: '6px 14px', cursor: 'pointer', fontSize: '12.5px' }} onClick={() => handleAction('extract', { paths: [contextMenu.item.path], destination: currentFolder })}>
              Extract ZIP
            </div>
          )}
          <div className="menu-option" style={{ padding: '6px 14px', cursor: 'pointer', fontSize: '12.5px' }} onClick={() => handleAction(contextMenu.item.is_hidden ? 'unhide' : 'hide', { paths: [contextMenu.item.path] })}>
            {contextMenu.item.is_hidden ? 'Unhide Item' : 'Hide Item'}
          </div>
          <div style={{ height: '1px', backgroundColor: 'var(--border-card)', margin: '4px 0' }} />
          <div className="menu-option" style={{ padding: '6px 14px', cursor: 'pointer', fontSize: '12.5px', color: '#DC2626' }} onClick={() => handleAction('recycle', { paths: [contextMenu.item.path] })}>
            Move to Recycle Bin
          </div>
        </div>
      )}

      {/* Password ZIP Modal */}
      {isPasswordModalOpen && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 3500, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="glass-card" style={{ width: '380px', padding: '24px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 800, marginBottom: '12px' }}>Password Encrypted ZIP</h3>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '16px' }}>Set AES encryption password for the created archive.</p>
            <input 
              type="text"
              value={zipArchiveName}
              onChange={(e) => setZipArchiveName(e.target.value)}
              placeholder="Archive Name..."
              style={{ width: '100%', height: '36px', padding: '8px', marginBottom: '12px', borderRadius: '4px', border: '1px solid var(--border-card)' }}
            />
            <input 
              type="password"
              value={zipPassword}
              onChange={(e) => setZipPassword(e.target.value)}
              placeholder="Encryption Password..."
              style={{ width: '100%', height: '36px', padding: '8px', marginBottom: '16px', borderRadius: '4px', border: '1px solid var(--border-card)' }}
            />
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
              <button className="btn-secondary" onClick={() => setIsPasswordModalOpen(false)}>Cancel</button>
              <button className="btn-primary" onClick={() => handleAction('zip', { destination: currentFolder + '/' + zipArchiveName })}>Create Encrypted ZIP</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
