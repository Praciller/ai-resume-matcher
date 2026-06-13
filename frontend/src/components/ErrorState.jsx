import { AlertCircle } from "lucide-react";

export default function ErrorState({ message }) {
  if (!message) {
    return null;
  }
  return (
    <div className="error-state" role="alert">
      <AlertCircle aria-hidden="true" />
      <div>
        <strong>Analysis stopped</strong>
        <p>{message}</p>
      </div>
    </div>
  );
}
