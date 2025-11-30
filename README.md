# Portfolio - Production Ready

This repository contains a React frontend and FastAPI backend, containerized and ready for production.

## Quick start (local)
1. Copy examples:
```bash
cp app/backend/.env.example app/backend/.env
cp app/frontend/.env.example app/frontend/.env
```

2. Build and run everything:
```bash
docker-compose up --build
```

Frontend: http://localhost:3000  
Backend health: http://localhost:8001/api/health

## CI/CD
- `.github/workflows/build-and-publish.yml` builds Docker images and pushes to GHCR (set secret `GHCR_PAT`).
- `.github/workflows/gh-pages-deploy.yml` publishes frontend to GitHub Pages.
- `.github/workflows/deploy-to-vps.yml` deploys to a VPS over SSH (set SSH secrets).

