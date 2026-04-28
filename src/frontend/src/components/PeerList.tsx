import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

interface Peer {
  id: number;
  name: str;
  endpoint: str;
  public_key: str;
  is_active: boolean;
}

const PeerList: React.FC = () => {
  const [peers, setPeers] = useState<Peer[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  const fetchPeers = async () => {
    const list: any = await invoke('get_peers');
    setPeers(list);
  };

  useEffect(() => {
    fetchPeers();
  }, []);

  const handleConnect = async (id: number) => {
    await invoke('connect_vpn', { peerId: id });
  };

  return (
    <div className="peer-list p-6 bg-gray-900 text-white min-h-[400px]">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Peers & Servers</h2>
        <div className="space-x-2">
            <button 
                onClick={() => setShowAddModal(true)}
                className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm"
            >
                + Add Peer
            </button>
            <button 
                className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg text-sm"
                onClick={async () => {
                    // Logic to open file picker and import
                }}
            >
                Import .conf
            </button>
        </div>
      </div>

      <div className="space-y-3">
        {peers.map(peer => (
          <div key={peer.id} className="peer-item bg-gray-800 p-4 rounded-lg flex justify-between items-center hover:bg-gray-750 transition-colors">
            <div>
              <p className="font-semibold">{peer.name}</p>
              <p className="text-xs text-gray-400">{peer.endpoint}</p>
            </div>
            <button 
              onClick={() => handleConnect(peer.id)}
              className={`px-4 py-1 rounded-full text-sm font-medium ${peer.is_active ? 'bg-green-600' : 'bg-gray-700 hover:bg-gray-600'}`}
            >
              {peer.is_active ? 'Connected' : 'Connect'}
            </button>
          </div>
        ))}
        {peers.length === 0 && (
          <div className="text-center py-10 text-gray-500">
            No peers found. Add one or import a config.
          </div>
        )}
      </div>
    </div>
  );
};

export default PeerList;
