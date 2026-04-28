import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import PeerList from './components/PeerList';
import Settings from './components/Settings';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="app-container min-h-screen bg-gray-950 text-white flex flex-col">
      <header className="p-4 bg-gray-900 border-b border-gray-800 flex justify-between items-center">
        <h1 className="text-xl font-black tracking-tighter text-blue-500">LOCALSHIELD <span className="text-white">VPN</span></h1>
        <nav className="flex space-x-4">
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`px-3 py-1 rounded-md transition-all ${activeTab === 'dashboard' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}
          >
            Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('peers')}
            className={`px-3 py-1 rounded-md transition-all ${activeTab === 'peers' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}
          >
            Peers
          </button>
          <button 
            onClick={() => setActiveTab('settings')}
            className={`px-3 py-1 rounded-md transition-all ${activeTab === 'settings' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}
          >
            Settings
          </button>
        </nav>
      </header>

      <main className="flex-1 overflow-auto">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'peers' && <PeerList />}
        {activeTab === 'settings' && <Settings />}
      </main>

      <footer className="p-2 bg-gray-900 border-t border-gray-800 text-[10px] text-center text-gray-500">
        LocalShield VPN - Fully Encrypted & Decentralized
      </footer>
    </div>
  );
}

export default App;
