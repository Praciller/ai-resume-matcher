import InterviewPrep from "./InterviewPrep";
import LearningPlan from "./LearningPlan";
import MatchScoreCard from "./MatchScoreCard";
import Recommendations from "./Recommendations";
import SkillGapList from "./SkillGapList";

export default function AnalysisReport({ result }) {
  return (
    <div className="report" aria-live="polite">
      <MatchScoreCard score={result.match_score} summary={result.summary} />
      <SkillGapList
        matchedSkills={result.matched_skills}
        missingSkills={result.missing_skills}
      />
      <Recommendations
        strengths={result.strengths}
        weaknesses={result.weaknesses}
        recommendations={result.recommendations}
      />
      <LearningPlan items={result.learning_plan} />
      <InterviewPrep questions={result.interview_questions} />
      {(result.risk_flags.length > 0 || result.warnings.length > 0) && (
        <section className="report-section report-notes" aria-labelledby="notes-title">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Review notes</p>
              <h2 id="notes-title">Warnings</h2>
            </div>
          </div>
          <ul className="plain-list">
            {[...result.risk_flags, ...result.warnings].map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>
      )}
      <footer className="report-meta">
        <span>Provider: {result.provider_used}</span>
        <span>Model: {result.model_used}</span>
        <span>ID: {result.analysis_id}</span>
        {result.cached && <span>Cached result</span>}
      </footer>
    </div>
  );
}
