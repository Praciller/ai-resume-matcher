import { FileText, Upload } from "lucide-react";

function formatFileSize(bytes) {
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export default function ResumeUpload({
  file,
  maxFileMb,
  onChange,
  error,
  disabled,
}) {
  return (
    <div className="field-group">
      <div className="field-heading">
        <label htmlFor="resume-file">Resume PDF</label>
        <span>Max {maxFileMb} MB</span>
      </div>
      <label className={`upload-control ${error ? "field-error" : ""}`}>
        <Upload aria-hidden="true" />
        <span>{file ? "Replace PDF" : "Choose PDF"}</span>
        <input
          id="resume-file"
          type="file"
          accept=".pdf,application/pdf"
          onChange={onChange}
          disabled={disabled}
          aria-describedby="resume-help resume-error"
        />
      </label>
      <p id="resume-help" className="field-help">
        Text-based PDFs only. Scanned files need OCR and are not supported.
      </p>
      {file && (
        <div className="file-summary">
          <FileText aria-hidden="true" />
          <span>{file.name}</span>
          <span>{formatFileSize(file.size)}</span>
        </div>
      )}
      {error && (
        <p id="resume-error" className="field-message" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
