import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { ShelfHealth } from '../lib/api';

interface Props {
  health: ShelfHealth;
}

const CIRCUMFERENCE = 2 * Math.PI * 54; // r=54

export default function ShelfHealthDashboard({ health }: Props) {
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setAnimated(true), 100);
    return () => clearTimeout(t);
  }, []);

  const score = health.shelf_score;
  const offset = CIRCUMFERENCE - (animated ? (score / 100) * CIRCUMFERENCE : CIRCUMFERENCE);

  const scoreColor =
    score >= 80 ? 'var(--status-correct)' :
    score >= 50 ? 'var(--status-misplaced)' :
    'var(--status-missing)';

  const stats = [
    { label: 'Correctly placed', value: health.correct_count, color: 'var(--status-correct)', icon: '✅' },
    { label: 'Misplaced', value: health.misplaced_count, color: 'var(--status-misplaced)', icon: '⚠️' },
    { label: 'Missing', value: health.missing_count, color: 'var(--status-missing)', icon: '❌' },
    { label: 'Total books', value: health.total_books, color: 'var(--accent)', icon: '📚' },
  ];

  return (
    <div>
      {/* Score ring + stat cards */}
      <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap' }}>
        {/* Radial score ring */}
        <div className="score-ring-wrap" style={{ flexShrink: 0 }}>
          <svg width="140" height="140" viewBox="0 0 120 120" className="score-ring-svg">
            <defs>
              <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#d4a647" />
                <stop offset="100%" stopColor="#4caf86" />
              </linearGradient>
            </defs>
            <circle className="score-ring-track" cx="60" cy="60" r="54" />
            <circle
              className="score-ring-progress"
              cx="60" cy="60" r="54"
              strokeDasharray={CIRCUMFERENCE}
              strokeDashoffset={offset}
              style={{ transition: 'stroke-dashoffset 1.5s cubic-bezier(0.4,0,0.2,1)' }}
            />
          </svg>
          {/* Center text overlaid */}
          <div style={{
            position: 'absolute',
            display: 'flex', flexDirection: 'column', alignItems: 'center',
            pointerEvents: 'none',
          }}>
          </div>
          {/* Absolute positioned center of SVG */}
          <div style={{ position: 'relative', marginTop: '-128px', textAlign: 'center', pointerEvents: 'none' }}>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              style={{ lineHeight: 1 }}
            >
              <div style={{ fontSize: '2rem', fontWeight: 700, color: scoreColor, fontFamily: 'Playfair Display, serif' }}>
                {animated ? Math.round(score) : 0}%
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                Shelf Score
              </div>
            </motion.div>
          </div>
          <div style={{ marginTop: '70px' }} /> {/* spacer */}
        </div>

        {/* Stat cards grid */}
        <div style={{ flex: 1, display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem' }}>
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              className="stat-card"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + i * 0.1 }}
            >
              <div style={{ fontSize: '1.4rem', marginBottom: '0.25rem' }}>{s.icon}</div>
              <div className="stat-value" style={{ color: s.color }}>{s.value}</div>
              <div className="stat-label">{s.label}</div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Shelf sort rule */}
      <div style={{
        padding: '0.75rem 1rem',
        background: 'var(--bg-elevated)',
        borderRadius: 'var(--radius-md)',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        marginBottom: '1.5rem',
        fontSize: '0.85rem',
        color: 'var(--text-secondary)',
      }}>
        <span>📋</span>
        <span>Sort rule: <strong style={{ color: 'var(--text-primary)' }}>{health.sort_rule}</strong></span>
        <span style={{ marginLeft: 'auto', color: 'var(--text-muted)' }}>{health.shelf_name}</span>
      </div>

      {/* Message */}
      <div className="ai-message">
        <span>🤖</span>
        <span>
          {score >= 90
            ? `Looking great! Your shelf is ${Math.round(score)}% organized.`
            : score >= 70
            ? `Found ${health.misplaced_count} misplaced book${health.misplaced_count !== 1 ? 's' : ''}. Let's sort that out.`
            : `Your shelf needs some love — ${health.misplaced_count} misplaced, ${health.missing_count} missing.`}
        </span>
      </div>
    </div>
  );
}
