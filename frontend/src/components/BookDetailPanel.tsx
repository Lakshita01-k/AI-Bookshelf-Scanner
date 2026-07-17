import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { DetectedBook } from '../lib/api';
import { BookOpen, AlertTriangle, X, HelpCircle } from 'lucide-react';

interface Props {
  books: DetectedBook[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

const STATUS_ICONS = {
  correct: <span style={{ color: 'var(--status-correct)', fontSize: '1rem' }}>✅</span>,
  misplaced: <span style={{ color: 'var(--status-misplaced)', fontSize: '1rem' }}>⚠️</span>,
  missing: <span style={{ color: 'var(--status-missing)', fontSize: '1rem' }}>❌</span>,
  unknown: <span style={{ color: 'var(--status-unknown)', fontSize: '1rem' }}>❓</span>,
};

const STATUS_BADGE_CLASS: Record<string, string> = {
  correct: 'badge badge-correct',
  misplaced: 'badge badge-misplaced',
  missing: 'badge badge-missing',
  unknown: 'badge badge-unknown',
};

const STATUS_LABELS: Record<string, string> = {
  correct: 'Correct',
  misplaced: 'Misplaced',
  missing: 'Missing',
  unknown: 'Unknown',
};

export default function BookDetailPanel({ books, selectedId, onSelect }: Props) {
  const selected = books.find(b => b.id === selectedId);

  // Group counts
  const counts = books.reduce(
    (acc, b) => { acc[b.status] = (acc[b.status] || 0) + 1; return acc; },
    {} as Record<string, number>
  );

  return (
    <div>
      {/* Summary row */}
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
        {(['correct', 'misplaced', 'missing', 'unknown'] as const).map(s =>
          counts[s] ? (
            <span key={s} className={STATUS_BADGE_CLASS[s]}>
              {STATUS_ICONS[s]} {counts[s]} {STATUS_LABELS[s]}
            </span>
          ) : null
        )}
      </div>

      {/* Selected book detail */}
      <AnimatePresence mode="wait">
        {selected && (
          <motion.div
            key={selected.id}
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 8 }}
            transition={{ duration: 0.25 }}
            style={{
              background: 'var(--bg-elevated)',
              border: '1px solid rgba(212,166,71,0.2)',
              borderRadius: 'var(--radius-md)',
              padding: '1rem',
              marginBottom: '1rem',
            }}
          >
            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              {/* Spine color swatch */}
              <div style={{
                width: 8, height: 64,
                background: selected.color,
                borderRadius: 4, flexShrink: 0, marginTop: 2,
              }} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: '1rem', fontFamily: 'Playfair Display, serif', fontWeight: 600, marginBottom: 2 }}>
                  {selected.matched_title || selected.ocr_text || '—'}
                </div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                  {selected.matched_author || 'Unknown author'}
                </div>
                <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                  <span className={STATUS_BADGE_CLASS[selected.status]}>
                    {STATUS_LABELS[selected.status]}
                  </span>
                  {selected.genre && selected.genre !== 'Unknown' && (
                    <span className="badge" style={{ background: 'var(--bg-card)', color: 'var(--text-muted)', border: '1px solid rgba(255,255,255,0.08)' }}>
                      {selected.genre}
                    </span>
                  )}
                </div>

                {selected.status === 'misplaced' && (
                  <div style={{
                    marginTop: '0.75rem',
                    padding: '0.5rem 0.75rem',
                    background: 'rgba(240,165,0,0.08)',
                    border: '1px solid rgba(240,165,0,0.2)',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.78rem',
                    color: 'var(--status-misplaced)',
                  }}>
                    📍 Currently at position {selected.detected_position + 1},
                    should be at position {selected.expected_position + 1}
                  </div>
                )}

                {/* Confidence bar */}
                {selected.confidence > 0 && (
                  <div style={{ marginTop: '0.6rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: 3 }}>
                      <span>Confidence</span>
                      <span>{Math.round(selected.confidence * 100)}%</span>
                    </div>
                    <div className="confidence-bar">
                      <motion.div
                        className="confidence-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${selected.confidence * 100}%` }}
                        transition={{ duration: 0.6 }}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Book list */}
      <div className="book-panel" id="book-list-panel">
        {books.map((book, i) => (
          <motion.div
            key={book.id}
            id={`book-item-${book.id}`}
            className={`book-list-item ${selectedId === book.id ? 'active' : ''}`}
            onClick={() => onSelect(book.id)}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.04, duration: 0.3 }}
          >
            <div
              className="book-spine-color"
              style={{ background: book.color }}
            />
            <div className="book-list-meta">
              <div className="book-list-title">
                {book.matched_title || book.ocr_text || 'Unknown book'}
              </div>
              <div className="book-list-author">
                {book.matched_author || '—'}
              </div>
            </div>
            <span className={STATUS_BADGE_CLASS[book.status]} style={{ flexShrink: 0 }}>
              {STATUS_LABELS[book.status]}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
