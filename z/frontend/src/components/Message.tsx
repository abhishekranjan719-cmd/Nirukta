import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import rehypeHighlight from 'rehype-highlight'
import 'katex/dist/katex.min.css'
import type { Message as MessageType } from '../types/chat'
import MermaidDiagram from './MermaidDiagram'
import PlotlyChart from './PlotlyChart'
import SortableTable from './SortableTable'

interface MessageProps {
  message: MessageType
}

export default function Message({ message }: MessageProps) {
  const formatTime = (date: Date) => {
    return new Date(date).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className={`message ${message.role}`}>
      <div className="message-avatar">
        {message.role === 'user' ? 'U' : 'AI'}
      </div>
      <div className="message-content">
        <div className="message-bubble">
          <div className="message-text">
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[rehypeKatex, rehypeHighlight]}
              components={{
                table({ children }: any) {
                  return <SortableTable>{children}</SortableTable>
                },
                pre({ children, ...props }: any) {
                  // Check if this pre contains a mermaid or plotly code block
                  const codeChild = children?.props
                  const className = codeChild?.className || ''
                  const isMermaid = /language-mermaid/.test(className)
                  const isPlotly = /language-plotly/.test(className)

                  // If it's a mermaid or plotly block, render without the pre wrapper
                  if (isMermaid || isPlotly) {
                    return <>{children}</>
                  }

                  // Default pre rendering for other code blocks
                  return <pre {...props}>{children}</pre>
                },
                code({ className, children, ...props }: any) {
                  const match = /language-(\w+)/.exec(className || '')
                  const language = match ? match[1] : ''
                  const inline = !className

                  // Render Mermaid diagrams
                  if (!inline && language === 'mermaid') {
                    return <MermaidDiagram chart={String(children).trim()} />
                  }

                  // Render Plotly charts
                  if (!inline && language === 'plotly') {
                    return <PlotlyChart data={String(children).trim()} />
                  }

                  // Default code rendering (with syntax highlighting from rehype-highlight)
                  return (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  )
                },
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
        <div className="message-time">{formatTime(message.timestamp)}</div>
      </div>
    </div>
  )
}
