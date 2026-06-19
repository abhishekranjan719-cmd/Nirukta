import { NavLink } from 'react-router-dom'

interface NavItem {
  label: string
  path: string
  icon?: string
}

interface SideNavProps {
  items: NavItem[]
  title: string
}

export default function SideNav({ items, title }: SideNavProps) {
  return (
    <aside style={{
      width: 220,
      minHeight: '100vh',
      background: '#FFFFFF',
      borderRight: '0.5px solid #D5DCE8',
      padding: '20px 0',
      flexShrink: 0,
    }}>
      <div style={{ padding: '0 20px 20px', borderBottom: '0.5px solid #D5DCE8' }}>
        <p style={{ fontSize: 11, fontWeight: 500, color: '#44546A', opacity: 0.5, margin: 0, textTransform: 'uppercase', letterSpacing: '0.08em' }}>{title}</p>
      </div>
      <nav style={{ padding: '12px 8px' }}>
        {items.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              padding: '8px 12px',
              borderRadius: 6,
              fontSize: 13,
              fontWeight: isActive ? 500 : 400,
              color: '#44546A',
              background: isActive ? '#E8F0DE' : 'transparent',
              textDecoration: 'none',
              marginBottom: 2,
            })}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
