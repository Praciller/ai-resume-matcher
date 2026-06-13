import { FlaskConical } from "lucide-react";

import { Button } from "./ui/button";

export default function SampleDemoMode({ onRun, disabled }) {
  return (
    <div className="sample-mode">
      <FlaskConical aria-hidden="true" />
      <div>
        <strong>Review the report first</strong>
        <p>Run deterministic sample data without uploading a resume.</p>
      </div>
      <Button
        type="button"
        variant="outline"
        onClick={onRun}
        disabled={disabled}
      >
        Run sample
      </Button>
    </div>
  );
}
