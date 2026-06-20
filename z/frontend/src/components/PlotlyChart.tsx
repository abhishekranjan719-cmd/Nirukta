import { useEffect, useRef, useState } from 'react'
// @ts-ignore
import Plotly from 'plotly.js-dist-min'

interface PlotlyChartProps {
  data: string
}

export default function PlotlyChart({ data }: PlotlyChartProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const renderChart = async () => {
      if (!containerRef.current) return

      try {
        console.log('Rendering Plotly chart:', data)

        // Parse the JSON data
        const chartData = JSON.parse(data)

        // Extract data, layout, and config
        const plotData = chartData.data || []
        const plotLayout = {
          ...chartData.layout,
          autosize: true,
          margin: { l: 50, r: 30, t: 50, b: 50 },
        }
        const plotConfig = {
          responsive: true,
          displayModeBar: true,
          displaylogo: false,
          modeBarButtonsToRemove: ['toImage'],
          ...chartData.config,
        }

        // Clear any existing plot
        containerRef.current.innerHTML = ''

        // Render the plot
        await Plotly.newPlot(
          containerRef.current,
          plotData,
          plotLayout,
          plotConfig
        )

        console.log('Plotly render success')
        setError('')
      } catch (err: any) {
        console.error('Plotly rendering error:', err)
        setError(`Failed to render chart: ${err.message || err}`)
      }
    }

    renderChart()

    // Cleanup on unmount
    return () => {
      if (containerRef.current) {
        Plotly.purge(containerRef.current)
      }
    }
  }, [data])

  if (error) {
    return (
      <div style={{ padding: '12px', background: '#fee', color: '#c00', borderRadius: '4px' }}>
        {error}
      </div>
    )
  }

  return <div ref={containerRef} className="plotly-chart" />
}
