export default function JobDescriptionInput({
  value,
  maxChars,
  onChange,
  disabled,
}) {
  const isShort = value.trim().length > 0 && value.trim().length < 20;
  const isLong = value.length > maxChars;

  return (
    <div className="field-group">
      <div className="field-heading">
        <label htmlFor="job-description">Job description</label>
        <span className={isLong ? "count-warning" : ""}>
          {value.length.toLocaleString()} / {maxChars.toLocaleString()}
        </span>
      </div>
      <textarea
        id="job-description"
        value={value}
        onChange={onChange}
        disabled={disabled}
        rows={12}
        placeholder="Paste responsibilities, required skills, and preferred experience."
        aria-describedby="job-description-help"
      />
      <p id="job-description-help" className="field-help">
        {isShort
          ? "Add more detail before analysis."
          : isLong
            ? "The API will analyze the first configured character limit."
            : "Include the full role context for a more useful comparison."}
      </p>
    </div>
  );
}
