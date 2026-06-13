import { useEffect, useMemo, useState } from "react";
import { CircleCheck, CircleDashed, CircleX, FileSearch } from "lucide-react";

import ApiService from "../services/api";
import AnalysisLoadingState from "./AnalysisLoadingState";
import AnalysisReport from "./AnalysisReport";
import AnalyzeButton from "./AnalyzeButton";
import ErrorState from "./ErrorState";
import JobDescriptionInput from "./JobDescriptionInput";
import ResumeUpload from "./ResumeUpload";
import SampleDemoMode from "./SampleDemoMode";

const DEFAULT_LIMITS = {
  max_resume_file_mb: 5,
  max_jd_chars: 20_000,
};

function ConnectionState({ status, health }) {
  const config = {
    checking: [CircleDashed, "Checking API"],
    connected: [CircleCheck, health?.mode === "mock" ? "Mock mode" : "API ready"],
    disconnected: [CircleX, "API unavailable"],
  };
  const [Icon, label] = config[status];
  return (
    <div className={`connection-state ${status}`}>
      <Icon aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}

export default function ResumeScreener() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [fileError, setFileError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");
  const [backendStatus, setBackendStatus] = useState("checking");
  const [health, setHealth] = useState(null);

  useEffect(() => {
    let active = true;
    ApiService.checkHealth()
      .then((payload) => {
        if (!active) return;
        setHealth(payload);
        setBackendStatus("connected");
      })
      .catch(() => {
        if (!active) return;
        setBackendStatus("disconnected");
      });
    return () => {
      active = false;
    };
  }, []);

  const limits = health || DEFAULT_LIMITS;
  const maxFileBytes = limits.max_resume_file_mb * 1024 * 1024;
  const formValid = useMemo(
    () =>
      Boolean(resumeFile) &&
      !fileError &&
      jobDescription.trim().length >= 20 &&
      backendStatus === "connected",
    [resumeFile, fileError, jobDescription, backendStatus]
  );

  const handleFileChange = (event) => {
    const file = event.target.files?.[0] || null;
    setResults(null);
    if (!file) {
      setResumeFile(null);
      setFileError("");
      return;
    }
    if (!file.name.toLowerCase().endsWith(".pdf") || file.type !== "application/pdf") {
      setResumeFile(null);
      setFileError("Choose a file with PDF extension and application/pdf type.");
      return;
    }
    if (file.size > maxFileBytes) {
      setResumeFile(null);
      setFileError(`PDF must be ${limits.max_resume_file_mb} MB or smaller.`);
      return;
    }
    setResumeFile(file);
    setFileError("");
  };

  const runRequest = async (request) => {
    setIsLoading(true);
    setError("");
    setResults(null);
    try {
      const payload = await request();
      setResults(payload);
      window.requestAnimationFrame(() => {
        document.getElementById("analysis-report")?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!formValid) return;
    runRequest(() => ApiService.analyzeResume(resumeFile, jobDescription.trim()));
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-mark" aria-hidden="true">
          <FileSearch />
        </div>
        <div>
          <p className="eyebrow">Application evidence review</p>
          <h1>AI Resume Matcher</h1>
        </div>
        <ConnectionState status={backendStatus} health={health} />
      </header>

      <div className="workspace">
        <aside className="input-panel" aria-labelledby="input-title">
          <div className="panel-intro">
            <p className="eyebrow">Step 1</p>
            <h2 id="input-title">Compare your evidence</h2>
            <p>
              Upload a text-based PDF and paste one job description. The API
              validates both before sending content to a server-side model.
            </p>
          </div>

          <ErrorState message={error} />

          <form onSubmit={handleSubmit}>
            <ResumeUpload
              file={resumeFile}
              maxFileMb={limits.max_resume_file_mb}
              onChange={handleFileChange}
              error={fileError}
              disabled={isLoading}
            />
            <JobDescriptionInput
              value={jobDescription}
              maxChars={limits.max_jd_chars}
              onChange={(event) => {
                setJobDescription(event.target.value);
                setResults(null);
              }}
              disabled={isLoading}
            />
            <AnalyzeButton disabled={!formValid || isLoading} isLoading={isLoading} />
          </form>

          <SampleDemoMode
            onRun={() => runRequest(() => ApiService.runSample())}
            disabled={isLoading || backendStatus !== "connected"}
          />
        </aside>

        <section id="analysis-report" className="report-panel" aria-label="Analysis report">
          {isLoading ? (
            <AnalysisLoadingState />
          ) : results ? (
            <AnalysisReport result={results} />
          ) : (
            <div className="empty-report">
              <p className="eyebrow">Step 2</p>
              <h2>Read the match report</h2>
              <p>
                Results will separate matched evidence, unclear skills, actions,
                learning priorities, and interview questions.
              </p>
              <div className="empty-lines" aria-hidden="true">
                <span />
                <span />
                <span />
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
