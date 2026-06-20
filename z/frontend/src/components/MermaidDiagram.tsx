import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

interface MermaidDiagramProps {
  chart: string
}

// Initialize mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif',
})

export default function MermaidDiagram({ chart }: MermaidDiagramProps) {
  const [svg, setSvg] = useState<string>('')
  const [error, setError] = useState<string>('')
  const idRef = useRef(`mermaid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`)

  useEffect(() => {
    const renderDiagram = async () => {
      try {
        console.log('Rendering Mermaid diagram:', chart)
        const { svg: renderedSvg } = await mermaid.render(idRef.current, chart)
        console.log('Mermaid render success')
        setSvg(renderedSvg)
        setError('')
      } catch (err: any) {
        console.error('Mermaid rendering error:', err)
        setError(`Failed to render diagram: ${err.message || err}`)
        setSvg('')
      }
    }

    renderDiagram()
  }, [chart])

  if (error) {
    return (
      <div style={{ padding: '16px', background: '#fee', color: '#c00', borderRadius: '8px', border: '1px solid #fcc' }}>
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>Mermaid Syntax Error</div>
        <div style={{ marginBottom: '12px' }}>{error}</div>
        <details style={{ marginTop: '8px' }}>
          <summary style={{ cursor: 'pointer', fontWeight: '500' }}>Show diagram code</summary>
          <pre style={{
            marginTop: '8px',
            padding: '8px',
            background: '#fff',
            color: '#333',
            borderRadius: '4px',
            fontSize: '12px',
            overflow: 'auto',
            maxHeight: '200px'
          }}>
            {chart}
          </pre>
        </details>
      </div>
    )
  }

  return <div className="mermaid" dangerouslySetInnerHTML={{ __html: svg }} />
}
