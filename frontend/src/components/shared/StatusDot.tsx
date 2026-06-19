interface StatusDotProps {
  status: 'healthy' | 'warning' | 'error'
}

const colors = {
  healthy: '#639922',
  warning: '#BA7517',
  error: '#C0392B',
}

export default function StatusDot({ status }: StatusDotProps) {
  return (
    <span
      style={{
        display: 'inline-block',
        width: 7,
        height: 7,
        borderRadius: '50%',
        background: colors[status],
        flexShrink: 0,
      }}
    />
  )
}
