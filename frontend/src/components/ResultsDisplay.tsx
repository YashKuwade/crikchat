// src/components/ResultsDisplay.tsx
import type { QueryResponse } from '../api/players'
import TableView from './TableView'
import BarChartView from './BarChartView'

interface ResultsDisplayProps {
  data: QueryResponse
  viewMode: 'table' | 'chart'
}

// Helper: Check if data is suitable for bar chart
function canShowChart(data: QueryResponse): boolean {
  // Need at least 2 columns
  if (data.columns.length < 2) return false
  
  // Need at least 1 row
  if (data.rows.length === 0) return false
  
  // Second column should be numeric
  const firstRow = data.rows[0]
  const secondColValue = firstRow[data.columns[1]]
  const isNumeric = typeof secondColValue === 'number' || !isNaN(Number(secondColValue))
  
  return isNumeric
}

export default function ResultsDisplay({ data, viewMode }: ResultsDisplayProps) {
  const chartAvailable = canShowChart(data)

  // If chart is requested but not available, fallback to table
  if (viewMode === 'chart' && !chartAvailable) {
    return (
      <div>
        <div style={{ 
          padding: 10, 
          background: '#fff3cd', 
          border: '1px solid #ffc107',
          marginBottom: 16,
          borderRadius: 4
        }}>
          ⚠️ Chart view not available for this data. Showing table instead.
        </div>
        <TableView data={data} />
      </div>
    )
  }

  return (
    <div>
      {viewMode === 'chart' ? (
        <BarChartView data={data} />
      ) : (
        <TableView data={data} />
      )}
    </div>
  )
}