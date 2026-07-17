import React from 'react';
import { motion } from 'framer-motion';
import { DetectedBook } from '../lib/api';

interface Props {
  books: DetectedBook[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

const STATUS_STYLES: Record<string, string> = {
  correct: 'bbox-correct',
  misplaced: 'bbox-misplaced',
  missing: 'bbox-missing',
  unknown: 'bbox-unknown',
};

const STATUS_LABELS: Record<string, string> = {
  correct: '✅',
  misplaced: '⚠️',
  missing: '❌',
  unknown: '❓',
};

export default function BookOverlay({ books, selectedId, onSelect }: Props) {
  return (
    <div className="bbox-container" id="book-overlay">
      {books.map((book, i) => {
        const isSelected = selectedId === book.id;
        const style: React.CSSProperties = {
          left: `${book.bbox.x * 100}%`,
          top: `${book.bbox.y * 100}%`,
          width: `${book.bbox.w * 100}%`,
          height: `${book.bbox.h * 100}%`,
        };

        return (
          <motion.div
            key={book.id}
            id={`bbox-${book.id}`}
            className={`bbox ${STATUS_STYLES[book.status]} ${isSelected ? 'selected' : ''}`}
            style={style}
            initial={{ opacity: 0, scale: 0.85 }}
            animate={{ opacity: 1, scale: isSelected ? 1.04 : 1 }}
            transition={{ delay: i * 0.06, duration: 0.4, ease: [0.34, 1.56, 0.64, 1] }}
            onClick={() => onSelect(book.id)}
            title={book.matched_title || book.ocr_text || 'Unknown'}
          >
            {/* Emoji label at top */}
            <span
              style={{
                position: 'absolute',
                top: -18,
                left: '50%',
                transform: 'translateX(-50%)',
                fontSize: '0.75rem',
                lineHeight: 1,
                pointerEvents: 'none',
              }}
            >
              {STATUS_LABELS[book.status]}
            </span>
          </motion.div>
        );
      })}
    </div>
  );
}
