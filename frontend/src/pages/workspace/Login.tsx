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
      setError("Please enter your email and password.")
      return
    }
    setError("")
    setLoading(true)
    // TODO: wire to POST /api/auth/login
    await new Promise((r) => setTimeout(r, 1200))
    setLoading(false)
    navigate("/workspace")
  }

  const ssoProviders = [
    { name: "Microsoft", icon: "M" },
    { name: "Google",    icon: "G" },
    { name: "Okta",      icon: "O" },
  ]

  return (
    <div style={{
      minHeight: "100vh",
      background: "#E8F0DE",
      display: "flex",
      fontFamily: "'Inter', 'Segoe UI', sans-serif",
    }}>
      {/* Left panel — brand */}
      <div style={{
        width: "45%",
        background: "#44546A",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "48px",
        position: "relative",
        overflow: "hidden",
      }}>
        {/* Subtle background pattern */}
        <svg style={{ position: "absolute", inset: 0, opacity: 0.04 }}
          width="100%" height="100%">
          <defs>
            <pattern id="grid" width="40" height="40"
              patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40"
                fill="none" stroke="#ffffff" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)"/>
        </svg>

        {/* Logo */}
        <div style={{ position: "relative" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
            <div style={{
              width: 36, height: 36,
              background: "#FDF0E2",
              borderRadius: 8,
              display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              <span style={{ fontSize: 16, fontWeight: 600, color: "#44546A" }}>N</span>
            </div>
            <span style={{ fontSize: 20, fontWeight: 500, color: "#ffffff", letterSpacing: "0.04em" }}>
              NIRUKTA
            </span>
          </div>
          <p style={{ fontSize: 13, color: "rgba(255,255,255,0.5)", margin: 0 }}>
            Enterprise Intelligence Platform
          </p>
        </div>

        {/* Centre copy */}
        <div style={{ position: "relative" }}>
          <p style={{
            fontSize: 11, fontWeight: 500,
            color: "#FDF0E2",
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            marginBottom: 16,
            opacity: 0.7,
          }}>
            निरुक्त — Decode your data
          </p>
          <h1 style={{
            fontSize: 36, fontWeight: 500,
            color: "#ffffff",
            lineHeight: 1.2,
            margin: "0 0 20px",
          }}>
            Ask anything.<br />
            Get answers<br />
            that matter.
          </h1>
          <p style={{
            fontSize: 14,
            color: "rgba(255,255,255,0.55)",
            lineHeight: 1.7,
            maxWidth: 320,
            margin: 0,
          }}>
            Nirukta connects to your databases and documents, reasons across them, and delivers verified answers — without SQL, without dashboards, without waiting.
          </p>
        </div>

        {/* Bottom stats */}
        <div style={{
          display: "flex", gap: 32,
          position: "relative",
        }}>
          {[
            { value: "92%", label: "Answer accuracy" },
            { value: "<10s", label: "Response time" },
            { value: "49", label: "Business domains" },
          ].map((stat) => (
            <div key={stat.label}>
              <p style={{ fontSize: 22, fontWeight: 500, color: "#FDF0E2", margin: "0 0 2px" }}>
                {stat.value}
              </p>
              <p style={{ fontSize: 11, color: "rgba(255,255,255,0.45)", margin: 0 }}>
                {stat.label}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Right panel — form */}
      <div style={{
        flex: 1,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "48px 40px",
      }}>
        <div style={{ width: "100%", maxWidth: 400 }}>

          {/* Heading */}
          <h2 style={{
            fontSize: 24, fontWeight: 500,
            color: "#44546A",
            margin: "0 0 6px",
          }}>
            Sign in
          </h2>
          <p style={{
            fontSize: 13, color: "#44546A",
            opacity: 0.55, margin: "0 0 32px",
          }}>
            Welcome back. Enter your credentials to continue.
          </p>

          {/* SSO buttons */}
          <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
            {ssoProviders.map((p) => (
              <button
                key={p.name}
                style={{
                  flex: 1,
                  padding: "9px 12px",
                  background: "#ffffff",
                  border: "0.5px solid #D5DCE8",
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 500,
                  color: "#44546A",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 6,
                  transition: "background 0.15s",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = "#F7FAF5")}
                onMouseLeave={(e) => (e.currentTarget.style.background = "#ffffff")}
              >
                <span style={{
                  width: 16, height: 16,
                  background: "#E8F0DE",
                  borderRadius: 4,
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 10,
                  fontWeight: 600,
                  color: "#44546A",
                }}>{p.icon}</span>
                {p.name}
              </button>
            ))}
          </div>

          {/* Divider */}
          <div style={{
            display: "flex", alignItems: "center",
            gap: 12, marginBottom: 24,
          }}>
            <div style={{ flex: 1, height: "0.5px", background: "#D5DCE8" }}/>
            <span style={{ fontSize: 11, color: "#44546A", opacity: 0.4 }}>
              or sign in with email
            </span>
            <div style={{ flex: 1, height: "0.5px", background: "#D5DCE8" }}/>
          </div>

          {/* Form */}
          <form onSubmit={handleSignIn}>
            {/* Email */}
            <div style={{ marginBottom: 16 }}>
              <label style={{
                display: "block",
                fontSize: 12, fontWeight: 500,
                color: "#44546A",
                marginBottom: 6,
              }}>
                Work email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                style={{
                  width: "100%",
                  padding: "9px 12px",
                  background: "#ffffff",
                  border: `0.5px solid ${error && !email ? "#C0392B" : "#D5DCE8"}`,
                  borderRadius: 8,
                  fontSize: 13,
                  color: "#44546A",
                  outline: "none",
                  boxSizing: "border-box",
                  transition: "border-color 0.15s",
                  fontFamily: "inherit",
                }}
                onFocus={(e) => (e.target.style.borderColor = "#44546A")}
                onBlur={(e) => (e.target.style.borderColor = "#D5DCE8")}
              />
            </div>

            {/* Password */}
            <div style={{ marginBottom: 24 }}>
              <div style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: 6,
              }}>
                <label style={{
                  fontSize: 12, fontWeight: 500, color: "#44546A",
                }}>
                  Password
                </label>
                <button
                  type="button"
                  style={{
                    fontSize: 12, color: "#44546A",
                    opacity: 0.5, background: "none",
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
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  style={{
                    width: "100%",
                    padding: "9px 40px 9px 12px",
                    background: "#ffffff",
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
                    cursor: "pointer", fontSize: 12,
                    color: "#44546A", opacity: 0.4,
                    fontFamily: "inherit",
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
                margin: "-16px 0 16px",
                display: "flex", alignItems: "center", gap: 6,
              }}>
                <span>⚠</span> {error}
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
                transition: "background 0.15s",
                fontFamily: "inherit",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 8,
              }}
            >
              {loading ? (
                <>
                  <span style={{
                    width: 14, height: 14,
                    border: "2px solid rgba(255,255,255,0.3)",
                    borderTopColor: "#ffffff",
                    borderRadius: "50%",
                    display: "inline-block",
                    animation: "spin 0.7s linear infinite",
                  }}/>
                  Signing in...
                </>
              ) : (
                "Sign in"
              )}
            </button>
          </form>

          {/* Footer */}
          <p style={{
            fontSize: 11, color: "#44546A",
            opacity: 0.4, textAlign: "center",
            marginTop: 32, lineHeight: 1.6,
          }}>
            By signing in you agree to Nirukta's Terms of Service<br />
            and Data Privacy Policy.
          </p>
        </div>
      </div>

      {/* Spinner keyframe */}
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}
