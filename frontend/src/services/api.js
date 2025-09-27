/**
 * API service for communicating with the backend
 */

// Use environment variable for API URL, fallback to Vercel API for production
const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === "production" ? "/api" : "http://localhost:8000");

class ApiService {
  /**
   * Screen a resume against a job description
   * @param {File} resumeFile - PDF file
   * @param {string} jobDescription - Job description text
   * @returns {Promise<Object>} - Match results
   */
  static async screenResume(resumeFile, jobDescription) {
    try {
      const formData = new FormData();
      formData.append("resume_file", resumeFile);
      formData.append("jd_text", jobDescription);

      const response = await fetch(`${API_BASE_URL}/screen-resume`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      if (error.name === "TypeError" && error.message.includes("fetch")) {
        throw new Error(
          "UNABLE TO CONNECT TO SERVER. PLEASE ENSURE BACKEND IS RUNNING."
        );
      }
      throw error;
    }
  }

  /**
   * Check backend health
   * @returns {Promise<Object>} - Health status
   */
  static async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return await response.json();
    } catch (error) {
      throw new Error("BACKEND UNAVAILABLE");
    }
  }
}

export default ApiService;
