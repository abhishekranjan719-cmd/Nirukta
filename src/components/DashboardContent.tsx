// DashbaordContent.tsx file

import React from "react";
import { useNavigate } from "react-router-dom";
import mainImage from "../assets/img/rocket-bg.png";
import starImg from "../assets/img/stars-01.svg";
import DownArrowImg from "../assets/img/arrow-narrow-down.svg";

import SuggestionCard, {
  Suggestion,
} from "./SuggestionCard";

interface Props {
  onToggleChat: () => void;
  onSuggestionClick: (text: string) => void;
  loadingStep: number;
}

const suggestions: Suggestion[] = [
  {
    title: "Policy Work",
    rows: [
      [
        { type: "text", value: "Provide a" },
        { type: "tag", value: "related query" },
      ],
      [
        { type: "text", value: "for" },
        { type: "tag", value: "business findings" },
      ],
      [
        { type: "text", value: "about" },
        { type: "tag", value: "topic" },
      ],
    ],
  },
  {
    title: "Company Work",
    rows: [
      [
        { type: "text", value: "Provide a" },
        { type: "tag", value: "related work section" },
      ],
      [
        { type: "text", value: "for" },
        { type: "tag", value: "research / business findings" },
      ],
      [
        { type: "text", value: "about" },
        { type: "tag", value: "topic" },
      ],
    ],
  },
  {
    title: "Company Work",
    rows: [
      [
        { type: "text", value: "Provide a" },
        { type: "tag", value: "related work section" },
      ],
      [
        { type: "text", value: "for" },
        { type: "tag", value: "research / business findings" },
      ],
      [
        { type: "text", value: "about" },
        { type: "tag", value: "topic" },
      ],
    ],
  },
];

const DashboardContent: React.FC<Props> = ({
  onToggleChat,
  onSuggestionClick,
}) => {
  const navigate = useNavigate();

  return (
    <>
     

      {/* Main Content */}
      <main className="dashboard-content width__dashboard-content">
        <div className="wrapper">

          {/* Rocket Section */}
          <div className="box__wrapper">
            <img src={mainImage} alt="Main" />
            <div className="box__wrapper-info">
              <h3>
                Transform Ideas into Action in Hours, Not Weeks
              </h3>
              <p>
                Launch your next project with AI-powered design
                sessions. From business requirements to
                ready-to-build backlogs complete with
                documentation, architecture, and infrastructure
                code all generated through natural conversation
                with specialized AI personas.
              </p>
            </div>
          </div>

          {/* Prompt Suggestions Button */}
          <div className="suggestion-header">
            <button
              onClick={() => navigate("/prompt-gallery")}
            >
              <img src={starImg} alt="star" />
              <span>Prompt Suggestions</span>
            </button>
          </div>

          {/* Suggestion Cards */}
          <div className="card-container">
            {suggestions.map((item, index) => (
              <SuggestionCard
                key={index}
                suggestion={item}
                onClick={onSuggestionClick}
              />
            ))}
          </div>

          {/* Show More */}
          <div className="show-more">
            <button onClick={() => navigate("/prompt-gallery")}>
              Show more
              <img src={DownArrowImg} alt="arrow" />
            </button>
          </div>

        </div>
      </main>
    </>
  );
};

export default DashboardContent;
