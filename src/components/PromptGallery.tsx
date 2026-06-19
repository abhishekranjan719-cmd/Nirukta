import React from "react";
import filterImg from "../assets/img/filter-one.png";
import SuggestionCard, {
  Suggestion,
} from "./SuggestionCard";

interface Props {
  onSuggestionClick: (text: string) => void;
}

const suggestions: Suggestion[] = [
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

// Duplicate for grid layout (like your image)
const galleryData: Suggestion[] = Array(12)
  .fill(null)
  .map((_, i) => ({
    ...suggestions[0],
    title: `Company Work`,
  }));

const PromptGallery: React.FC<Props> = ({
  onSuggestionClick,
}) => {
  return (
    <>
     

      {/* Main */}
      <main className="dashboard-content width__dashboard-content width__dashboard-content-prompt">
        <div className="wrapper">

          {/* Top Section */}
          <div className="prompt-gallery-header">
            <h3>Prompt Gallery</h3>
            <button className="filter-btn"><img src={filterImg} alt="arrow" /> Filters</button>
          </div>

          {/* Cards Grid */}
          <div className="card-container gallery__card-container">
            {galleryData.map((item, index) => (
              <SuggestionCard
                key={index}
                suggestion={item}
                onClick={onSuggestionClick}
              />
            ))}
          </div>

        </div>
      </main>
    </>
  );
};

export default PromptGallery;
