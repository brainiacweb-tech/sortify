import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import MenuBar from './components/MenuBar';
import FileUploadModal from './components/FileUploadModal';
import AboutModal from './components/AboutModal';
import WelcomeModal from './components/WelcomeModal';
import DashboardView from './views/DashboardView';
import OrganizeView from './views/OrganizeView';
import DuplicatesView from './views/DuplicatesView';
import HistoryView from './views/HistoryView';
import RulesView from './views/RulesView';
import BulkRenameView from './views/BulkRenameView';
import SettingsView from './views/SettingsView';
import UserGuideView from './views/UserGuideView';
import FilesView from './views/FilesView';
import StorageView from './views/StorageView';

import { API_BASE } from './apiConfig';

export default function App() {
  const params = new URLSearchParams(window.location.search);
  const [activeTab, setActiveTab] = useState(params.get('tab') || 'dashboard');
  const [searchQuery, setSearchQuery] = useState('');
  const [theme, setTheme] = useState(params.get('theme') || 'light');
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [isAboutModalOpen, setIsAboutModalOpen] = useState(false);
  const [isWelcomeModalOpen, setIsWelcomeModalOpen] = useState(false);
  const [selectedFolder, setSelectedFolder] = useState('');
  const [userInfo, setUserInfo] = useState({ name: 'User', initials: 'US' });

  useEffect(() => {
    if (localStorage.getItem('sortify_welcomed') !== 'true') {
      setIsWelcomeModalOpen(true);
    }
  }, []);

  const [stats, setStats] = useState({
    total_files_organized: 0,
    total_runs: 0,
    duplicates_found: 0,
    category_breakdown: {}
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    fetch(`${API_BASE}/stats`)
      .then(res => res.json())
      .then(data => {
        if (data) setStats(data);
      })
      .catch(() => {});

    fetch(`${API_BASE}/default-folders`)
      .then(res => res.json())
      .then(data => {
        if (data && data.downloads) {
          setSelectedFolder(data.downloads);
        }
      })
      .catch(() => {});

    fetch(`${API_BASE}/user-info`)
      .then(res => res.json())
      .then(data => {
        if (data && data.name) {
          setUserInfo(data);
        }
      })
      .catch(() => {});
  }, []);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleShowAbout = () => {
    setIsAboutModalOpen(true);
  };

  const handleOrganizeUploaded = (count) => {
    setStats(prev => ({
      ...prev,
      total_files_organized: prev.total_files_organized + count,
      total_runs: prev.total_runs + 1
    }));
  };

  const handleSelectFolderViaMenu = async () => {
    try {
      if (window.pywebview && window.pywebview.api && window.pywebview.api.select_folder) {
        const res = await window.pywebview.api.select_folder(selectedFolder || '');
        if (res && res.folder) {
          setSelectedFolder(res.folder);
          return;
        }
      }
      const res = await fetch(`${API_BASE}/select-folder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initial: selectedFolder })
      });
      const data = await res.json();
      if (data && data.folder) {
        setSelectedFolder(data.folder);
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', backgroundColor: 'var(--bg-dark)', position: 'relative', overflow: 'hidden' }}>
      {/* Artistic Brand Green Rotating Circular Maze Overlay System */}
      <div className="bg-maze-overlay">
        <div className="maze-watermark-art-primary" />
        <div className="maze-watermark-art-secondary" />
      </div>

      {/* Top Application Menu Bar */}
      <MenuBar 
        setActiveTab={setActiveTab}
        onSelectFolder={handleSelectFolderViaMenu}
        onUploadClick={() => setIsUploadModalOpen(true)}
        toggleTheme={toggleTheme}
        theme={theme}
        onShowAbout={handleShowAbout}
      />

      <div style={{ display: 'flex', flex: 1, position: 'relative', zIndex: 1 }}>
        {/* Sidebar Navigation */}
        <Sidebar 
          activeTab={activeTab} 
          setActiveTab={setActiveTab} 
          onShowAbout={handleShowAbout} 
          userInfo={userInfo}
        />

        {/* Main View Area */}
        <main style={{ flex: 1, padding: '24px 32px', overflowY: 'auto' }}>
          <Header 
            searchQuery={searchQuery} 
            setSearchQuery={setSearchQuery} 
            theme={theme} 
            toggleTheme={toggleTheme} 
            onFileUploadClick={() => setIsUploadModalOpen(true)}
            userInfo={userInfo}
          />

        {activeTab === 'dashboard' && (
          <DashboardView 
            selectedFolder={selectedFolder}
            setSelectedFolder={setSelectedFolder}
            onNavigateOrganize={() => setActiveTab('organize')}
            onNavigateDuplicates={() => setActiveTab('duplicates')}
            onNavigateHistory={() => setActiveTab('history')}
            onFileUploadClick={() => setIsUploadModalOpen(true)}
            stats={stats} 
          />
        )}
        {activeTab === 'organize' && (
          <OrganizeView 
            targetFolder={selectedFolder}
            setTargetFolder={setSelectedFolder}
            onActivityUpdated={() => setStats(prev => ({ ...prev, total_runs: prev.total_runs + 1 }))} 
          />
        )}
        {activeTab === 'files' && (
          <FilesView 
            initialFolder={selectedFolder}
          />
        )}
        {activeTab === 'duplicates' && (
          <DuplicatesView 
            targetDir={selectedFolder}
            setTargetDir={setSelectedFolder}
          />
        )}
        {activeTab === 'storage' && (
          <StorageView 
            targetFolder={selectedFolder}
          />
        )}
        {activeTab === 'history' && <HistoryView />}
        {activeTab === 'rules' && <RulesView />}
        {activeTab === 'rename' && (
          <BulkRenameView 
            targetFolder={selectedFolder}
            setTargetFolder={setSelectedFolder}
          />
        )}
        {activeTab === 'guide' && (
          <UserGuideView onNavigate={setActiveTab} />
        )}
        {activeTab === 'settings' && (
          <SettingsView 
            theme={theme} 
            setTheme={setTheme} 
            userInfo={userInfo} 
            setUserInfo={setUserInfo} 
          />
        )}
        </main>
      </div>

      {/* File Upload Modal */}
      <FileUploadModal 
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onOrganizeUploaded={handleOrganizeUploaded}
      />

      {/* About Modal */}
      <AboutModal 
        isOpen={isAboutModalOpen}
        onClose={() => setIsAboutModalOpen(false)}
      />

      {/* Welcome Onboarding Modal */}
      <WelcomeModal 
        isOpen={isWelcomeModalOpen}
        onClose={() => setIsWelcomeModalOpen(false)}
        onStartOrganizing={() => setActiveTab('organize')}
        onOpenGuide={() => setActiveTab('guide')}
      />
    </div>
  );
}
