import { ArrowRight } from "lucide-react";

import { Button } from "./ui/button";

export default function AnalyzeButton({ disabled, isLoading }) {
  return (
    <Button
      type="submit"
      size="lg"
      disabled={disabled}
      className="w-full min-h-11 justify-between"
    >
      <span>{isLoading ? "Analyzing evidence" : "Analyze resume"}</span>
      <ArrowRight aria-hidden="true" className="h-4 w-4" />
    </Button>
  );
}
