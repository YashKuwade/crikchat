import React, { useState } from 'react'
import { executeNaturalLanguageQuery } from '../api/players'
import type { QueryResponse } from '../api/players'
import ResultsDisplay from './ResultsDisplay'

export default function PlayerLookup() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<QueryResponse | null>(null)
  const [viewMode, setViewMode] = useState<'table' | 'chart'>('table')

  async function lookup() {
    setError(null)
    setResult(null)
    const trimmed = question.trim()
    if (!trimmed) {
      setError('Enter a Question')
      return
    }
    setLoading(true)
    try {
      const data = await executeNaturalLanguageQuery(trimmed)
      setResult(data)
      // Auto-switch to chart if data looks good for visualization
      if (data.columns.length === 2 && data.rows.length > 0 && data.rows.length <= 10) {
        setViewMode('chart')
      } else {
        setViewMode('table')
      }
    } catch (err: any) {
      setError(err?.message || String(err))
    } finally {
      setLoading(false)
    }
  }

  // Helper to check if chart is available
  const canShowChart = result && 
    result.columns.length >= 2 && 
    result.rows.length > 0 &&
    !isNaN(Number(result.rows[0][result.columns[1]]))

  return (
    <div style={{ maxWidth: 900, margin: '20px auto', padding: '0 20px' }}>
      <h2>Cricket Stats Query</h2>
      <div style={{ marginBottom: 16 }}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && lookup()}
          placeholder="Ask anything: 'Show players with more than 5000 runs'"
          style={{ width: '80%', padding: 10, marginRight: 8, fontSize: 14 }}
        />
        <button onClick={lookup} disabled={loading} style={{ padding: 10 }}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && <div style={{ color: 'crimson', padding: 10, background: '#ffe0e0' }}>{error}</div>}

      {result && result.rows.length > 0 && (
        <div style={{ marginTop: 16 }}>
          {/* Results Header with View Toggle */}
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: 12 
          }}>
            <p style={{ margin: 0, fontWeight: 'bold' }}>
              Found {result.row_count} result{result.row_count !== 1 ? 's' : ''}
            </p>

            {canShowChart && (
              <div style={{ 
                display: 'flex', 
                gap: 8,
                border: '1px solid #ddd',
                borderRadius: 4,
                padding: 2,
                background: '#f9f9f9'
              }}>
                <button
                  onClick={() => setViewMode('table')}
                  style={{
                    padding: '6px 12px',
                    border: 'none',
                    background: viewMode === 'table' ? '#007bff' : 'transparent',
                    color: viewMode === 'table' ? 'white' : '#333',
                    cursor: 'pointer',
                    borderRadius: 3,
                    fontWeight: viewMode === 'table' ? 'bold' : 'normal'
                  }}
                >
                  📊 Table
                </button>
                <button
                  onClick={() => setViewMode('chart')}
                  style={{
                    padding: '6px 12px',
                    border: 'none',
                    background: viewMode === 'chart' ? '#007bff' : 'transparent',
                    color: viewMode === 'chart' ? 'white' : '#333',
                    cursor: 'pointer',
                    borderRadius: 3,
                    fontWeight: viewMode === 'chart' ? 'bold' : 'normal'
                  }}
                >
                  📈 Chart
                </button>
              </div>
            )}
          </div>

          {/* Results Display */}
          <ResultsDisplay data={result} viewMode={viewMode} />

          {/* SQL Query Display */}
          {result.sql && (
            <details style={{ marginTop: 12, fontSize: 12 }}>
              <summary style={{ cursor: 'pointer', color: '#666' }}>
                Show SQL Query
              </summary>
              <pre style={{ 
                background: '#f5f5f5', 
                padding: 10, 
                marginTop: 8,
                borderRadius: 4,
                overflow: 'auto'
              }}>
                {result.sql}
              </pre>
            </details>
          )}
        </div>
      )}

      {result && result.rows.length === 0 && (
        <div style={{ padding: 20, background: '#f0f0f0', marginTop: 16, borderRadius: 4 }}>
          No results found
        </div>
      )}
    </div>
  )
}