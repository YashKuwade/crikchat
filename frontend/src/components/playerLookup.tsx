import React, { useState } from 'react'

type Resp = { id?: number | null; name: string; runs: number }

export default function PlayerLookup() {
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<Resp | null>(null)

  async function lookup() {
    setError(null)
    setResult(null)
    const trimmed = name.trim()
    if (!trimmed) {
      setError('Enter a player name')
      return
    }
    setLoading(true)
    try {
      const res = await fetch('/api/player_runs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: trimmed }),
      })
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.detail || `HTTP ${res.status}`)
      }
      const data = (await res.json()) as Resp
      setResult(data)
    } catch (err: any) {
      setError(err?.message || String(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 700 }}>
      <h2>Batter Career Runs in ODIs</h2>
      <div style={{ marginBottom: 8 }}>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter Batter Name"
          style={{ width: '70%', padding: 8, marginRight: 8 }}
        />
        <button onClick={lookup} disabled={loading}>
          {loading ? 'Looking...' : 'Lookup'}
        </button>
      </div>

      {error && <div style={{ color: 'crimson' }}>{error}</div>}

      {result && (
        <div style={{ marginTop: 12, padding: 12, background: '#f2f2f2' }}>
          <div>
            <strong>{result.name}</strong> {result.id ? <span> (id: {result.id})</span> : null}
          </div>
          <div style={{ marginTop: 6 }}>Runs: <strong>{result.runs}</strong></div>
        </div>
      )}
    </div>
  )
}