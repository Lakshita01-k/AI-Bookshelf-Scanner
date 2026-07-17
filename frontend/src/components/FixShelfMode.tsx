import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { CheckCircle, ArrowRight } from 'lucide-react';
import confetti from 'canvas-confetti';
import { DetectedBook } from '../lib/api';

interface Step {
  book: DetectedBook;
  instruction: string;
  from: number;
  to: number;
}

interface Props {
  books: DetectedBook[];
}

function buildSteps(books: DetectedBook[]): Step[] {
  return books
    .filter(b => b.status === 'misplaced')
    .map(b => {
      const diff = b.expected_position - b.detected_position;
      const dir = diff > 0 ? 'right →' : '← left';
      const spots = Math.abs(diff);
      return {
        book: b,
        from: b.detected_position,
        to: b.expected_position,
        instruction: `Move "${b.matched_title || 'this book'}" ${spots} spot${spots !== 1 ? 's' : ''} ${dir}`,
      };
    })
    .sort((a, b) => Math.abs(b.to - b.from) - Math.abs(a.to - a.from));
}

export default function FixShelfMode({ books }: Props) {
  const steps = buildSteps(books);
  const [doneSet, setDoneSet] = useState<Set<string>>(new Set());
  const [allDone, setAllDone] = useState(false);

  const toggleDone = (bookId: string) => {
    setDoneSet(prev => {
      const next = new Set(prev);
      if (next.has(bookId)) next.delete(bookId);
      else next.add(bookId);
      return next;
    });
  };

  useEffect(() => {
    if (steps.length > 0 && doneSet.size === steps.length) {
      setAllDone(true);
      // Confetti 🎉
      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.6 },
        colors: ['#d4a647', '#4caf86', '#f0a500', '#ffffff'],
      });
      setTimeout(() => confetti({
        particleCount: 60,
        angle: 60,
        spread: 55,
        origin: { x: 0, y: 0.7 },
      }), 200);
      setTimeout(() => confetti({
        particleCount: 60,
        angle: 120,
        spread: 55,
        origin: { x: 1, y: 0.7 },
      }), 400);
    } else {
      setAllDone(false);
    }
  }, [doneSet, steps.length]);

  if (steps.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        style={{
          textAlign: 'center',
          padding: '3rem',
          background: 'rgba(76,175,134,0.06)',
          border: '1px solid rgba(76,175,134,0.2)',
          borderRadius: 'var(--radius-lg)',
        }}
      >
        <div style={{ fontSize: '3rem', marginBottom: '0.75rem' }}>✨</div>
        <h3 style={{ color: 'var(--status-correct)', marginBottom: '0.5rem' }}>Your shelf is perfect!</h3>
        <p>All books are in their correct positions. Nothing to fix here.</p>
      </motion.div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div>
          <h3 style={{ marginBottom: '0.25rem' }}>Fix My Shelf</h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            {doneSet.size} of {steps.length} moves completed
          </p>
        </div>
        <button
          className="btn btn-ghost btn-sm"
          onClick={() => setDoneSet(new Set())}
          id="reset-fix-btn"
        >
          Reset
        </button>
      </div>

      {/* Progress bar */}
      <div style={{ height: 4, background: 'rgba(255,255,255,0.06)', borderRadius: 99, marginBottom: '1.5rem', overflow: 'hidden' }}>
        <motion.div
          style={{ height: '100%', background: 'linear-gradient(90deg, #d4a647, #4caf86)', borderRadius: 99 }}
          animate={{ width: steps.length ? `${(doneSet.size / steps.length) * 100}%` : '0%' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        />
      </div>

      {/* Steps */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }} id="fix-steps-list">
        <AnimatePresence>
          {steps.map((step, i) => {
            const isDone = doneSet.has(step.book.id);
            return (
              <motion.div
                key={step.book.id}
                id={`fix-step-${step.book.id}`}
                layout
                initial={{ opacity: 0, x: -16 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.07, duration: 0.4, layout: { duration: 0.4, ease: [0.34, 1.56, 0.64, 1] } }}
                className={`fix-step ${isDone ? 'done' : ''}`}
                onClick={() => toggleDone(step.book.id)}
                style={{ cursor: 'pointer' }}
              >
                <div className="fix-step-number">
                  {isDone ? <CheckCircle size={16} color="var(--status-correct)" /> : i + 1}
                </div>
                <div className="fix-step-content">
                  <div className="fix-step-instruction" style={{ textDecoration: isDone ? 'line-through' : 'none', opacity: isDone ? 0.6 : 1 }}>
                    {step.instruction}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginTop: '0.3rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    <span>Slot {step.from + 1}</span>
                    <ArrowRight size={11} />
                    <span>Slot {step.to + 1}</span>
                    {step.book.genre && (
                      <>
                        <span>·</span>
                        <span>{step.book.genre}</span>
                      </>
                    )}
                  </div>
                </div>
                <div
                  style={{
                    width: 8, height: 40, background: step.book.color,
                    borderRadius: 4, flexShrink: 0,
                  }}
                />
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* All done banner */}
      <AnimatePresence>
        {allDone && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 16 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            style={{
              marginTop: '1.5rem',
              padding: '1.5rem',
              background: 'rgba(76,175,134,0.1)',
              border: '1px solid rgba(76,175,134,0.3)',
              borderRadius: 'var(--radius-lg)',
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🎉</div>
            <h3 style={{ color: 'var(--status-correct)', marginBottom: '0.25rem' }}>Shelf sorted!</h3>
            <p style={{ fontSize: '0.9rem' }}>Your library is now perfectly organized.</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
