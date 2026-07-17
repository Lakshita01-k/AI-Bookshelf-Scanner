import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { GenreCount } from '../lib/api';
import { motion } from 'framer-motion';

interface Props {
  genres: GenreCount[];
}

const PALETTE = [
  '#d4a647', '#4caf86', '#f0a500', '#3d7abf', '#e05c5c',
  '#8b6e4e', '#5c8a3a', '#7a4abf', '#bf5c8a', '#4abfbf',
];

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: 'var(--radius-sm)',
        padding: '0.5rem 0.9rem',
        fontSize: '0.82rem',
        color: 'var(--text-primary)',
      }}>
        <strong>{payload[0].name}</strong>: {payload[0].value} book{payload[0].value !== 1 ? 's' : ''}
      </div>
    );
  }
  return null;
};

export default function GenreChart({ genres }: Props) {
  if (!genres.length) {
    return <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>No genre data available.</p>;
  }

  const data = genres.map(g => ({ name: g.genre, value: g.count }));

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
    >
      <h4 style={{ marginBottom: '1rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.75rem' }}>
        Genre Distribution
      </h4>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={65}
            outerRadius={100}
            paddingAngle={3}
            dataKey="value"
            animationBegin={300}
            animationDuration={900}
          >
            {data.map((_, i) => (
              <Cell key={i} fill={PALETTE[i % PALETTE.length]} stroke="transparent" />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            formatter={(value) => (
              <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{value}</span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
