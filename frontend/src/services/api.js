const API_BASE_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

async function parseResponse(response) {
  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    throw new Error(
      payload?.detail || "The analysis service could not complete this request."
    );
  }
  return payload;
}

class ApiService {
  static async analyzeResume(resumeFile, jobDescription) {
    const formData = new FormData();
    formData.append("resume_file", resumeFile);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: "POST",
        body: formData,
      });
      return await parseResponse(response);
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error("Cannot reach the analysis API. Check the backend server.");
      }
      throw error;
    }
  }

  static async runSample() {
    const response = await fetch(`${API_BASE_URL}/api/mock-analyze`, {
      method: "POST",
    });
    return parseResponse(response);
  }

  static async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      return await parseResponse(response);
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error("Backend unavailable");
      }
      throw error;
    }
  }
}

export default ApiService;
