# Model Routing

## Order

Default:

```text
9arm qwen3.6-35b-a3b
  -> Gemini gemini-2.5-flash-lite
  -> Gemini gemini-2.5-flash
  -> Groq openai/gpt-oss-20b
  -> Cerebras gpt-oss-120b
```

Change order with `AI_PROVIDER_ORDER`.

## Acceptance Gate

Each response must:

1. Parse as one JSON object.
2. Validate against `AnalysisResult`.
3. Keep score in `0..100`.
4. Include every required array.
5. Include a meaningful summary and actionable recommendations.
6. Deduplicate string lists case-insensitively.

Invalid or low-quality output moves to the next model. If every configured provider fails, the API returns a controlled `503`.

## Structured Output

- Gemini uses `responseMimeType=application/json` and `responseJsonSchema`.
- Groq and Cerebras use OpenAI-compatible `response_format.type=json_schema`.
- 9arm receives the schema in the prompt, then passes through the same Pydantic validation gate.

Provider schema generation removes unsupported annotation keywords while retaining required fields and `additionalProperties: false`.

## Privacy

Resume and JD text are sent to the first provider that successfully returns accepted output. Configure only providers approved for the intended data-handling policy.
