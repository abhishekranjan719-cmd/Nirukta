import { createContext, useContext, useState, ReactNode } from 'react'

interface AuthContextType {
  user: { name: string; email: string; role: string } | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthContextType['user']>(null)

  const login = async (email: string, _password: string) => {
    // TODO: wire to backend /api/auth/login
    setUser({ name: 'Abhishek', email, role: 'AI Admin' })
    localStorage.setItem('nirukta_token', 'demo-token')
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('nirukta_token')
    window.location.href = '/login'
  }

  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
