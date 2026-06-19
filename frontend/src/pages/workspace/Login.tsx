import { useState } from "react"
import { useNavigate } from "react-router-dom"

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [showPassword, setShowPassword] = useState(false)

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email || !password) {
      setError("Enter your email and password to continue.")
      return
    }
    setError("")
    setLoading(true)
    // TODO: wire to POST /api/auth/login
    await new Promise((r) => setTimeout(r, 1200))
    setLoading(false)
    navigate("/workspace")
  }

  return (
    <div style={{
      minHeight: "100vh",
      background: "#E8F0DE",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "'Inter', 'Segoe UI', sans-serif",
    }}>
      <div style={{
        background: "#ffffff",
        borderRadius: 12,
        padding: "40px",
        width: "100%",
        maxWidth: 380,
        border: "0.5px solid #D5DCE8",
      }}>

        {/* Logo */}
        <div style={{
          display: "flex", alignItems: "center",
          gap: 10, marginBottom: 32,
        }}>
          <div style={{
            width: 32, height: 32,
            background: "#FDF0E2",
            borderRadius: 6,
            display: "flex", alignItems: "center",
            justifyContent: "center",
          }}>
            <span style={{
              fontSize: 14, fontWeight: 600,
              color: "#44546A",
            }}>N</span>
          </div>
          <span style={{
            fontSize: 16, fontWeight: 500,
            color: "#44546A", letterSpacing: "0.04em",
          }}>NIRUKTA</span>
        </div>

        {/* Heading */}
        <h2 style={{
          fontSize: 20, fontWeight: 500,
          color: "#44546A", margin: "0 0 4px",
        }}>
          Welcome back
        </h2>
        <p style={{
          fontSize: 13, color: "#44546A",
          opacity: 0.5, margin: "0 0 28px",
        }}>
          Sign in to your workspace
        </p>

        {/* Form */}
        <form onSubmit={handleSignIn}>

          {/* Email */}
          <div style={{ marginBottom: 14 }}>
            <label style={{
              display: "block", fontSize: 12,
              fontWeight: 500, color: "#44546A",
              marginBottom: 6,
            }}>
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value)
                setError("")
              }}
              placeholder="you@company.com"
              autoFocus
              style={{
                width: "100%",
                padding: "9px 12px",
                background: "#FAFAFA",
                border: `0.5px solid ${error && !email ? "#C0392B" : "#D5DCE8"}`,
                borderRadius: 8,
                fontSize: 13,
                color: "#44546A",
                outline: "none",
                boxSizing: "border-box",
                fontFamily: "inherit",
              }}
              onFocus={(e) => (e.target.style.borderColor = "#44546A")}
              onBlur={(e) => (e.target.style.borderColor = "#D5DCE8")}
            />
          </div>

          {/* Password */}
          <div style={{ marginBottom: 20 }}>
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: 6,
            }}>
              <label style={{
                fontSize: 12, fontWeight: 500,
                color: "#44546A",
              }}>
                Password
              </label>
              <button
                type="button"
                style={{
                  fontSize: 12, color: "#44546A",
                  opacity: 0.45, background: "none",
                  border: "none", cursor: "pointer",
                  padding: 0, fontFamily: "inherit",
                }}
              >
                Forgot password?
              </button>
            </div>
            <div style={{ position: "relative" }}>
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value)
                  setError("")
                }}
                placeholder="••••••••"
                style={{
                  width: "100%",
                  padding: "9px 44px 9px 12px",
                  background: "#FAFAFA",
                  border: `0.5px solid ${error && !password ? "#C0392B" : "#D5DCE8"}`,
                  borderRadius: 8,
                  fontSize: 13,
                  color: "#44546A",
                  outline: "none",
                  boxSizing: "border-box",
                  fontFamily: "inherit",
                }}
                onFocus={(e) => (e.target.style.borderColor = "#44546A")}
                onBlur={(e) => (e.target.style.borderColor = "#D5DCE8")}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: "absolute", right: 12,
                  top: "50%", transform: "translateY(-50%)",
                  background: "none", border: "none",
                  cursor: "pointer", fontSize: 11,
                  color: "#44546A", opacity: 0.4,
                  fontFamily: "inherit", padding: 0,
                }}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          {/* Error */}
          {error && (
            <p style={{
              fontSize: 12, color: "#C0392B",
              margin: "-12px 0 16px",
            }}>
              {error}
            </p>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "10px",
              background: loading ? "#8A9AAD" : "#44546A",
              border: "none",
              borderRadius: 8,
              fontSize: 13,
              fontWeight: 500,
              color: "#ffffff",
              cursor: loading ? "not-allowed" : "pointer",
              fontFamily: "inherit",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 8,
              transition: "background 0.15s",
            }}
          >
            {loading ? (
              <>
                <span style={{
                  width: 13, height: 13,
                  border: "2px solid rgba(255,255,255,0.3)",
                  borderTopColor: "#ffffff",
                  borderRadius: "50%",
                  display: "inline-block",
                  animation: "spin 0.7s linear infinite",
                }}/>
                Signing in...
              </>
            ) : "Sign in"}
          </button>

        </form>
      </div>

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  )
}
