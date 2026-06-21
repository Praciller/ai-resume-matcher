"""Fail when Git tracks secrets, private resumes, or generated artifacts."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PARTS = {"uploads", "temp_uploads", "extracted_text", "node_modules"}
FORBIDDEN_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".pem", ".key", ".pdf"}
PRIVATE_DATA_PREFIXES = {("backend", "dataset", "resumes")}
MAX_TRACKED_BYTES = 5 * 1024 * 1024
SECRET_ASSIGNMENT = re.compile(
    r"(?im)^(?:[A-Z0-9_]*(?:API_KEY|SECRET|TOKEN|PASSWORD))[ \t]*=[ \t]*([^\s#]+)"
)
UNSAFE_CLAIMS = (
    "guaranteed " + "best candidate",
    "production " + "hiring accuracy",
)


def tracked_files() -> list[Path]:
    output = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return [ROOT / item.decode() for item in output.split(b"\0") if item]


def violations(paths: list[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        relative = path.relative_to(ROOT)
        relative_parts = tuple(part.casefold() for part in relative.parts)
        parts = set(relative_parts)
        if parts & FORBIDDEN_PARTS or path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            failures.append(f"unsafe tracked artifact: {relative.as_posix()}")
            continue
        if any(relative_parts[: len(prefix)] == prefix for prefix in PRIVATE_DATA_PREFIXES):
            failures.append(f"unsafe tracked artifact: {relative.as_posix()}")
            continue
        if path.stat().st_size > MAX_TRACKED_BYTES:
            failures.append(f"oversized tracked artifact: {relative.as_posix()}")
            continue
        if path.name == ".env":
            failures.append("tracked environment file: .env")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if SECRET_ASSIGNMENT.search(text):
            failures.append(f"possible credential assignment: {relative.as_posix()}")
        lowered = text.casefold()
        for claim in UNSAFE_CLAIMS:
            if claim in lowered:
                failures.append(f"unsafe hiring claim in {relative.as_posix()}: {claim}")
    return failures


def main() -> int:
    failures = violations(tracked_files())
    if failures:
        print("\n".join(failures))
        return 1
    print("Repository guardrails passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
