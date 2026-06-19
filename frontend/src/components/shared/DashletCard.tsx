import { ReactNode } from 'react'

interface DashletCardProps {
  label: string
  value: string | number
  icon?: ReactNode
  trend?: string
}

export default function DashletCard({ label, value, trend }: DashletCardProps) {
  return (
    <div
      style={{
        background: '#FDF0E2',
        borderRadius: 8,
        padding: '10px 14px',
      }}
    >
      <p style={{ fontSize: 11, color: '#44546A', margin: '0 0 4px', opacity: 0.7 }}>{label}</p>
      <p style={{ fontSize: 20, fontWeight: 500, color: '#44546A', margin: 0 }}>{value}</p>
      {trend && <p style={{ fontSize: 11, color: '#639922', margin: '4px 0 0' }}>{trend}</p>}
    </div>
  )
}
