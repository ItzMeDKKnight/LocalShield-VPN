import React from 'react';
import { useVPNStatus } from '../hooks/useVPNStatus';
import { useStats } from '../hooks/useStats';
import { invoke } from '@tauri-apps/api/tauri';

const Dashboard: React.FC = () => {
  const status = useVPNStatus();
  const stats = useStats();

  const handleToggle = async () => {
    if (status.connected) {
      await invoke('disconnect_vpn');
    } else {
      // For simplicity, connect to the first available peer if any
      await invoke('connect_vpn', { peerId: 1 });
    }
  };

  const formatSpeed = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B/s`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB/s`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB/s`;
  };

  const latencyColor = (ms: number) => {
    if (ms < 0) return 'text-gray-400';
    if (ms < 50) return 'text-green-500';
    if (ms < 150) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <div className="dashboard p-6 bg-gray-900 text-white rounded-xl shadow-2xl">
      <div className="flex flex-col items-center justify-center space-y-8">
        <div className={`status-indicator w-48 h-48 rounded-full flex items-center justify-center border-4 ${status.connected ? 'border-green-500 shadow-[0_0_20px_rgba(34,197,94,0.5)] animate-pulse' : 'border-gray-600'}`}>
          <button 
            onClick={handleToggle}
            className={`w-40 h-40 rounded-full text-2xl font-bold transition-all duration-300 ${status.connected ? 'bg-green-600 hover:bg-green-700' : 'bg-gray-700 hover:bg-gray-600'}`}
          >
            {status.connected ? 'CONNECTED' : 'CONNECT'}
          </button>
        </div>

        <div className="stats-grid grid grid-cols-2 gap-4 w-full">
          <div className="stat-card bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Download</p>
            <p className="text-2xl font-mono">{formatSpeed(stats.download_speed)}</p>
          </div>
          <div className="stat-card bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Upload</p>
            <p className="text-2xl font-mono">{formatSpeed(stats.upload_speed)}</p>
          </div>
          <div className="stat-card bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Latency</p>
            <p className={`text-2xl font-mono ${latencyColor(status.latency)}`}>
              {status.latency >= 0 ? `${status.latency.toFixed(0)} ms` : '--'}
            </p>
          </div>
          <div className="stat-card bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Uptime</p>
            <p className="text-2xl font-mono">{new Date(stats.uptime * 1000).toISOString().substr(11, 8)}</p>
          </div>
        </div>
        
        <div className="current-peer text-center">
            <p className="text-gray-400">Current Peer</p>
            <p className="text-xl font-semibold">{status.peer || 'None'}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
