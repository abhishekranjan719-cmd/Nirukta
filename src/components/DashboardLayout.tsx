// DashbaordLayout.tsx file

import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";
import DashboardContent from "./DashboardContent";
import PromptGallery from "./PromptGallery";
import ChatPanel from "./ChatPanel";
import ChatExperiencePage from "../pages/ChatExperiencePage";

const DashboardLayout: React.FC = () => {
  const [isChatOpen, setIsChatOpen] = useState(true);
  const [chatInput, setChatInput] = useState("");

  const handleSuggestionClick = (text: string) => {
    setChatInput(text);
    setIsChatOpen(true);
  };

  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="main-content">
        <Header onToggleChat={() => setIsChatOpen(!isChatOpen)} />
          <div className="page-content">
            <Routes>
              <Route
                path="/"
                element={
                  <DashboardContent
                    onToggleChat={() => setIsChatOpen(!isChatOpen)}
                    onSuggestionClick={handleSuggestionClick}
                    loadingStep={0}
                  />
                }
              />

              <Route
                path="/prompt-gallery"
                element={
                  <PromptGallery
                    onSuggestionClick={handleSuggestionClick}
                  />
                }
              />

            
              <Route
                path="/chat-experience"
                element={<ChatExperiencePage />}
              />
            </Routes>
          </div>
        
      </div>

      {isChatOpen && (
        <ChatPanel
          onClose={() => setIsChatOpen(false)}
          chatInput={chatInput}
          setChatInput={setChatInput}
        />
      )}
    </div>
  );
};

export default DashboardLayout;
