# Deployment Guide

This guide covers deploying DAXGenie to a cloud platform for a public demo.

## Prerequisites

- Git repo pushed to GitHub
- Docker image builds successfully (`docker build -t daxgenie .`)
- `.env` file configured with `GEMINI_API_KEY` and optional `SERVICE_API_KEY`

## Option 1: Render (Recommended for beginners)

**Cost:** Free tier available (with limitations)

1. Go to https://render.com and sign up with GitHub.
2. Click "New+" → "Web Service"
3. Select your `daxgenie` GitHub repo
4. Configure:
   - **Name:** daxgenie
   - **Environment:** Docker
   - **Plan:** Free (or Starter if you want better uptime)
5. Add environment variables in Render dashboard:
   - `GEMINI_API_KEY=<your-key>`
   - `SERVICE_API_KEY=<your-key>` (optional)
   - `RATE_LIMIT_PER_MIN=60`
6. Click "Create Web Service"
7. Render builds and deploys. Your app will be live at `https://daxgenie-<random>.onrender.com`

**Note:** Free tier spins down after 15 minutes of inactivity. Add a link in your README to keep it warm.

## Option 2: Railway (Good free tier)

**Cost:** Free tier with $5/month credits

1. Go to https://railway.app and sign up.
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo
4. Railway auto-detects Docker and deploys.
5. Go to "Variables" and add:
   - `GEMINI_API_KEY`
   - `SERVICE_API_KEY` (optional)
   - `RATE_LIMIT_PER_MIN=60`
6. Your app will be live at `https://<project-name>.up.railway.app`

## Option 3: Fly.io (Fast, good free tier)

**Cost:** Free tier with 3 shared-cpu-1x Fly Apps

1. Install `flyctl`: https://fly.io/docs/hands-on/install-flyctl/
2. In your repo:
   ```bash
   flyctl auth login
   flyctl launch
   ```
3. Follow the wizard. Keep the Dockerfile option.
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
