import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, test, vi } from "vitest";

import ResumeScreener from "../components/ResumeScreener";
import ApiService from "../services/api";

vi.mock("../services/api", () => ({
  default: {
    checkHealth: vi.fn(),
    analyzeResume: vi.fn(),
    runSample: vi.fn(),
  },
}));

const health = {
  status: "healthy",
  mode: "live",
  configured_providers: ["9arm", "gemini"],
  primary_provider: "9arm",
  max_resume_file_mb: 5,
  max_resume_chars: 20_000,
  max_jd_chars: 20_000,
};

const result = {
  match_score: 78,
  summary:
    "The candidate aligns well with the role and has useful evidence for the core requirements.",
  matched_skills: ["React", "Python"],
  missing_skills: ["AWS"],
  strengths: ["Built production interfaces"],
  weaknesses: ["Cloud impact is unclear"],
  recommendations: ["Add a quantified AWS deployment project to the resume."],
  learning_plan: [
    {
      priority: "high",
      skill: "AWS",
      reason: "The job requires cloud deployment experience.",
      suggested_action: "Deploy one API and document reliability metrics.",
    },
  ],
  interview_questions: ["How did you validate your API in production?"],
  risk_flags: ["Cloud experience is not explicit."],
  model_used: "qwen3.6-35b-a3b",
  provider_used: "9arm",
  cached: false,
  analysis_id: "abc123",
  warnings: [],
};

describe("ResumeScreener", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    ApiService.checkHealth.mockResolvedValue(health);
  });

  test("renders required inputs and connected status", async () => {
    render(<ResumeScreener />);

    expect(screen.getByRole("heading", { name: "AI Resume Matcher" })).toBeVisible();
    expect(screen.getByLabelText("Resume PDF")).toBeVisible();
    expect(screen.getByLabelText("Job description")).toBeVisible();

    await waitFor(() => {
      expect(screen.getByText("API ready")).toBeVisible();
    });
  });

  test("shows PDF name and size", async () => {
    const user = userEvent.setup();
    render(<ResumeScreener />);
    const file = new File(["resume"], "candidate.pdf", {
      type: "application/pdf",
    });

    await user.upload(screen.getByLabelText("Resume PDF"), file);

    expect(screen.getByText("candidate.pdf")).toBeVisible();
    expect(screen.getByText("0.00 MB")).toBeVisible();
  });

  test("rejects non-PDF files", async () => {
    const user = userEvent.setup({ applyAccept: false });
    render(<ResumeScreener />);
    const file = new File(["resume"], "candidate.txt", { type: "text/plain" });

    await user.upload(screen.getByLabelText("Resume PDF"), file);

    expect(
      screen.getByText("Choose a file with PDF extension and application/pdf type.")
    ).toBeVisible();
  });

  test("keeps analyze disabled until inputs are valid", async () => {
    const user = userEvent.setup();
    render(<ResumeScreener />);
    const button = screen.getByRole("button", { name: /Analyze resume/i });
    expect(button).toBeDisabled();

    await user.type(
      screen.getByLabelText("Job description"),
      "Senior engineer role requiring React and Python."
    );
    await user.upload(
      screen.getByLabelText("Resume PDF"),
      new File(["resume"], "candidate.pdf", { type: "application/pdf" })
    );

    await waitFor(() => expect(button).toBeEnabled());
  });

  test("submits valid inputs and renders structured result", async () => {
    const user = userEvent.setup();
    ApiService.analyzeResume.mockResolvedValue(result);
    render(<ResumeScreener />);
    const file = new File(["resume"], "candidate.pdf", {
      type: "application/pdf",
    });
    const jd = "Senior engineer role requiring React, Python, and AWS.";

    await user.upload(screen.getByLabelText("Resume PDF"), file);
    await user.type(screen.getByLabelText("Job description"), jd);
    await user.click(screen.getByRole("button", { name: /Analyze resume/i }));

    await waitFor(() => {
      expect(ApiService.analyzeResume).toHaveBeenCalledWith(file, jd);
    });
    expect(await screen.findByText("78/100")).toBeVisible();
    expect(screen.getByText("React")).toBeVisible();
    expect(screen.getAllByText("AWS").length).toBeGreaterThan(0);
    expect(screen.getByText("Questions to rehearse")).toBeVisible();
  });

  test("runs sample mode without uploaded inputs", async () => {
    const user = userEvent.setup();
    ApiService.runSample.mockResolvedValue(result);
    render(<ResumeScreener />);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Run sample" })).toBeEnabled();
    });
    await user.click(screen.getByRole("button", { name: "Run sample" }));

    expect(await screen.findByText("78/100")).toBeVisible();
    expect(ApiService.runSample).toHaveBeenCalledOnce();
  });

  test("shows controlled API errors", async () => {
    const user = userEvent.setup();
    ApiService.runSample.mockRejectedValue(
      new Error("AI analysis is temporarily unavailable.")
    );
    render(<ResumeScreener />);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Run sample" })).toBeEnabled();
    });
    await user.click(screen.getByRole("button", { name: "Run sample" }));

    expect(
      await screen.findByText("AI analysis is temporarily unavailable.")
    ).toBeVisible();
  });
});
