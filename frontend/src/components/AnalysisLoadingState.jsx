export default function AnalysisLoadingState() {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <span className="sr-only">Analyzing resume and job description.</span>
      <div className="skeleton-line skeleton-short" />
      <div className="skeleton-line" />
      <div className="skeleton-line" />
      <div className="skeleton-grid">
        <div className="skeleton-block" />
        <div className="skeleton-block" />
      </div>
    </div>
  );
}
