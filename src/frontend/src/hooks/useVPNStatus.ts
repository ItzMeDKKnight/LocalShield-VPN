import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

export function useVPNStatus() {
  const [status, setStatus] = useState({ connected: false, peer: null, latency: -1 });

  const fetchStatus = async () => {
    try {
      const res: any = await invoke('get_backend_status');
      setStatus(res);
    } catch (err) {
      console.error("Failed to fetch status", err);
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  return status;
}
