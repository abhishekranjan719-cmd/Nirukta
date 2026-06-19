import React from "react";

export interface SuggestionItem {
  type: "text" | "tag";
  value: string;
}

export interface Suggestion {
  title: string;
  rows: SuggestionItem[][];
}

interface Props {
  suggestion: Suggestion;
  onClick: (text: string) => void;
}

const SuggestionCard: React.FC<Props> = ({
  suggestion,
  onClick,
}) => {
  const buildPrompt = (rows: SuggestionItem[][]): string => {
    return rows
      .map((row) => row.map((item) => item.value).join(" "))
      .join(" ");
  };

  return (
    <div
      className="suggestion-card"
      onClick={() => onClick(buildPrompt(suggestion.rows))}
      style={{ cursor: "pointer" }}
    >
      <h4>{suggestion.title}</h4>

      {suggestion.rows.map((row, rowIndex) => (
        <div key={rowIndex} className="content-line">
          {row.map((element, i) =>
            element.type === "tag" ? (
              <span key={i} className="tag">
                {element.value}
              </span>
            ) : (
              <span key={i} className="normal-text">
                {element.value}
              </span>
            )
          )}
        </div>
      ))}
    </div>
  );
};

export default SuggestionCard;
