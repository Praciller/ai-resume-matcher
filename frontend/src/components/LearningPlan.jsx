export default function LearningPlan({ items }) {
  return (
    <section className="report-section" aria-labelledby="learning-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Skill development</p>
          <h2 id="learning-title">Learning plan</h2>
        </div>
      </div>
      {items.length ? (
        <div className="learning-list">
          {items.map((item) => (
            <article key={`${item.priority}-${item.skill}`}>
              <div className="learning-title">
                <h3>{item.skill}</h3>
                <span className={`priority ${item.priority}`}>{item.priority}</span>
              </div>
              <p>{item.reason}</p>
              <strong>{item.suggested_action}</strong>
            </article>
          ))}
        </div>
      ) : (
        <p className="empty-copy">No learning priorities returned.</p>
      )}
    </section>
  );
}
