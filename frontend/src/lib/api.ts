// API client — typed wrappers for all Shelfie backend endpoints
// Vite's dev proxy routes /api/* → http://localhost:8000
const API_BASE = import.meta.env.VITE_API_URL ?? '';

export type BookStatus = 'correct' | 'misplaced' | 'missing' | 'unknown';

export interface BoundingBox {
  x: number; y: number; w: number; h: number;
}

export interface DetectedBook {
  id: string;
  book_id: string | null;
  ocr_text: string;
  matched_title: string;
  matched_author: string;
  confidence: number;
  status: BookStatus;
  bbox: BoundingBox;
  detected_position: number;
  expected_position: number;
  genre: string;
  cover_url: string;
  color: string;
}

export interface ScanResponse {
  scan_id: string;
  shelf_id: string | null;
  detected_books: DetectedBook[];
  shelf_score: number;
  message: string;
}

export interface Book {
  id: string;
  shelf_id: string;
  title: string;
  author: string;
  genre: string;
  isbn: string;
  cover_url: string;
  position: number;
  color: string;
}

export interface Shelf {
  id: string;
  name: string;
  sort_rule: string;
}

export interface InventoryResponse {
  shelf: Shelf;
  books: Book[];
}

export interface RecommendationOut {
  book_id: string;
  title: string;
  current_position: number;
  ideal_shelf_id: string;
  ideal_shelf_name: string;
  ideal_position: number;
  instruction: string;
  neighbor_left: string | null;
  neighbor_right: string | null;
}

export interface GenreCount {
  genre: string;
  count: number;
}

export interface ShelfHealth {
  shelf_id: string;
  shelf_name: string;
  total_books: number;
  correct_count: number;
  misplaced_count: number;
  missing_count: number;
  unknown_count: number;
  shelf_score: number;
  genre_distribution: GenreCount[];
  sort_rule: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...init?.headers },
    ...init,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API ${res.status}: ${err}`);
  }
  return res.json();
}

export const api = {
  async scanShelf(file: File, shelfId = 'demo-shelf-001'): Promise<ScanResponse> {
    const form = new FormData();
    form.append('file', file);
    const res = await fetch(`${API_BASE}/api/scan?shelf_id=${shelfId}`, {
      method: 'POST',
      body: form,
    });
    if (!res.ok) throw new Error(`Scan failed: ${await res.text()}`);
    return res.json();
  },

  async getInventory(shelfId: string): Promise<InventoryResponse> {
    return request(`/api/inventory/${shelfId}`);
  },

  async getRecommendation(bookId: string, currentPos?: number): Promise<RecommendationOut> {
    const q = currentPos !== undefined ? `?current_position=${currentPos}` : '';
    return request(`/api/recommend/${bookId}${q}`);
  },

  async getShelfHealth(shelfId: string): Promise<ShelfHealth> {
    return request(`/api/shelf-health/${shelfId}`);
  },

  async listShelves(): Promise<Shelf[]> {
    return request('/api/inventory');
  },
};
