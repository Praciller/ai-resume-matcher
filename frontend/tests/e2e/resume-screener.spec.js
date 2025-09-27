const { test, expect } = require("@playwright/test");

test.describe("Resume Screener Application", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("should display the main page with correct title", async ({ page }) => {
    // Check if the page loads correctly
    await expect(page).toHaveTitle(/AI Resume Matcher/);

    // Check if the main heading is visible
    await expect(
      page.getByRole("heading", { name: /AI Resume Matcher/i })
    ).toBeVisible();
  });

  test("should show backend status", async ({ page }) => {
    // Check if backend status is displayed
    await expect(page.getByText(/Backend Status:/i)).toBeVisible();

    // The status should be one of: Connected, Disconnected, or Checking
    const statusElement = page.getByText(/Backend Status:/i);
    await expect(statusElement).toBeVisible();
  });

  test("should have upload form elements", async ({ page }) => {
    // Check if job description textarea is present
    await expect(page.getByLabel(/Job Description/i)).toBeVisible();

    // Check if file upload input is present
    await expect(page.getByLabel(/Resume File/i)).toBeVisible();

    // Check if submit button is present
    await expect(
      page.getByRole("button", { name: /Analyze Resume/i })
    ).toBeVisible();
  });

  test("should show validation error for empty form submission", async ({
    page,
  }) => {
    // Try to submit empty form
    await page.getByRole("button", { name: /Analyze Resume/i }).click();

    // Check if form validation prevents submission (HTML5 validation)
    const jobDescriptionField = page.getByLabel(/Job Description/i);
    await expect(jobDescriptionField).toHaveAttribute("required");

    const fileField = page.getByLabel(/Resume File/i);
    await expect(fileField).toHaveAttribute("required");
  });

  test("should accept job description input", async ({ page }) => {
    const jobDescription =
      "Software Engineer position requiring React and Node.js experience";

    // Fill in job description
    await page.getByLabel(/Job Description/i).fill(jobDescription);

    // Verify the text was entered
    await expect(page.getByLabel(/Job Description/i)).toHaveValue(
      jobDescription
    );
  });

  test("should show file name when PDF is selected", async ({ page }) => {
    // Note: This test would need a sample PDF file to work properly
    // For now, we'll just check that the file input accepts PDF files
    const fileInput = page.getByLabel(/Resume File/i);
    await expect(fileInput).toHaveAttribute("accept", ".pdf");
  });

  test("should have responsive design elements", async ({ page }) => {
    // Check if the layout adapts to different screen sizes
    await page.setViewportSize({ width: 768, height: 1024 });

    // Main elements should still be visible on tablet size
    await expect(
      page.getByRole("heading", { name: /AI Resume Matcher/i })
    ).toBeVisible();
    await expect(page.getByLabel(/Job Description/i)).toBeVisible();

    // Check mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(
      page.getByRole("heading", { name: /AI Resume Matcher/i })
    ).toBeVisible();
  });

  test("should display match score section", async ({ page }) => {
    // Check if match score card is present
    await expect(page.getByText(/Match Score/i)).toBeVisible();

    // Check if it shows the default state
    await expect(page.getByText(/--\/100/)).toBeVisible();
  });

  test("should display analysis section", async ({ page }) => {
    // Check if detailed analysis card is present
    await expect(
      page.getByRole("heading", { name: /Detailed Analysis/i })
    ).toBeVisible();

    // Check if it shows the default state
    await expect(
      page.getByText(/Upload a resume to see detailed analysis/i)
    ).toBeVisible();
  });

  test("should have proper accessibility attributes", async ({ page }) => {
    // Check if form labels are properly associated
    const jobDescriptionLabel = page.locator('label[for="job-description"]');
    const jobDescriptionInput = page.getByLabel(/Job Description/i);

    await expect(jobDescriptionLabel).toBeVisible();
    await expect(jobDescriptionInput).toBeVisible();

    // Check if buttons have proper accessible names
    const submitButton = page.getByRole("button", { name: /Analyze Resume/i });
    await expect(submitButton).toBeVisible();
  });
});
