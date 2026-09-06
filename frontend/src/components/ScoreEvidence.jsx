export default function ScoreEvidence({ breakdown, evidence, limitations }) {
  const hasBreakdown = Boolean(breakdown);
  const hasEvidence = Array.isArray(evidence) && evidence.length > 0;
  const hasLimitations = Array.isArray(limitations) && limitations.length > 0;

  if (!hasBreakdown && !hasEvidence && !hasLimitations) {
    return null;
  }

  return (
    <section className="report-section" aria-labelledby="provenance-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Score provenance</p>
          <h2 id="provenance-title">How this score was computed</h2>
        </div>
      </div>
      {hasBreakdown && (
        <ul className="plain-list breakdown-list">
          <li>
            {breakdown.matched_count} of {breakdown.skills_considered} recognized
            requirement keywords matched
            {breakdown.partial_count > 0 &&
              `, ${breakdown.partial_count} matched only through a known alias`}
            {breakdown.missing_count > 0 &&
              `, ${breakdown.missing_count} missing`}
            .
          </li>
          <li>
            Formula: <code>{breakdown.formula}</code>
          </li>
        </ul>
      )}
      {hasEvidence && (
        <div>
          <h3>Evidence from the resume</h3>
          <ul className="plain-list">
            {evidence.map((item) => (
              <li key={`${item.skill}-${item.evidence_quote}`}>
                <strong>{item.skill}</strong>
                {item.status === "partial" && " (alias match)"}: &ldquo;{item.evidence_quote}&rdquo;
              </li>
            ))}
          </ul>
        </div>
      )}
      {hasLimitations && (
        <div>
          <h3>Limitations</h3>
          <ul className="plain-list">
            {limitations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
