# Deployment Guide

This guide covers deploying DAXGenie to a cloud platform for a public demo.

## Prerequisites

- Git repo pushed to GitHub
- Docker image builds successfully (`docker build -t daxgenie .`)
- `.env` file configured with `GEMINI_API_KEY` and optional `SERVICE_API_KEY`
- `requirements.txt` installs the official `google-genai` SDK for Gemini API access

## Deployment checklist

- [ ] Confirm `requirements.txt` includes `google-genai`
- [ ] Copy `.env.example` to `.env` and set `GEMINI_API_KEY`
- [ ] Optionally set `SERVICE_API_KEY` for secure API access
- [ ] Build the Docker image locally: `docker build -t daxgenie .`
- [ ] Verify the app runs locally: `streamlit run app.py`
- [ ] Push changes to GitHub before cloud deployment

## Option 1: Render (Recommended for beginners)

**Cost:** Free tier available (with limitations)

Render can deploy both the UI and API services together using the included `render.yaml` configuration.

1. Go to https://render.com and sign up with GitHub.
2. Click "New+" → "Web Service"
3. Connect your `daxgenie` GitHub repo.
4. In the Render dashboard, choose "From `render.yaml`" when configuring the service.
5. Add the following environment variables in Render:
   - `GEMINI_API_KEY=<your-key>`
   - `SERVICE_API_KEY=<your-key>` (optional)
   - `RATE_LIMIT_PER_MIN=60`
6. Deploy the two services defined in `render.yaml`.
7. Your Streamlit app will be live at the Render URL shown for the `daxgenie-web` service.

> Note: Render uses service names for internal networking. The Streamlit UI is configured to use `http://daxgenie-api:8000` for the API backend in `render.yaml`.

**Note:** Free tier spins down after 15 minutes of inactivity. Add a link in your README to keep it warm.

## Option 2: Railway (Good free tier)

**Cost:** Free tier with $5/month credits

Railway can deploy the app directly from this repo using the included `railway.json` config.

1. Go to https://railway.app and sign up.
2. Click "New Project" → "Deploy from GitHub"
3. Select your `daxgenie` repo.
4. Railway should detect the Dockerfile automatically.
5. Add project variables:
   - `GEMINI_API_KEY`
   - `SERVICE_API_KEY` (optional)
   - `RATE_LIMIT_PER_MIN=60`
6. Deploy the project.
7. Your app will be live at `https://<project-name>.up.railway.app`

Railway commands:

```bash
# Install the Railway CLI if you want local deployment control
npm install -g @railway/cli

# Log in
railway login

# Link your project to the repo
railway link

# Deploy your app
railway up
```

## Option 3: Fly.io (Fast, good free tier)

**Cost:** Free tier with 3 shared-cpu-1x Fly Apps

A `fly.toml` file is included for Fly.io deployments.

1. Install `flyctl`: https://fly.io/docs/hands-on/install-flyctl/
2. In your repo:
   ```bash
   flyctl auth login
   flyctl launch
   ```
3. When prompted, choose the Dockerfile option.
4. Set secrets:
   ```bash
   flyctl secrets set GEMINI_API_KEY=<your-key>
   flyctl secrets set SERVICE_API_KEY=<your-key>
   flyctl secrets set RATE_LIMIT_PER_MIN=60
   ```
5. Deploy:
   ```bash
   flyctl deploy
   ```
6. Your app will be live at `https://<app-name>.fly.dev`

Fly commands:

```bash
# Install flyctl if needed
curl -L https://fly.io/install.sh | sh

# Authenticate
flyctl auth login

# Initialize the project (choose Dockerfile)
flyctl launch --dockerfile Dockerfile

# Deploy the app
flyctl deploy
```

**Note:** If you want to deploy the FastAPI backend separately on Fly, create a second Fly app and set `API_BACKEND_URL` in the Streamlit app to the deployed API URL.

## Update README with Live Demo Link

Once deployed, update your `README.md`:

```markdown
## Live Demo

[Try DAXGenie online](https://daxgenie-<your-id>.onrender.com) (powered by [Render](https://render.com))
```

## Monitoring & Logs

- **Render:** Dashboard → Logs tab
- **Railway:** Project → Logs
- **Fly.io:** `flyctl logs`

## Cost Considerations

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| Render   | Yes (limited uptime) | Simple demos, learning |
| Railway  | Yes ($5/mo credits) | Small projects |
| Fly.io   | Yes (3 apps) | Production-like performance |

For a portfolio project, **Render Free** or **Railway** are good starting points.
