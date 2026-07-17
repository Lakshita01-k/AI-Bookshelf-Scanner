import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, RotateCcw, LayoutDashboard, ListTodo, Layers } from 'lucide-react';

import { useScanShelf } from './hooks/useScanShelf';
import { api, ShelfHealth } from './lib/api';

import ShelfUploader from './components/ShelfUploader';
import ScanAnimation from './components/ScanAnimation';
import BookOverlay from './components/BookOverlay';
import BookDetailPanel from './components/BookDetailPanel';
import FixShelfMode from './components/FixShelfMode';
import ShelfHealthDashboard from './components/ShelfHealthDashboard';
import GenreChart from './components/GenreChart';

type Tab = 'books' | 'fix' | 'dashboard';

export default function App() {
  const { state, result, error, progress, scan, reset } = useScanShelf();
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [selectedBookId, setSelectedBookId] = useState<string | null>(null);
  const [tab, setTab] = useState<Tab>('books');
  const [health, setHealth] = useState<ShelfHealth | null>(null);

  // Load shelf health once scan is done
  useEffect(() => {
    if (state === 'done' && result?.shelf_id) {
      api.getShelfHealth(result.shelf_id).then(setHealth).catch(console.error);
    }
  }, [state, result?.shelf_id]);

  const handleFile = (file: File) => {
    const url = URL.createObjectURL(file);
    setImageUrl(url);
    scan(file);
  };

  const handleReset = () => {
    reset();
    setImageUrl(null);
    setSelectedBookId(null);
    setTab('books');
    setHealth(null);
  };

  // Bi-directional: clicking a bbox selects book in panel and vice versa
  const handleSelectBook = (id: string) => {
    setSelectedBookId(prev => prev === id ? null : id);
  };

  return (
    <>
      {/* ── Header ───────────────────────────────────────────────── */}
      <header className="app-header">
        <div className="app-logo">
          <div className="app-logo-icon">📚</div>
          <span className="app-logo-text">Shelf<span>ie</span></span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div className="demo-badge">
            <div className="dot" />
            Demo Mode
          </div>
          {state !== 'idle' && (
            <button className="btn btn-ghost btn-sm" onClick={handleReset} id="reset-btn">
              <RotateCcw size={14} />
              New Scan
            </button>
          )}
        </div>
      </header>

      {/* ── Main ─────────────────────────────────────────────────── */}
      <main className="main-content">
        <AnimatePresence mode="wait">

          {/* ── 1. Idle — Uploader ── */}
          {state === 'idle' && (
            <motion.div key="uploader" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <ShelfUploader onFile={handleFile} />
            </motion.div>
          )}

          {/* ── 2. Scanning ── */}
          {state === 'scanning' && imageUrl && (
            <motion.div key="scanning" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
              <div style={{ maxWidth: 800, margin: '0 auto' }}>
                <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
                  <h2>Scanning your bookshelf...</h2>
                  <p style={{ marginTop: '0.4rem' }}>
                    Our AI is reading every spine. Hang tight.
                  </p>
                </div>
                <ScanAnimation imageUrl={imageUrl} progress={progress} />
              </div>
            </motion.div>
          )}

          {/* ── 3. Error ── */}
          {state === 'error' && (
            <motion.div key="error" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              style={{ textAlign: 'center', padding: '4rem' }}
            >
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>😔</div>
              <h2 style={{ marginBottom: '0.5rem' }}>Scan Failed</h2>
              <p style={{ marginBottom: '2rem', color: 'var(--status-missing)' }}>{error}</p>
              <button className="btn btn-primary" onClick={handleReset}>Try Again</button>
            </motion.div>
          )}

          {/* ── 4. Done — Results ── */}
          {state === 'done' && result && imageUrl && (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {/* AI message banner */}
              <div className="ai-message" style={{ marginBottom: '1.25rem' }}>
                <span>🤖</span>
                <span>{result.message}</span>
              </div>

              {/* Tabs */}
              <div className="tabs" id="main-tabs">
                <button className={`tab ${tab === 'books' ? 'active' : ''}`} onClick={() => setTab('books')} id="tab-books">
                  <Layers size={14} style={{ display: 'inline', marginRight: 4 }} />
                  Books
                </button>
                <button className={`tab ${tab === 'fix' ? 'active' : ''}`} onClick={() => setTab('fix')} id="tab-fix">
                  <ListTodo size={14} style={{ display: 'inline', marginRight: 4 }} />
                  Fix My Shelf
                </button>
                <button className={`tab ${tab === 'dashboard' ? 'active' : ''}`} onClick={() => setTab('dashboard')} id="tab-dashboard">
                  <LayoutDashboard size={14} style={{ display: 'inline', marginRight: 4 }} />
                  Dashboard
                </button>
              </div>

              {/* ── Tab: Books ── */}
              <AnimatePresence mode="wait">
                {tab === 'books' && (
                  <motion.div
                    key="books-tab"
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="results-layout"
                  >
                    {/* Image + bounding boxes */}
                    <div>
                      <div className="scan-container" id="results-image-container">
                        <img src={imageUrl} alt="Scanned bookshelf" className="scan-image" />
                        <div className="scan-overlay" style={{ pointerEvents: 'auto' }}>
                          <BookOverlay
                            books={result.detected_books}
                            selectedId={selectedBookId}
                            onSelect={handleSelectBook}
                          />
                        </div>
                      </div>

                      {/* Legend */}
                      <div style={{ display: 'flex', gap: '1rem', marginTop: '0.75rem', flexWrap: 'wrap' }}>
                        {[
                          { color: 'var(--status-correct)', label: 'Correct' },
                          { color: 'var(--status-misplaced)', label: 'Misplaced' },
                          { color: 'var(--status-missing)', label: 'Missing' },
                          { color: 'var(--status-unknown)', label: 'Unknown' },
                        ].map(l => (
                          <div key={l.label} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                            <div style={{ width: 10, height: 10, borderRadius: 2, background: l.color }} />
                            {l.label}
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Side panel */}
                    <div className="card" style={{ padding: '1.25rem' }}>
                      <h4 style={{ marginBottom: '1rem', paddingBottom: '0.75rem', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
                        Detected Books ({result.detected_books.length})
                      </h4>
                      <BookDetailPanel
                        books={result.detected_books}
                        selectedId={selectedBookId}
                        onSelect={handleSelectBook}
                      />
                    </div>
                  </motion.div>
                )}

                {/* ── Tab: Fix My Shelf ── */}
                {tab === 'fix' && (
                  <motion.div
                    key="fix-tab"
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="results-layout"
                  >
                    {/* Left: image for reference */}
                    <div>
                      <div className="scan-container">
                        <img src={imageUrl} alt="Shelf reference" className="scan-image" style={{ opacity: 0.7 }} />
                        <div className="scan-overlay" style={{ pointerEvents: 'auto' }}>
                          <BookOverlay
                            books={result.detected_books.filter(b => b.status === 'misplaced')}
                            selectedId={selectedBookId}
                            onSelect={handleSelectBook}
                          />
                        </div>
                      </div>
                      <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.5rem', textAlign: 'center' }}>
                        Only misplaced books are highlighted
                      </p>
                    </div>

                    {/* Right: steps */}
                    <div className="card">
                      <FixShelfMode books={result.detected_books} />
                    </div>
                  </motion.div>
                )}

                {/* ── Tab: Dashboard ── */}
                {tab === 'dashboard' && (
                  <motion.div
                    key="dashboard-tab"
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                  >
                    {health ? (
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        <div className="card">
                          <h3 style={{ marginBottom: '1.25rem' }}>Shelf Health</h3>
                          <ShelfHealthDashboard health={health} />
                        </div>
                        <div className="card">
                          <GenreChart genres={health.genre_distribution} />
                        </div>
                      </div>
                    ) : (
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                        {[1, 2].map(i => (
                          <div key={i} className="card skeleton" style={{ height: 300 }} />
                        ))}
                      </div>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )}

        </AnimatePresence>
      </main>

      {/* ── Footer ───────────────────────────────────────────────── */}
      <footer style={{
        padding: '1rem 2.5rem',
        borderTop: '1px solid rgba(255,255,255,0.05)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '0.78rem',
        color: 'var(--text-muted)',
      }}>
        <span>📚 Shelfie — AI Bookshelf Scanner</span>
        <span>Built with FastAPI · React · Framer Motion</span>
      </footer>
    </>
  );
}
