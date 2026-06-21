from __future__ import annotations

import pytest

from backend.core.parser import (
    InputValidationError,
    parse_pdf_to_text,
    validate_job_description,
    validate_pdf_upload,
)
from backend.tests.pdf_factory import make_text_pdf


def test_pdf_validation_accepts_real_pdf() -> None:
    content = make_text_pdf()
    validate_pdf_upload("resume.pdf", "application/pdf", content, 1_000_000)


@pytest.mark.parametrize(
    ("filename", "content_type", "content"),
    [
        ("resume.txt", "application/pdf", b"%PDF-invalid"),
        ("resume.pdf", "text/plain", b"%PDF-invalid"),
        ("resume.pdf", "application/pdf", b"not-a-pdf"),
    ],
)
def test_pdf_validation_rejects_invalid_inputs(
    filename: str, content_type: str, content: bytes
) -> None:
    with pytest.raises(InputValidationError):
        validate_pdf_upload(filename, content_type, content, 1_000_000)


def test_pdf_validation_rejects_oversized_file() -> None:
    with pytest.raises(InputValidationError, match="file-size limit"):
        validate_pdf_upload(
            "resume.pdf",
            "application/pdf",
            b"%PDF-" + b"x" * 100,
            20,
        )


def test_pdf_parser_extracts_and_limits_text() -> None:
    parsed = parse_pdf_to_text(make_text_pdf("Python React FastAPI"), 12)
    assert parsed.text == "Python React"
    assert parsed.truncated is True


def test_image_only_pdf_returns_controlled_error() -> None:
    with pytest.raises(InputValidationError, match="image-only"):
        parse_pdf_to_text(make_text_pdf("   "), 20_000)


def test_job_description_validation_handles_long_input() -> None:
    parsed = validate_job_description("Senior engineer " * 100, 80)
    assert len(parsed.text) == 80
    assert parsed.truncated is True


def test_job_description_rejects_empty_input() -> None:
    with pytest.raises(InputValidationError, match="20 characters"):
        validate_job_description("short", 20_000)
