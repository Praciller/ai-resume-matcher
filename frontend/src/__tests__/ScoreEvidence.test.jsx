import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import ScoreEvidence from "../components/ScoreEvidence";

const breakdown = {
  skills_considered: 5,
  matched_count: 3,
  partial_count: 1,
  missing_count: 1,
  coverage: 0.6,
  formula: "round(48 + matched/considered * 42)",
};

const evidence = [
  {
    skill: "python",
    status: "matched",
    source: "resume",
    evidence_quote: "Built data pipelines in Python.",
  },
  {
    skill: "kubernetes",
    status: "partial",
    source: "resume",
    evidence_quote: "Familiar with K8s clusters.",
  },
];

const limitations = [
  "Keyword-based matching cannot verify the depth, recency, or quality of experience.",
];

describe("ScoreEvidence", () => {
  test("renders breakdown, evidence quotes, and limitations", () => {
    render(
      <ScoreEvidence
        breakdown={breakdown}
        evidence={evidence}
        limitations={limitations}
      />
    );
    expect(screen.getByText(/3 of 5 recognized requirement keywords matched/)).toBeInTheDocument();
    expect(screen.getByText(/1 matched only through a known alias/)).toBeInTheDocument();
    expect(screen.getByText(/Built data pipelines in Python\./)).toBeInTheDocument();
    expect(screen.getByText(/Familiar with K8s clusters\./)).toBeInTheDocument();
    expect(screen.getByText("Limitations")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Keyword-based matching cannot verify the depth, recency, or quality of experience."
      )
    ).toBeInTheDocument();
  });

  test("renders nothing when no provenance fields are present", () => {
    const { container } = render(
      <ScoreEvidence breakdown={null} evidence={[]} limitations={[]} />
    );
    expect(container).toBeEmptyDOMElement();
  });
});
