#!/usr/bin/env bash
# deploy_remote.sh <owner/repo> <branch> <target_dir>
set -euo pipefail
REPO="$1"
BRANCH="${2:-main}"
TARGET_DIR="${3:-/home/deploy/app}"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"
if [ ! -d .git ]; then
  git clone "https://github.com/${REPO}.git" .
else
  git fetch origin "$BRANCH" --depth=1
fi
git checkout -f "$BRANCH"
git reset --hard "origin/${BRANCH}"
if command -v docker >/dev/null 2>&1 && command -v docker-compose >/dev/null 2>&1; then
  docker-compose pull || true
  docker-compose up -d --build --remove-orphans
elif docker compose version >/dev/null 2>&1; then
  docker compose pull || true
  docker compose up -d --build --remove-orphans
else
  echo "Docker compose not available. Exiting."
  exit 2
fi
docker image prune -f || true
echo "Deployed."
