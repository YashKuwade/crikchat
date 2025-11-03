// src/api/players.ts
export type PlayerResponse = {
  id?: number | null
  name: string
  career_runs: number
}

export type ApiError = { detail?: string } | { error?: string }

/**
 * POST /api/player_runs
 * Sends JSON body { name }
 */
export async function fetchPlayerByPost(name: string): Promise<PlayerResponse> {
  const res = await fetch('/api/player_runs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  })
  if (!res.ok) {
    const body = (await safeParseJson(res)) as ApiError
    throw new Error(body?.detail || body?.error || `HTTP ${res.status}`)
  }
  return (await res.json()) as PlayerResponse
}

/**
 * GET /api/player_runs?name=...
 * Optional fallback if you enable the GET endpoint.
 */
export async function fetchPlayerByGet(name: string): Promise<PlayerResponse> {
  const url = `/api/player_runs?name=${encodeURIComponent(name)}`
  const res = await fetch(url)
  if (!res.ok) {
    const body = (await safeParseJson(res)) as ApiError
    throw new Error(body?.detail || body?.error || `HTTP ${res.status}`)
  }
  return (await res.json()) as PlayerResponse
}

/** helper to avoid throwing on non-json responses */
async function safeParseJson(res: Response) {
  try {
    return await res.json()
  } catch {
    return {}
  }
}