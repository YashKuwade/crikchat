// src/utils/chartColors.ts

export const colorSchemes = {
  blue: ['#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'],
  green: ['#15803d', '#22c55e', '#4ade80', '#86efac', '#d1fae5'],
  purple: ['#7c3aed', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe'],
  orange: ['#ea580c', '#fb923c', '#fdba74', '#fed7aa', '#ffedd5'],
  red: ['#dc2626', '#f87171', '#fca5a5', '#fecaca', '#fee2e2'],
}

export function getColorForValue(value: number, max: number, scheme: keyof typeof colorSchemes = 'blue'): string {
  const colors = colorSchemes[scheme]
  const percentage = value / max
  
  if (percentage > 0.8) return colors[0]  // Darkest
  if (percentage > 0.6) return colors[1]
  if (percentage > 0.4) return colors[2]
  if (percentage > 0.2) return colors[3]
  return colors[4]  // Lightest
}