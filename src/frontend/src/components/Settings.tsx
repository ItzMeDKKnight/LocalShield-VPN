import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

const Settings: React.FC = () => {
  const [killSwitch, setKillSwitch] = useState(false);
  const [dnsProvider, setDnsProvider] = useState('cloudflare');

  const handleKillSwitch = async (val: boolean) => {
    setKillSwitch(val);
    await invoke('toggle_killswitch', { enabled: val });
  };

  const handleDns = async (provider: string) => {
    setDnsProvider(provider);
    await invoke('toggle_dns', { enabled: true, provider });
  };

  return (
    <div className="settings p-6 bg-gray-900 text-white space-y-8">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>

      <div className="setting-item flex justify-between items-center p-4 bg-gray-800 rounded-lg">
        <div>
          <p className="font-semibold">Network Kill Switch</p>
          <p className="text-sm text-gray-400">Block all traffic if VPN disconnects</p>
        </div>
        <input 
          type="checkbox" 
          checked={killSwitch}
          onChange={(e) => handleKillSwitch(e.target.checked)}
          className="w-6 h-6 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
      </div>

      <div className="setting-item p-4 bg-gray-800 rounded-lg">
        <p className="font-semibold mb-2">DNS Protection (DoH)</p>
        <select 
          value={dnsProvider}
          onChange={(e) => handleDns(e.target.value)}
          className="w-full bg-gray-700 border-none rounded-lg p-2 text-white"
        >
          <option value="cloudflare">Cloudflare (1.1.1.1)</option>
          <option value="google">Google (8.8.8.8)</option>
          <option value="custom">Custom DoH URL</option>
        </select>
      </div>

      <div className="log-viewer bg-black p-4 rounded-lg h-40 overflow-y-auto font-mono text-xs text-green-400">
        <p>[INFO] App started...</p>
        <p>[INFO] Loaded 3 peers from encrypted DB</p>
        <p>[INFO] Private key retrieved from keychain</p>
        {/* Real logs would be streamed here */}
      </div>

      <div className="version-info text-center text-gray-500 text-xs">
        LocalShield VPN v1.0.0 (Alpha)
      </div>
    </div>
  );
};

export default Settings;
