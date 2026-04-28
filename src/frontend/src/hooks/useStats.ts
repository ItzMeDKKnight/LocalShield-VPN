import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

export function useStats() {
  const [stats, setStats] = useState({
    uptime: 0,
    upload_speed: 0,
    download_speed: 0,
    total_sent: 0,
    total_recv: 0
  });

  const fetchStats = async () => {
    try {
      const res: any = await invoke('get_backend_status');
      if (res.stats) {
        setStats(res.stats);
      }
    } catch (err) {
      console.error("Failed to fetch stats", err);
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchStats, 1000);
    return () => clearInterval(interval);
  }, []);

  return stats;
}
