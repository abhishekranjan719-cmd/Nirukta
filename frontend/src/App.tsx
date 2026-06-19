import { Routes, Route, Navigate } from 'react-router-dom'

// Workspace pages
import Login from '@/pages/workspace/Login'
import Home from '@/pages/workspace/Home'
import Conversation from '@/pages/workspace/Conversation'
import Results from '@/pages/workspace/Results'
import DrillDown from '@/pages/workspace/DrillDown'
import ReportBuilder from '@/pages/workspace/ReportBuilder'
import ActionCenter from '@/pages/workspace/ActionCenter'
import AlertCenter from '@/pages/workspace/AlertCenter'
import ConversationHistory from '@/pages/workspace/ConversationHistory'

// Control Center pages
import CCOverview from '@/pages/control-center/Overview'
import CCAgents from '@/pages/control-center/Agents'
import CCPrompts from '@/pages/control-center/Prompts'
import CCEvaluation from '@/pages/control-center/Evaluation'
import CCAccuracy from '@/pages/control-center/Accuracy'
import CCKnowledgeBase from '@/pages/control-center/KnowledgeBase'
import CCModels from '@/pages/control-center/Models'
import CCCost from '@/pages/control-center/Cost'
import CCObservability from '@/pages/control-center/Observability'
import CCGovernance from '@/pages/control-center/Governance'
import CCUsers from '@/pages/control-center/Users'
import CCSettings from '@/pages/control-center/Settings'

export default function App() {
  return (
    <Routes>
      {/* Auth */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />

      {/* Intelligence Workspace */}
      <Route path="/workspace" element={<Home />} />
      <Route path="/workspace/conversation/:id?" element={<Conversation />} />
      <Route path="/workspace/results" element={<Results />} />
      <Route path="/workspace/drill-down" element={<DrillDown />} />
      <Route path="/workspace/reports" element={<ReportBuilder />} />
      <Route path="/workspace/actions" element={<ActionCenter />} />
      <Route path="/workspace/alerts" element={<AlertCenter />} />
      <Route path="/workspace/history" element={<ConversationHistory />} />

      {/* Control Center */}
      <Route path="/control-center" element={<CCOverview />} />
      <Route path="/control-center/agents" element={<CCAgents />} />
      <Route path="/control-center/prompts" element={<CCPrompts />} />
      <Route path="/control-center/evaluation" element={<CCEvaluation />} />
      <Route path="/control-center/accuracy" element={<CCAccuracy />} />
      <Route path="/control-center/knowledge-base" element={<CCKnowledgeBase />} />
      <Route path="/control-center/models" element={<CCModels />} />
      <Route path="/control-center/cost" element={<CCCost />} />
      <Route path="/control-center/observability" element={<CCObservability />} />
      <Route path="/control-center/governance" element={<CCGovernance />} />
      <Route path="/control-center/users" element={<CCUsers />} />
      <Route path="/control-center/settings" element={<CCSettings />} />
    </Routes>
  )
}
