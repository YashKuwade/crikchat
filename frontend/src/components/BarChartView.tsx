// src/components/BarChartView.tsx
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import type { QueryResponse } from '../api/players'
import { getColorForValue } from '../utils/chartColors'

interface BarChartViewProps {
  data: QueryResponse
}

export default function BarChartView({ data }: BarChartViewProps) {
  // Transform data for Recharts
  // Assumes: first column is category (X-axis), second column is value (Y-axis)
  const chartData = data.rows.map(row => ({
    name: String(row[data.columns[0]] || ''),
    value: Number(row[data.columns[1]] || 0)
  }))

  const maxValue = Math.max(...chartData.map(d => d.value))
  
  // Get column names for labels
  const xAxisLabel = data.columns[0]?.replace(/_/g, ' ') || 'Category'
  const yAxisLabel = data.columns[1]?.replace(/_/g, ' ') || 'Value'

  // Generate a nice title
  const chartTitle = `${yAxisLabel} by ${xAxisLabel}`

  // Color scheme options
  const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1']
  const barColor = colors[0]

  return (
    <div style={{ width: '100%', marginTop: 20 }}>
      {/* Chart Title */}
      <h3 style={{ 
        margin: '0 0 20px 0', 
        textAlign: 'center',
        color: '#333',
        textTransform: 'capitalize'
      }}>
        {chartTitle}
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="name" 
            angle={-45} 
            textAnchor="end" 
            height={100}
            label={{ value: xAxisLabel, position: 'insideBottom', offset: -10 }}
          />
          <YAxis 
            label={{ value: yAxisLabel, angle: -90, position: 'insideLeft' }}
          />
          <Tooltip />
          <Legend />
          <Bar 
            dataKey="value" 
            fill={barColor} 
            name={yAxisLabel}
            radius={[8,8,0,0]}
          >
            {chartData.map((entry, index) => (
                <Cell 
                key={`cell-${index}`} 
                fill={getColorForValue(entry.value, maxValue, 'blue')} 
                />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}