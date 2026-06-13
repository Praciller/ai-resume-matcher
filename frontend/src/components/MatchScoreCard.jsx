export default function MatchScoreCard({ score, summary }) {
  const label =
    score >= 80 ? "Strong alignment" : score >= 60 ? "Partial alignment" : "Early fit";

  return (
    <section className="report-section score-section" aria-labelledby="score-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Role fit</p>
          <h2 id="score-title">{label}</h2>
        </div>
        <span className="score-badge" aria-label={`Match score ${score} out of 100`}>
          {score}/100
        </span>
      </div>
      <div
        className="score-track"
        role="progressbar"
        aria-valuemin="0"
        aria-valuemax="100"
        aria-valuenow={score}
      >
        <span style={{ width: `${score}%` }} />
      </div>
      <p className="report-summary">{summary}</p>
    </section>
  );
}
