import React, { useState } from 'react'
import { executeNaturalLanguageQuery } from '../api/players'
import type { QueryResponse } from '../api/players'
export default function PlayerLookup() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<QueryResponse | null>(null)

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
    } catch (err: any) {
      setError(err?.message || String(err))
    } finally {
      setLoading(false)
    }
  }

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
          <p style={{ marginBottom: 8, fontWeight: 'bold' }}>
            Found {result.row_count} result{result.row_count !== 1 ? 's' : ''}
          </p>
          
          <div style={{ overflowX: 'auto' }}>
            <table style={{ 
              width: '100%', 
              borderCollapse: 'collapse',
              background: 'white',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <thead>
                <tr style={{ background: '#f0f0f0' }}>
                  {result.columns.map((col) => (
                    <th key={col} style={{ 
                      padding: '12px', 
                      textAlign: 'left', 
                      border: '1px solid #ddd',
                      fontWeight: '600',
                      textTransform: 'capitalize'
                    }}>
                      {col.replace(/_/g, ' ')}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.rows.map((row, idx) => (
                  <tr key={idx} style={{ 
                    background: idx % 2 === 0 ? 'white' : '#f9f9f9' 
                  }}>
                    {result.columns.map((col) => (
                      <td key={col} style={{ 
                        padding: '10px', 
                        border: '1px solid #ddd'
                      }}>
                        {row[col] ?? '-'}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

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
        <div style={{ padding: 20, background: '#f0f0f0', marginTop: 16 }}>
          No results found
        </div>
      )}
    </div>
  )
}