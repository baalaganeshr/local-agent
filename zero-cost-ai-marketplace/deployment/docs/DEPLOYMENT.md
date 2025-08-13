# Deployment Guide

## Docker Compose

1. Build and run
```bash
docker compose up --build -d
```

2. Services
- Frontend: http://localhost:8080
- Backend:  http://localhost:8001/docs

## Production Notes
- Place a reverse proxy (e.g., Nginx, Traefik) in front of backend and frontend.
- Configure HTTPS at the proxy.
- Set CORS_ALLOW_ORIGINS to your actual domains.
- Move from SQLite to Postgres/MySQL when needed.
