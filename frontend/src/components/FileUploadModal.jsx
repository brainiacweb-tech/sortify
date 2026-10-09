import React, { useState } from 'react';
import { Upload, X, Play } from 'lucide-react';
import confetti from 'canvas-confetti';
import logoImg from '../assets/logo.png';
import { API_BASE } from '../apiConfig';

export default function FileUploadModal({ isOpen, onClose, onOrganizeUploaded }) {
  if (!isOpen) return null;

  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const handleFileDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setSelectedFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleExecuteUploadOrganize = async () => {
    if (selectedFiles.length === 0 || isProcessing) return;
    setIsProcessing(true);

    try {
      const formData = new FormData();
      for (const f of selectedFiles) {
        formData.append('files', f);
      }

      // Step 1: Save this upload batch to its own folder
      const uploadRes = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData
      });
      const uploadData = await uploadRes.json();

      if (!uploadRes.ok) {
        throw new Error(uploadData.error || 'Upload failed');
      }

      // Step 2: Scan only this upload batch
      const scanRes = await fetch(`${API_BASE}/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder: uploadData.target_directory, recursive: false, check_duplicates: true })
      });
      const scanData = await scanRes.json();

      // Step 3: Organize the uploaded files
      if (scanRes.ok && scanData.items && scanData.items.length > 0) {
        const orgRes = await fetch(`${API_BASE}/organize`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        const orgData = await orgRes.json();

        if (orgRes.ok) {
          confetti({ particleCount: 80, spread: 60 });
          alert(`Successfully uploaded & organized ${orgData.total_successful} files into categorized folders!`);
        }
      } else {
        alert(`Uploaded ${uploadData.saved_count} files to ${uploadData.target_directory}!`);
      }

      setIsProcessing(false);
      if (onOrganizeUploaded) onOrganizeUploaded(selectedFiles.length);
      onClose();
    } catch (err) {
      setIsProcessing(false);
      alert('Upload / Organize Error: ' + err.message);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(15, 23, 42, 0.6)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div className="glass-card animate-fade-in" style={{
        width: '90%',
        maxWidth: '620px',
        padding: '24px',
        position: 'relative',
        borderRadius: 'var(--rounded-sm)'
      }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              padding: '6px 12px',
              borderRadius: 'var(--rounded-sm)',
              backgroundColor: 'var(--colors-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <img src={logoImg} alt="Sortify" style={{ height: '22px', objectFit: 'contain' }} />
            </div>
            <div>
              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '16.5px', fontWeight: 600, color: 'var(--text-primary)' }}>Upload Files to Organize</h3>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', color: 'var(--text-muted)' }}>Drag and drop files to categorize and sort instantly</p>
            </div>
          </div>
          <button onClick={onClose} style={{ border: 'none', background: 'transparent', cursor: 'pointer', color: 'var(--text-muted)' }}>
            <X size={20} />
          </button>
        </div>

        {/* Drag & Drop Target Area */}
        <label
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleFileDrop}
          style={{
            border: '2px dashed var(--colors-primary)',
            borderRadius: 'var(--rounded-sm)',
            padding: '28px 20px',
            textAlign: 'center',
            backgroundColor: 'rgb(217, 241, 225)',
            marginBottom: '20px',
            cursor: 'pointer',
            display: 'block'
          }}
        >
          <input type="file" multiple onChange={handleFileChange} style={{ display: 'none' }} />
          <Upload size={32} color="var(--colors-link)" style={{ marginBottom: '8px' }} />
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '13.2px', fontWeight: 500, color: 'var(--text-primary)' }}>
            {selectedFiles.length > 0 ? `${selectedFiles.length} file(s) selected` : 'Drag & drop files here, or click to browse'}
          </p>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>Supports Documents, Images, Spreadsheets, Code, Archives & more</p>
        </label>

        {/* Selected Files Table */}
        {selectedFiles.length > 0 && (
          <div style={{ maxHeight: '160px', overflowY: 'auto', marginBottom: '20px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13.2px' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-card)', color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: '12px' }}>
                  <th style={{ padding: '8px 12px', textAlign: 'left' }}>File Name</th>
                  <th style={{ padding: '8px 12px', textAlign: 'left' }}>Size</th>
                </tr>
              </thead>
              <tbody>
                {selectedFiles.map((f, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid var(--border-card)' }}>
                    <td style={{ padding: '8px 12px', fontWeight: 500, color: 'var(--text-primary)' }}>{f.name}</td>
                    <td style={{ padding: '8px 12px', color: 'var(--text-muted)' }}>{(f.size / (1024 * 1024)).toFixed(2)} MB</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Actions */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleExecuteUploadOrganize} disabled={isProcessing || selectedFiles.length === 0}>
            <Play size={16} />
            <span>{isProcessing ? 'Processing Files...' : 'Upload & Organize Files'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
