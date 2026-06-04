# daxgenie
AI-powered DAX formula assistant for Power BI

## Overview

DAXGenie is an open-source Streamlit app that helps Power BI analysts:

- Generate DAX formulas from plain-English descriptions
- Explain and break down existing DAX formulas

It integrates with an LLM backend using the Google Gemini Developer API via the official `google-genai` SDK in `app.py` and is designed as a small, shareable portfolio piece.

## Features

- Natural language → DAX generation
- Formula explanation and step-by-step breakdown
- Streamlit UI for quick demos

## Demo

Preview the app (placeholder demo):

![DAXGenie demo](assets/demo.gif)

Replace `assets/demo.gif` with a short screen recording (MP4/GIF) showing the Generate and Explain flows.

How to record a short demo:

- Keep the demo under 20 seconds.
- Show entering a prompt, clicking "Generate DAX", and the produced formula.
- Then paste a DAX formula and click "Explain DAX" to show the explanation.
- Optimize for clarity: highlight the input and the resulting formula in the video/GIF.

## Run locally

1. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

The app now uses the official `google-genai` package for Gemini API access.

3. (Optional) Validate the setup:

```bash
python validate_setup.py
```

4. Run the app:

```bash
streamlit run app.py
```

Open http://localhost:8501 to view the demo.

When you enable the local API backend in the Streamlit sidebar, DAXGenie will show the FastAPI backend health status and call the backend at `API_BACKEND_URL`.

## Example prompts

Use the example prompts in the Streamlit UI (select a prompt and click "Use example prompt") or paste your own. Example natural-language prompts:

- "Calculate year-over-year sales growth percentage for the current selection."
- "Calculate total sales for the last 30 days ending at the selected date"
- "Calculate a 3-month rolling average of Sales[Amount]"

Example DAX formulas for the Explain mode:

- `SUM(Sales[Amount])`
- `CALCULATE(SUM(Sales[Amount]), DATESYTD(Calendar[Date]))`
- `CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date]))`


## Docker

Build and run the container:

```bash
docker build -t daxgenie:latest .
docker run -p 8501:8501 --env-file .env daxgenie:latest
```

## Render deployment

A `render.yaml` file is included for Render deployments. It configures both the `daxgenie-api` and `daxgenie-web` services, with the web app pointing to the API backend at `http://daxgenie-api:8000`.

## Other deployment options

- `railway.json` is included to help Railway detect the Dockerfile and deploy the app.
- `fly.toml` is included to help Fly.io deploy the app from the same repository.

> Note: Railway and Fly use the same Dockerfile for the app. Set `GEMINI_API_KEY` and optional `SERVICE_API_KEY` in the platform environment settings. If you deploy the FastAPI backend separately, update `API_BACKEND_URL` to the backend's public URL.

Railway commands:

```bash
npm install -g @railway/cli
railway login
railway link
railway up
```

Fly.io commands:

```bash
curl -L https://fly.io/install.sh | sh
flyctl auth login
flyctl launch --dockerfile Dockerfile
flyctl deploy
```

## Docker Compose (full stack)

To run the Streamlit UI and the FastAPI backend together locally using docker-compose:

```bash
cp .env.example .env
# set GEMINI_API_KEY in .env
docker compose up --build
```

- Streamlit UI: http://localhost:8501
- FastAPI: http://localhost:8000/docs (interactive API docs)
- FastAPI health: http://localhost:8000/healthz

## Live Demo

After deploying DAXGenie to a public host, update this section with the live URL so viewers and reviewers can access the running app.

Example:

[Try DAXGenie online](https://daxgenie-example.onrender.com)

If you deploy the backend separately, make sure `API_BACKEND_URL` points to the deployed FastAPI service.

## Deploy to the cloud

See [DEPLOY.md](DEPLOY.md) for step-by-step deployment guides to Render, Railway, or Fly.io.


## API Authentication & Rate Limiting

The FastAPI backend supports optional API key authentication and per-key rate limiting:

- **API Key**: Set `SERVICE_API_KEY` in `.env` to require the `X-API-KEY` header on all requests.
- **Rate Limit**: Set `RATE_LIMIT_PER_MIN` (default: 60) to limit requests per key per minute.

Example request with auth:

```bash
curl -X POST http://localhost:8000/generate \
  -H "X-API-KEY: your_service_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"text": "Calculate YoY growth"}'
```

If `SERVICE_API_KEY` is not set, the API is open (no auth required). The rate limiter still applies to limit abuse.

The FastAPI app also exposes a lightweight health endpoint at `GET /healthz` for container health checks or local status probes.

## CI

A basic GitHub Actions workflow is included at `.github/workflows/ci.yml` to check syntax and run tests (including rate limit tests).

## Environment

Required and optional environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `SERVICE_API_KEY`: Optional API key for protecting the FastAPI endpoints (leave blank for open API)
- `RATE_LIMIT_PER_MIN`: Maximum requests per key per minute (default: 60)
- `API_BACKEND_URL`: URL of the FastAPI backend (only for local Streamlit UI; default: `http://localhost:8000`)

See `.env.example` for a template.

## Contributing

Contributions welcome — open issues or PRs. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Validation

Before deploying, run:

```bash
python validate_setup.py
```

This checks dependencies, syntax, and runs tests.

## License

MIT

