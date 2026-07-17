import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Upload, BookOpen, Sparkles } from 'lucide-react';

interface Props {
  onFile: (file: File) => void;
}

export default function ShelfUploader({ onFile }: Props) {
  const onDrop = useCallback((accepted: File[]) => {
    if (accepted[0]) onFile(accepted[0]);
  }, [onFile]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png', '.webp', '.heic'] },
    maxFiles: 1,
  });

  const handleDemo = () => {
    fetch('/demo-bookshelf.png')
      .then(r => r.blob())
      .then(blob => {
        const file = new File([blob], 'demo-bookshelf.png', { type: 'image/png' });
        onFile(file);
      });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
    >
      {/* Hero text */}
      <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.35rem 1rem',
            background: 'var(--accent-dim)',
            border: '1px solid rgba(212,166,71,0.25)',
            borderRadius: '99px',
            fontSize: '0.8rem',
            color: 'var(--accent)',
            fontWeight: 500,
            marginBottom: '1.5rem',
          }}
        >
          <Sparkles size={13} />
          AI-powered bookshelf organizer
        </motion.div>

        <h1 style={{ marginBottom: '0.75rem' }}>
          Your shelf, <em>sorted.</em>
        </h1>
        <p style={{ maxWidth: 480, margin: '0 auto', fontSize: '1.05rem', color: 'var(--text-secondary)' }}>
          Snap a photo of your bookshelf and let Shelfie detect, identify, and
          tell you exactly where each book belongs.
        </p>
      </div>

      {/* Drop zone */}
      <div
        {...getRootProps()}
        className={`uploader-zone ${isDragActive ? 'drag-active' : ''}`}
        id="shelf-dropzone"
      >
        <input {...getInputProps()} id="shelf-file-input" />

        <motion.div
          animate={isDragActive ? { scale: 1.1 } : { scale: 1 }}
          transition={{ type: 'spring', stiffness: 400, damping: 15 }}
        >
          <span className="uploader-icon">📚</span>
        </motion.div>

        {isDragActive ? (
          <h2 className="uploader-title">Drop it right here!</h2>
        ) : (
          <h2 className="uploader-title">Drop your shelf photo here</h2>
        )}

        <p className="uploader-sub">
          JPG, PNG, WEBP supported · Works best with a straight-on, well-lit photo
        </p>

        <div className="uploader-actions">
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            className="btn btn-primary btn-lg"
            onClick={e => e.stopPropagation()}
            style={{ pointerEvents: 'none' }}
          >
            <Upload size={18} />
            Choose Photo
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            className="btn btn-secondary btn-lg"
            id="demo-shelf-btn"
            onClick={e => { e.stopPropagation(); handleDemo(); }}
          >
            <BookOpen size={18} />
            Try Demo Shelf
          </motion.button>
        </div>
      </div>

      {/* Feature pills */}
      <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', marginTop: '2rem', flexWrap: 'wrap' }}>
        {[
          { icon: '🔍', label: 'Spine detection' },
          { icon: '📖', label: 'Title recognition' },
          { icon: '🗂️', label: 'Smart sorting' },
          { icon: '🎯', label: 'Step-by-step fix plan' },
        ].map(f => (
          <div
            key={f.label}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              padding: '0.4rem 0.9rem',
              background: 'var(--bg-elevated)',
              border: '1px solid rgba(255,255,255,0.05)',
              borderRadius: '99px',
              fontSize: '0.8rem',
              color: 'var(--text-muted)',
            }}
          >
            <span>{f.icon}</span> {f.label}
          </div>
        ))}
      </div>
    </motion.div>
  );
}
