export default function Recommendations({ strengths, weaknesses, recommendations }) {
  return (
    <section className="report-section" aria-labelledby="recommendations-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Application strategy</p>
          <h2 id="recommendations-title">Evidence and next actions</h2>
        </div>
      </div>
      <div className="evidence-columns">
        <div>
          <h3>Strengths to keep</h3>
          <ul className="plain-list">
            {strengths.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
        <div>
          <h3>Weak evidence</h3>
          <ul className="plain-list">
            {weaknesses.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </div>
      <ol className="action-list">
        {recommendations.map((item, index) => (
          <li key={item}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <p>{item}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}
