import { useState, useEffect } from 'react';
import { api } from '../lib/api';
import type { InventoryResponse } from '../lib/api';

export function useInventory(shelfId: string | null) {
  const [data, setData] = useState<InventoryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!shelfId) return;
    setLoading(true);
    api.getInventory(shelfId)
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [shelfId]);

  return { data, loading, error };
}
