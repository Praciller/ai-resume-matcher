# Gemini Resume Analysis

Gemini is the first fallback after 9arm.

```env
GEMINI_RESUME_MODEL=gemini-2.5-flash-lite
GEMINI_RESUME_FALLBACK_MODEL=gemini-2.5-flash
GEMINI_TIMEOUT_SECONDS=30
GEMINI_MAX_RETRIES=1
```

## Request

The server sends normalized resume text, normalized JD text, scoring instructions, neutral-risk guidance, and the generated JSON Schema. Keys remain server-side.

## Fallback

Flash Lite runs first. When transport, JSON, schema, or quality validation fails, Flash runs once. The router then continues to Groq and Cerebras if configured.

## Validation

Gemini structured output reduces malformed responses but does not replace application validation. Pydantic remains the final contract before any result reaches the browser.

## Failure Behavior

Provider error details are not exposed. Users receive retry/sample guidance and can continue using deterministic sample mode.
