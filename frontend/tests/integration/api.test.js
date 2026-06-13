import { afterEach, describe, expect, test, vi } from "vitest";

import ApiService from "../../src/services/api";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("ApiService", () => {
  test("checks the health endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: "healthy", mode: "live" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const result = await ApiService.checkHealth();

    expect(result.status).toBe("healthy");
    expect(fetchMock).toHaveBeenCalledWith("/api/health");
  });

  test("posts resume and job description to analyze endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ match_score: 80 }),
    });
    vi.stubGlobal("fetch", fetchMock);
    const file = new File(["resume"], "candidate.pdf", {
      type: "application/pdf",
    });

    await ApiService.analyzeResume(file, "Senior React engineer role");

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/analyze",
      expect.objectContaining({
        method: "POST",
        body: expect.any(FormData),
      })
    );
    const formData = fetchMock.mock.calls[0][1].body;
    expect(formData.get("resume_file")).toBe(file);
    expect(formData.get("job_description")).toBe("Senior React engineer role");
  });

  test("posts to deterministic sample endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ provider_used: "mock" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const result = await ApiService.runSample();

    expect(result.provider_used).toBe("mock");
    expect(fetchMock).toHaveBeenCalledWith("/api/mock-analyze", {
      method: "POST",
    });
  });

  test("returns controlled API detail", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ detail: "Resume MIME type must be application/pdf." }),
      })
    );

    await expect(ApiService.runSample()).rejects.toThrow(
      "Resume MIME type must be application/pdf."
    );
  });

  test("translates network failure", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("fetch failed")));

    await expect(ApiService.checkHealth()).rejects.toThrow("Backend unavailable");
  });
});
