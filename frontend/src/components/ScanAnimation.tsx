import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const STATUS_MESSAGES = [
  'Detecting spines...',
  'Segmenting book regions...',
  'Reading titles...',
  'Matching to database...',
  'Cross-checking inventory...',
  'Computing shelf score...',
  'Almost done...',
];

interface Props {
  imageUrl: string;
  progress: number;
}

export default function ScanAnimation({ imageUrl, progress }: Props) {
  const [msgIdx, setMsgIdx] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setMsgIdx(i => (i + 1) % STATUS_MESSAGES.length);
    }, 900);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="scan-container" id="scan-animation-container">
      <img src={imageUrl} alt="Your bookshelf" className="scan-image" />

      {/* Scan line sweep */}
      <div className="scan-overlay">
        <motion.div
          className="scan-line"
          initial={{ top: '0%' }}
          animate={{ top: ['0%', '100%', '0%'] }}
          transition={{ duration: 2.4, repeat: Infinity, ease: 'linear' }}
        />

        {/* Radial shimmer on image */}
        <motion.div
          style={{
            position: 'absolute',
            inset: 0,
            background: 'radial-gradient(ellipse 50% 30% at 50% 50%, rgba(212,166,71,0.06) 0%, transparent 70%)',
          }}
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.6, repeat: Infinity, ease: 'easeInOut' }}
        />

        {/* Status bar at bottom */}
        <div className="scan-status-bar">
          <div className="scan-spinner" />
          <AnimatePresence mode="wait">
            <motion.span
              key={msgIdx}
              className="scan-status-text"
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.3 }}
            >
              {STATUS_MESSAGES[msgIdx]}
            </motion.span>
          </AnimatePresence>
          <div style={{ marginLeft: 'auto', fontSize: '0.8rem', color: 'var(--accent)', fontWeight: 600 }}>
            {progress}%
          </div>
        </div>
      </div>

      {/* Progress bar below image */}
      <div style={{
        height: 3, background: 'rgba(255,255,255,0.06)', borderRadius: 99,
        marginTop: '0.75rem', overflow: 'hidden',
      }}>
        <motion.div
          style={{ height: '100%', background: 'linear-gradient(90deg, #d4a647, #4caf86)', borderRadius: 99 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
}
