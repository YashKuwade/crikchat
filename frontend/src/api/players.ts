// src/api/players.ts
export type QueryResponse = {
  columns: string[]
  rows: Record<string, any>[]
  row_count: []   // unified naming
  sql?: string
}

// legacy player response
export type PlayerResponse = {
  id?: number | null
  name: string
  runs?: number
  career_runs?: number
  wickets?: number
  country?: string
  balls?: number
  sixes?: number
  fours?: number
  matches?: number
  fifties?: number
  centuries?: number
  [key: string]: any  // Allow any additional fields
}

export type ApiError = { detail?: string } | { error?: string }

export async function executeNaturalLanguageQuery(userQuery: string): Promise<QueryResponse> {
  const res = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: userQuery }),
  })
  const body = await safeParseJson(res)
  if (!res.ok) {
    const err = (body as ApiError)
    throw new Error(err?.detail || err?.error || `HTTP ${res.status}`)
  }
  return (body as QueryResponse)
}

// legacy function
export async function fetchPlayerByPost(name: string): Promise<PlayerResponse> {
  const res = await fetch('/api/player_runs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  })
  const body = await safeParseJson(res)
  if (!res.ok) {
    const err = (body as ApiError)
    throw new Error(err?.detail || err?.error || `HTTP ${res.status}`)
  }
  return (body as PlayerResponse)
}

/** helper to avoid throwing on non-json responses */
async function safeParseJson(res: Response) {
  try {
    return await res.json()
  } catch {
    return {}
  }
}