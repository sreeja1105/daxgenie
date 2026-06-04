from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import os
import time
from threading import Lock
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

# Gemini API key (for model calls)
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MODEL_NAME = 'gemini-2.5-flash'

# Rate limiter storage (in-memory, demo only)
_rate_lock = Lock()
_rate_store: dict = {}

# Rate limit per minute (default: 60 requests/min per API key)
DEFAULT_RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))


# Prompt templates (kept same style as the Streamlit app)
GENERATE_DAX_PROMPT = """You are DAXGenie, an expert Power BI DAX assistant with deep knowledge of DAX patterns, time intelligence, calculations, and best practices.

A Power BI analyst needs help with the following calculation:

"{user_request}"

Provide your response in EXACTLY this format (use markdown):

### DAX Formula
```dax
[Working DAX formula here]
```

### How It Works
[Plain English explanation in 2-4 sentences. Avoid jargon. Focus on what each part of the formula does.]

### Things to Watch Out For
- [Common pitfall 1]
- [Common pitfall 2]
- [Optional: performance or accuracy tip]

### Example Usage
[Briefly describe how a Power BI user would use this measure in a report — what visual would it appear in, what would it show]

Important rules:
- Use modern DAX syntax (DAX 2.0+)
- Include comments inside complex formulas using -- 
- If the request is ambiguous, make reasonable assumptions and state them clearly
- Use Calendar table conventions (Calendar[Date], DimDate) for time intelligence
- Output ONLY the sections above. Do not add extra commentary."""

EXPLAIN_DAX_PROMPT = """You are DAXGenie, an expert Power BI DAX assistant who excels at making complex formulas understandable.

A Power BI analyst wants to understand the following DAX formula:

```dax
{dax_formula}
```

Provide your response in EXACTLY this format (use markdown):

### What This Formula Does
[1-2 sentence high-level summary in plain English. What business question does this answer?]

### Step-by-Step Breakdown
[Walk through the formula piece by piece. For each function or operation:
- Name the function
- Explain what it does in plain English
- Note any important behavior]

### Result
[What does this formula return? A number, a percentage, a date? What context does it depend on?]

### Common Use Cases
[2-3 bullet points of real-world scenarios where this formula would be used]

Important rules:
- Be specific, not vague
- Assume the reader knows Power BI basics but not advanced DAX
- If you notice anything unusual or potential issues with the formula, flag it
- Output ONLY the sections above."""


def call_gemini(prompt: str) -> str:
    """Wrapper to call the configured Gemini model. Returns text or raises."""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return response.text or ""
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini: {e}")


def _verify_api_key(x_api_key: str = Header(None)) -> str:
    """Dependency to validate API key (if configured) and apply simple rate limiting.

    - If `SERVICE_API_KEY` is set in env, requests must include that key via `X-API-KEY` header.
    - Applies an in-memory per-key rate limit (requests per minute).
    """
    service_key = os.getenv("SERVICE_API_KEY")
    # Validate key if configured
    if service_key:
        if not x_api_key or x_api_key != service_key:
            raise HTTPException(status_code=401, detail="Invalid or missing X-API-KEY")
    # Use provided key or "anonymous" when none configured
    key = x_api_key or "anonymous"

    now = time.time()
    window = 60.0
    limit = int(os.getenv("RATE_LIMIT_PER_MIN", str(DEFAULT_RATE_LIMIT)))

    with _rate_lock:
        entry = _rate_store.get(key)
        if not entry or now > entry[0]:
            # reset window: store (reset_time, count)
            _rate_store[key] = (now + window, 1)
        else:
            reset_time, count = entry
            count += 1
            _rate_store[key] = (reset_time, count)
            if count > limit:
                retry_after = int(reset_time - now)
                raise HTTPException(status_code=429, detail=f"Rate limit exceeded. Retry after {retry_after}s")

    return key


class TextIn(BaseModel):
    text: str


app = FastAPI(title="DAXGenie API")


@app.post("/generate")
async def generate_dax(payload: TextIn, key: str = Depends(_verify_api_key)):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="`text` is required")
    prompt = GENERATE_DAX_PROMPT.format(user_request=payload.text)
    try:
        result = call_gemini(prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain")
async def explain_dax(payload: TextIn, key: str = Depends(_verify_api_key)):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="`text` is required")
    prompt = EXPLAIN_DAX_PROMPT.format(dax_formula=payload.text)
    try:
        result = call_gemini(prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
