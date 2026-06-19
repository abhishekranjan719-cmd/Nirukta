


import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { fetchDashboardData, ChatResponse } from "../services/chat.service";
import dropDownImg from "../assets/img/Dropdown-vertical.png";
import plusImage from "../assets/img/plus.png";

const ChatExperiencePage: React.FC = () => {
  const location = useLocation();
  const message = (location.state as any)?.message;

  const [data, setData] = useState<ChatResponse | null>(null);

  useEffect(() => {
    const load = async () => {
      const response = await fetchDashboardData();
      setData(response);
    };

    load();
  }, []);

  return (
    <div className="chat-experience-layout">
      {!data ? (
        <div className="dashboard-skeleton">
            <div className="figma-skeleton">

                {/* Top List Section */}
                <div className="skeleton-list">
                    {[1, 2].map((item) => (
                    <div key={item} className="skeleton-list-row">
                        <div className="skeleton-avatar shimmer" />

                        <div className="skeleton-text-group">
                            <div className="skeleton-line title shimmer" />
                            <div className="skeleton-line width-400 shimmer" />
                            <div className="skeleton-line width-400  shimmer" />
                            <div className="skeleton-line width-150  shimmer" />
                        </div>

                        <div className="skeleton-button shimmer" />
                    </div>
                    ))}
                </div>

                {/* Two Column Cards */}
                <div className="skeleton-cards">
                    <div className="left__skeleton-cards">
                        <div className="dot__skeleton-cards">
                            <div className="dot-40 shimmer">

                            </div>
                            <div className="dot-380 shimmer">
                                
                            </div>
                        </div>
                        <div className="skeleton-big-card shimmer" />
                        <div className="dot__skeleton-cards">
                            <div className="dot-380 shimmer">
                                
                            </div>
                        </div>
                        <div className="dot__skeleton-cards">
                            <div className="dot-380 shimmer">
                                
                            </div>
                        </div>
                    </div>
                    <div className="right__skeleton-cards">
                        <div className="dot__skeleton-cards">
                            <div className="dot-40 shimmer">

                            </div>
                            <div className="dot-380 shimmer">
                                
                            </div>
                        </div>
                        <div className="skeleton-big-card shimmer" />
                        <div className="dot__skeleton-cards">
                            <div className="dot-380 shimmer">
                                
                            </div>
                        </div>
                        <div className="dot__skeleton-cards">
                            <div className="dot-380 shimmer">
                                
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
      ) : (
       
        <main className="dashboard-content">
             {/* Charts Row */}
            <div className="charts-grid">
                <div className="recruiter-card chart-card">
                    {/* Header */}
                    <div className="recruiter-card-header">
                        <div>
                        <h3 className="card-title">{data?.recruiterTimeBreakdown.title}</h3>
                        <p className="card-description">
                            {data?.recruiterTimeBreakdown.description}
                        </p>
                        </div>

                        <button className="more-btn">
                        <img src={dropDownImg} alt="dropDownImg"></img>
                        </button>
                    </div>

                    {/* Divider */}
                    <div className="divider" />

                    {/* Content */}
                    <div className="card-content">
                        {/* Left Section */}
                        <div className="content-section">
                        <div className="section-title">
                            <span>📊 Current Recruitment Metrics:</span>
                        </div>

                        <ul>
                            {data?.recruiterTimeBreakdown.metrics.map((metric, index) => (
                                <li key={index}>{metric}</li>
                            ))}
                        </ul>
                        </div>

                        {/* Right Section */}
                        <div className="content-section">
                        <div className="section-title">
                            <span>🎯 AI Opportunities:</span>
                        </div>

                        <ul>
                            {data?.recruiterTimeBreakdown.opportunities.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                        </div>
                    </div>
                    {/* Footer */}
                    <div className="card-footer">
                        <button className="pin-btn"><img src={plusImage} alt="plusImage"></img> Pin to Dashboard</button>
                    </div>
                </div>
             </div>
            <div className="charts-grid">
                <div className="recruiter-card chart-card">
                    {/* Header */}
                    <div className="recruiter-card-header">
                        <div>
                        <h3 className="card-title">{data?.benchmark.title}</h3>
                        <p className="card-description-info">
                           {data?.benchmark.description}
                        </p>
                        </div>
                    </div>

                    {/* Content */}
                    <div className="card-content">
                        <div className="chart-container">
                            Chart Goes here
                        </div>
                    </div>
                    {/* Footer */}
                    <div className="card-footer">
                        <button className="pin-btn"><img src={plusImage} alt="plusImage"></img> Pin to Dashboard</button>
                    </div>
                </div>
                <div className="recruiter-card chart-card">
                    {/* Header */}
                    <div className="recruiter-card-header">
                        <div>
                        <h3 className="card-title">{data?.benchmark.title}</h3>
                        <p className="card-description-info">
                            {data?.benchmark.description}
                        </p>
                        </div>
                    </div>

                    {/* Content */}
                    <div className="card-content">
                        <div className="chart-container">
                            Chart Goes here
                        </div>
                    </div>
                    {/* Footer */}
                    <div className="card-footer">
                        <button className="pin-btn"><img src={plusImage} alt="plusImage"></img> Pin to Dashboard</button>
                    </div>
                </div>
            </div>
        </main>

      )}
    </div>
  );
};

export default ChatExperiencePage;