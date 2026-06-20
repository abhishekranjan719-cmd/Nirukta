/**
 * Nirukt Logo — "The Decode" mark
 *
 * Concept: the left half is compressed, fragmented data (raw, unreadable).
 * A thin decode axis divides it from the right half — the resolved N,
 * marked with diamond connection nodes and a single pulse dot on the
 * diagonal, representing data in motion through the graph.
 *
 * Usage:
 *   <Logo />                          // dark tile, default 32px
 *   <Logo size={48} />                // custom size
 *   <Logo variant="light" />          // light tile for dark backgrounds
 *   <Logo showWordmark />             // renders "nirukt" beside the mark
 */

interface LogoProps {
  size?: number
  variant?: "dark" | "light"
  showWordmark?: boolean
  wordmarkSize?: number
}

export default function Logo({
  size = 32,
  variant = "dark",
  showWordmark = false,
  wordmarkSize = 18,
}: LogoProps) {
  const tile = variant === "dark" ? "#44546A" : "#FDF0E2"
  const mark = variant === "dark" ? "#FDF0E2" : "#44546A"
  const wordmarkColor = variant === "dark" ? "#44546A" : "#FDF0E2"

  const height = size * (86 / 64) // preserve the tall aspect ratio

  return (
    <div style={{ display: "flex", alignItems: "center", gap: size * 0.3 }}>
      <svg
        width={size}
        height={height}
        viewBox="0 0 64 86"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="nirukt"
        role="img"
      >
        <rect width="64" height="86" rx="11" fill={tile} />

        {/* Left half — compressed, fragmented data */}
        <line x1="7" y1="22" x2="19" y2="22" stroke={mark} strokeWidth="1.5" opacity="0.3" />
        <line x1="9" y1="29" x2="17" y2="29" stroke={mark} strokeWidth="1.5" opacity="0.45" />
        <line x1="7" y1="36" x2="20" y2="36" stroke={mark} strokeWidth="1.5" opacity="0.2" />
        <line x1="8" y1="43" x2="18" y2="43" stroke={mark} strokeWidth="1.5" opacity="0.4" />
        <line x1="7" y1="50" x2="19" y2="50" stroke={mark} strokeWidth="1.5" opacity="0.25" />
        <line x1="9" y1="57" x2="17" y2="57" stroke={mark} strokeWidth="1.5" opacity="0.35" />
        <line x1="7" y1="64" x2="20" y2="64" stroke={mark} strokeWidth="1.5" opacity="0.2" />

        {/* Decode axis */}
        <line x1="32" y1="10" x2="32" y2="76" stroke={mark} strokeWidth="0.5" opacity="0.12" />

        {/* Right half — resolved N */}
        <rect x="35" y="17" width="22" height="1.2" fill={mark} opacity="0.25" />
        <rect x="36" y="20" width="2.5" height="46" fill={mark} />
        <polygon points="38.5,21 40,21 58,65 56.5,65" fill={mark} opacity="0.7" />
        <rect x="55.5" y="20" width="2.5" height="46" fill={mark} />

        {/* Diamond connection nodes */}
        <polygon points="37.25,11 40,17.5 37.25,20 34.5,17.5" fill={mark} />
        <polygon points="56.75,11 59.5,17.5 56.75,20 54,17.5" fill={mark} />

        {/* Pulse — data in motion */}
        <circle cx="48" cy="43" r="1.8" fill={mark} opacity="0.7" />
      </svg>

      {showWordmark && (
        <span
          style={{
            fontSize: wordmarkSize,
            fontWeight: 500,
            color: wordmarkColor,
            letterSpacing: "0.05em",
          }}
        >
          nirukt
        </span>
      )}
    </div>
  )
}
