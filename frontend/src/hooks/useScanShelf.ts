import { useState, useCallback } from 'react';
import { api } from '../lib/api';
import type { ScanResponse } from '../lib/api';

type ScanState = 'idle' | 'scanning' | 'done' | 'error';

export function useScanShelf() {
  const [state, setState] = useState<ScanState>('idle');
  const [result, setResult] = useState<ScanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);

  const scan = useCallback(async (file: File) => {
    setState('scanning');
    setError(null);
    setProgress(0);

    // Animate progress for UX feedback
    const progressInterval = setInterval(() => {
      setProgress((p: number) => Math.min(p + (p < 70 ? 15 : p < 90 ? 5 : 1), 95));
    }, 400);

    try {
      const res = await api.scanShelf(file);
      clearInterval(progressInterval);
      setProgress(100);
      await new Promise(r => setTimeout(r, 300)); // brief hold at 100%
      setResult(res);
      setState('done');
    } catch (err) {
      clearInterval(progressInterval);
      setError(err instanceof Error ? err.message : 'Scan failed');
      setState('error');
    }
  }, []);

  const reset = useCallback(() => {
    setState('idle');
    setResult(null);
    setError(null);
    setProgress(0);
  }, []);

  return { state, result, error, progress, scan, reset };
}
