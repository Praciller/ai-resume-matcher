import { Check, Minus } from "lucide-react";

function SkillList({ title, items, type }) {
  const Icon = type === "matched" ? Check : Minus;
  return (
    <div>
      <h3>{title}</h3>
      {items.length ? (
        <ul className="tag-list">
          {items.map((item) => (
            <li key={item} className={type}>
              <Icon aria-hidden="true" />
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="empty-copy">No items returned.</p>
      )}
    </div>
  );
}

export default function SkillGapList({ matchedSkills, missingSkills }) {
  return (
    <section className="report-section" aria-labelledby="skills-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Evidence map</p>
          <h2 id="skills-title">Skills</h2>
        </div>
      </div>
      <div className="two-column-list">
        <SkillList title="Matched" items={matchedSkills} type="matched" />
        <SkillList title="Missing or unclear" items={missingSkills} type="missing" />
      </div>
    </section>
  );
}
