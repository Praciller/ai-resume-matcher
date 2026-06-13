export default function InterviewPrep({ questions }) {
  return (
    <section className="report-section" aria-labelledby="interview-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Interview prep</p>
          <h2 id="interview-title">Questions to rehearse</h2>
        </div>
      </div>
      <ol className="question-list">
        {questions.map((question, index) => (
          <li key={question}>
            <span>{index + 1}</span>
            <p>{question}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}
