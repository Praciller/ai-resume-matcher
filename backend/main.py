"""FastAPI application for resume and job-description analysis."""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.core.analysis import (
    AIAnalyzer,
    AnalysisUnavailableError,
    ProviderResult,
    build_mock_analysis,
    make_analysis_id,
    sample_analysis,
    to_response,
)
from backend.core.cache import AnalysisCache
from backend.core.config import get_settings
from backend.core.parser import (
    InputValidationError,
    parse_pdf_to_text,
    validate_job_description,
    validate_pdf_upload,
)
from backend.core.schema import AnalysisResponse, HealthResponse


logger = logging.getLogger(__name__)
settings = get_settings()
cache = AnalysisCache()
analyzer = AIAnalyzer(settings)

app = FastAPI(
    title="AI Resume Matcher API",
    description="Validated resume and job-description matching API.",
    version="2.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.frontend_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"name": "AI Resume Matcher API", "status": "ready"}


@app.get("/api/health", response_model=HealthResponse)
@app.get("/health", response_model=HealthResponse, include_in_schema=False)
def health() -> HealthResponse:
    providers = settings.configured_providers()
    mode = "mock" if settings.mock_ai_mode else ("live" if providers else "unconfigured")
    return HealthResponse(
        status="healthy",
        mode=mode,
        configured_providers=providers,
        primary_provider=providers[0] if providers else None,
        max_resume_file_mb=settings.max_resume_file_mb,
        max_resume_chars=settings.max_resume_chars,
        max_jd_chars=settings.max_jd_chars,
    )


@app.post("/api/mock-analyze", response_model=AnalysisResponse)
def mock_analyze() -> AnalysisResponse:
    result = ProviderResult(sample_analysis(), "mock", "deterministic-sample-v1")
    return to_response(
        result=result,
        analysis_id="sample-demo",
        cached=False,
        warnings=["Sample data only. No resume was uploaded."],
    )


@app.post("/api/analyze", response_model=AnalysisResponse)
@app.post("/api/screen-resume", response_model=AnalysisResponse, include_in_schema=False)
async def analyze(
    resume_file: Annotated[UploadFile, File(description="PDF resume")],
    job_description: Annotated[str | None, Form()] = None,
    jd_text: Annotated[str | None, Form()] = None,
) -> AnalysisResponse:
    try:
        submitted_jd = job_description if job_description is not None else jd_text
        if submitted_jd is None:
            raise InputValidationError("Job description is required.")
        file_bytes = await resume_file.read(settings.max_resume_file_bytes + 1)
        validate_pdf_upload(
            filename=resume_file.filename,
            content_type=resume_file.content_type,
            file_bytes=file_bytes,
            max_bytes=settings.max_resume_file_bytes,
        )
        parsed_resume = parse_pdf_to_text(file_bytes, settings.max_resume_chars)
        parsed_jd = validate_job_description(submitted_jd, settings.max_jd_chars)
    except InputValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    warnings: list[str] = []
    if parsed_resume.truncated:
        warnings.append(
            f"Resume text was limited to {settings.max_resume_chars} characters."
        )
    if parsed_jd.truncated:
        warnings.append(
            f"Job description was limited to {settings.max_jd_chars} characters."
        )

    analysis_id = make_analysis_id(parsed_resume.text, parsed_jd.text)
    if settings.cache_enabled:
        cached = cache.get(analysis_id)
        if cached:
            return to_response(
                ProviderResult(cached.result, cached.provider, cached.model),
                analysis_id=analysis_id,
                cached=True,
                warnings=warnings,
            )

    try:
        if settings.mock_ai_mode:
            provider_result = ProviderResult(
                build_mock_analysis(parsed_resume.text, parsed_jd.text),
                "mock",
                "deterministic-local-v1",
            )
        else:
            provider_result = analyzer.analyze(
                parsed_resume.text, parsed_jd.text
            )
    except AnalysisUnavailableError as exc:
        logger.warning("Analysis unavailable for id=%s", analysis_id)
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    if settings.cache_enabled:
        cache.set(
            key=analysis_id,
            result=provider_result.analysis,
            provider=provider_result.provider,
            model=provider_result.model,
            ttl_seconds=settings.cache_ttl_seconds,
        )

    return to_response(
        provider_result,
        analysis_id=analysis_id,
        cached=False,
        warnings=warnings,
    )
