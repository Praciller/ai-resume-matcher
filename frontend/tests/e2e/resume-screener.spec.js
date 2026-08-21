import { expect, test } from "@playwright/test";

const health = {
  status: "healthy",
  mode: "live",
  configured_providers: ["external"],
  primary_provider: "external",
  max_resume_file_mb: 5,
  max_resume_chars: 20_000,
  max_jd_chars: 20_000,
};

const sample = {
  match_score: 78,
  summary:
    "The candidate aligns well with the role and has useful evidence for the core requirements.",
  matched_skills: ["React", "Python"],
  missing_skills: ["AWS"],
  strengths: ["Built production interfaces"],
  weaknesses: ["Cloud impact is unclear"],
  recommendations: ["Add a quantified AWS deployment project to the resume."],
  learning_plan: [],
  interview_questions: ["How did you validate your API in production?"],
  risk_flags: [],
  model_used: "deterministic-sample-v1",
  provider_used: "mock",
  cached: false,
  analysis_id: "sample-demo",
  warnings: ["Sample data only. No resume was uploaded."],
};

test.beforeEach(async ({ page }) => {
  await page.route("**/api/health", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(health) })
  );
  await page.route("**/api/mock-analyze", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(sample) })
  );
  await page.goto("/");
});

test("loads core form and status", async ({ page }) => {
  await expect(page).toHaveTitle("AI Resume Matcher");
  await expect(page.getByRole("heading", { name: "AI Resume Matcher" })).toBeVisible();
  await expect(page.getByLabel("Resume PDF")).toBeVisible();
  await expect(page.getByLabel("Job description")).toBeVisible();
  await expect(page.getByText("API ready")).toBeVisible();
});

test("sample mode renders structured result", async ({ page }) => {
  await page.getByRole("button", { name: "Run sample" }).click();

  await expect(page.getByText("78/100")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Skills" })).toBeVisible();
  await expect(page.getByText("React")).toBeVisible();
  await expect(page.getByText("Questions to rehearse")).toBeVisible();
});

test("mobile layout remains usable", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });

  await expect(page.getByRole("heading", { name: "Compare your evidence" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Run sample" })).toBeVisible();
  await expect(page.getByLabel("Job description")).toBeVisible();
});
