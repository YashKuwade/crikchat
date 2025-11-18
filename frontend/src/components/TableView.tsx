// src/components/TableView.tsx
import { useState } from 'react'
import type { QueryResponse } from '../api/players'

interface TableViewProps {
  data: QueryResponse
}

export default function TableView({ data }: TableViewProps) {
  const [sortColumn, setSortColumn] = useState<string | null>(null)
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc')

  // Handle column header click for sorting
  const handleSort = (column: string) => {
    if (sortColumn === column) {
      // Toggle direction if same column
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      // New column, default to ascending
      setSortColumn(column)
      setSortDirection('asc')
    }
  }

  // Sort the rows
  const sortedRows = [...data.rows].sort((a, b) => {
    if (!sortColumn) return 0

    const aVal = a[sortColumn]
    const bVal = b[sortColumn]

    // Handle null/undefined
    if (aVal == null) return 1
    if (bVal == null) return -1

    // Numeric comparison
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return sortDirection === 'asc' ? aVal - bVal : bVal - aVal
    }

    // String comparison
    const aStr = String(aVal).toLowerCase()
    const bStr = String(bVal).toLowerCase()
    
    if (aStr < bStr) return sortDirection === 'asc' ? -1 : 1
    if (aStr > bStr) return sortDirection === 'asc' ? 1 : -1
    return 0
  })

  return (
    <div style={{ marginTop: 16, overflowX: 'auto' }}>
      <table style={{ 
        width: '100%', 
        borderCollapse: 'collapse',
        background: 'white',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
      }}>
        <thead>
          <tr style={{ background: '#f0f0f0' }}>
            {data.columns.map((col) => (
              <th 
                key={col}
                onClick={() => handleSort(col)}
                style={{ 
                padding: '12px', 
                textAlign: 'left', 
                border: '1px solid #ddd',
                fontWeight: '600',
                textTransform: 'capitalize'
              }}>
                {col.replace(/_/g, ' ')}
                {sortColumn === col && (
                  <span style={{ marginLeft: 6, fontSize: 10 }}>
                    {sortDirection === 'asc' ? '▲' : '▼'}
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedRows.map((row, idx) => (
            <tr 
              key={idx} 
              style={{ 
                background: idx % 2 === 0 ? 'white' : '#f9f9f9',
                transition: 'background 0.2s'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#e8f4f8'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = idx % 2 === 0 ? 'white' : '#f9f9f9'
              }}
            >
              {data.columns.map((col) => (
                <td key={col} style={{ 
                  padding: '10px', 
                  border: '1px solid #ddd'
                }}>
                  {typeof row[col] === 'number' 
                    ? row[col].toLocaleString()  // Format numbers with commas
                    : (row[col] ?? '-')
                  }
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}