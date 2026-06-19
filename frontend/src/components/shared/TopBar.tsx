interface TopBarProps {
  title?: string
  actions?: React.ReactNode
}

export default function TopBar({ title, actions }: TopBarProps) {
  return (
    <header style={{
      height: 56,
      background: '#FFFFFF',
      borderBottom: '0.5px solid #D5DCE8',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <span style={{ fontSize: 16, fontWeight: 500, color: '#44546A' }}>
          NIRUKTA
        </span>
        {title && (
          <>
            <span style={{ color: '#D5DCE8' }}>|</span>
            <span style={{ fontSize: 13, color: '#44546A', opacity: 0.7 }}>{title}</span>
          </>
        )}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        {actions}
        <div style={{
          width: 32, height: 32, borderRadius: '50%',
          background: '#E8F0DE', display: 'flex',
          alignItems: 'center', justifyContent: 'center',
          fontSize: 12, fontWeight: 500, color: '#44546A', cursor: 'pointer',
        }}>AR</div>
      </div>
    </header>
  )
}
