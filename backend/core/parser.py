"""PDF and text input validation."""

from __future__ import annotations

import io
import re
from dataclasses import dataclass

from pypdf import PdfReader


class InputValidationError(ValueError):
    """User-correctable input error."""


@dataclass(frozen=True)
class ParsedText:
    text: str
    truncated: bool


def validate_pdf_upload(
    filename: str | None,
    content_type: str | None,
    file_bytes: bytes,
    max_bytes: int,
) -> None:
    if not filename or not filename.lower().endswith(".pdf"):
        raise InputValidationError("Resume must use the .pdf file extension.")
    if content_type != "application/pdf":
        raise InputValidationError("Resume MIME type must be application/pdf.")
    if not file_bytes:
        raise InputValidationError("Resume PDF is empty.")
    if len(file_bytes) > max_bytes:
        max_mb = max_bytes // (1024 * 1024)
        raise InputValidationError(
            f"Resume PDF exceeds the {max_mb} MB file-size limit."
        )
    if not file_bytes.startswith(b"%PDF-"):
        raise InputValidationError("Resume file does not contain a valid PDF header.")


def normalize_text(value: str) -> str:
    lines = [" ".join(line.split()) for line in value.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def limit_text(value: str, max_chars: int) -> ParsedText:
    normalized = normalize_text(value)
    return ParsedText(
        text=normalized[:max_chars],
        truncated=len(normalized) > max_chars,
    )


def validate_job_description(value: str, max_chars: int) -> ParsedText:
    limited = limit_text(value, max_chars)
    if len(limited.text) < 20:
        raise InputValidationError(
            "Job description must contain at least 20 characters."
        )
    return limited


def parse_pdf_to_text(file_bytes: bytes, max_chars: int) -> ParsedText:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
    except Exception as exc:
        raise InputValidationError(
            "Resume PDF is corrupted or cannot be opened."
        ) from exc

    if not reader.pages:
        raise InputValidationError("Resume PDF contains no pages.")

    page_text: list[str] = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            page_text.append(text)

    limited = limit_text("\n".join(page_text), max_chars)
    if not re.search(r"[A-Za-z0-9]", limited.text):
        raise InputValidationError(
            "This PDF appears to be scanned/image-only. OCR is not supported in v1."
        )
    return limited
