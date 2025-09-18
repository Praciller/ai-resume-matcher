import React, { useState, useEffect } from "react";
import ApiService from "../services/api";

const ResumeScreener = () => {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState("checking");

  // Check backend health on component mount
  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        await ApiService.checkHealth();
        setBackendStatus("connected");
      } catch (error) {
        setBackendStatus("disconnected");
        setError("BACKEND SERVER IS NOT RUNNING. PLEASE START THE BACKEND.");
      }
    };

    checkBackendHealth();
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      setResumeFile(file);
      setError(null);
    } else {
      setError("PLEASE SELECT A VALID PDF FILE");
      setResumeFile(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!resumeFile || !jobDescription.trim()) {
      setError("PLEASE PROVIDE BOTH JOB DESCRIPTION AND RESUME FILE");
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await ApiService.screenResume(resumeFile, jobDescription);
      setResults(data);
    } catch (err) {
      setError(err.message.toUpperCase());
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-mono font-bold text-center border-4 border-black p-4 bg-white">
          INTELLIGENT RESUME SCREENER
        </h1>

        {/* Backend Status */}
        <div className="mt-4 text-center">
          <span className="font-mono text-sm">
            BACKEND STATUS:
            <span
              className={`ml-2 font-bold ${
                backendStatus === "connected"
                  ? "text-green-600"
                  : backendStatus === "disconnected"
                  ? "text-red-600"
                  : "text-yellow-600"
              }`}
            >
              {backendStatus.toUpperCase()}
            </span>
          </span>
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-2 gap-8 h-[calc(100vh-200px)]">
        {/* Left Panel - Input */}
        <div className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Job Description Input */}
            <div>
              <label className="block text-lg font-mono font-bold mb-2 uppercase">
                JOB DESCRIPTION:
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="PASTE JOB DESCRIPTION HERE..."
                className="w-full h-64 brutalist-input resize-none"
                required
              />
            </div>

            {/* Resume File Input */}
            <div>
              <label className="block text-lg font-mono font-bold mb-2 uppercase">
                RESUME FILE (PDF):
              </label>
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="w-full brutalist-input file:mr-4 file:py-2 file:px-4 file:border-0 file:text-sm file:font-mono file:bg-black file:text-white file:uppercase file:font-bold hover:file:bg-white hover:file:text-black"
                required
              />
              {resumeFile && (
                <p className="mt-2 text-sm font-mono">
                  SELECTED: {resumeFile.name}
                </p>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-4 px-6 brutalist-button text-lg font-bold"
            >
              {isLoading ? "SCREENING..." : "SCREEN RESUME"}
            </button>
          </form>

          {/* Error Display */}
          {error && (
            <div className="brutalist-container bg-light-gray">
              <h3 className="font-mono font-bold text-lg mb-2 uppercase">
                ERROR:
              </h3>
              <p className="font-mono text-red-600">{error}</p>
            </div>
          )}
        </div>

        {/* Right Panel - Results */}
        <div className="space-y-6">
          {/* Match Score Display */}
          <div className="brutalist-container">
            <h2 className="text-2xl font-mono font-bold mb-4 uppercase">
              MATCH SCORE:
            </h2>
            <div className="text-center">
              {results ? (
                <div className="text-6xl font-mono font-bold border-4 border-black p-8 bg-light-gray">
                  {results.match_score}/100
                </div>
              ) : (
                <div className="text-6xl font-mono font-bold border-4 border-black p-8 bg-light-gray text-gray-400">
                  --/100
                </div>
              )}
            </div>
          </div>

          {/* Match Summary */}
          <div className="brutalist-container flex-1">
            <h2 className="text-2xl font-mono font-bold mb-4 uppercase">
              ANALYSIS:
            </h2>
            <div className="h-64 overflow-y-auto">
              {results ? (
                <div className="space-y-4">
                  <div>
                    <h3 className="font-mono font-bold uppercase mb-2">
                      SUMMARY:
                    </h3>
                    <p className="font-mono text-sm leading-relaxed">
                      {results.match_summary}
                    </p>
                  </div>

                  {results.detailed_analysis && (
                    <>
                      {results.detailed_analysis.skill_matches && (
                        <div>
                          <h3 className="font-mono font-bold uppercase mb-2">
                            MATCHED SKILLS:
                          </h3>
                          <p className="font-mono text-sm">
                            {results.detailed_analysis.skill_matches.join(
                              ", "
                            ) || "NONE SPECIFIED"}
                          </p>
                        </div>
                      )}

                      {results.detailed_analysis.skill_gaps && (
                        <div>
                          <h3 className="font-mono font-bold uppercase mb-2">
                            SKILL GAPS:
                          </h3>
                          <p className="font-mono text-sm">
                            {results.detailed_analysis.skill_gaps.join(", ") ||
                              "NONE IDENTIFIED"}
                          </p>
                        </div>
                      )}

                      {results.detailed_analysis.overall_recommendation && (
                        <div>
                          <h3 className="font-mono font-bold uppercase mb-2">
                            RECOMMENDATION:
                          </h3>
                          <p className="font-mono text-sm">
                            {results.detailed_analysis.overall_recommendation}
                          </p>
                        </div>
                      )}
                    </>
                  )}
                </div>
              ) : (
                <p className="font-mono text-gray-400 text-center mt-8">
                  UPLOAD A RESUME TO SEE ANALYSIS
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeScreener;
