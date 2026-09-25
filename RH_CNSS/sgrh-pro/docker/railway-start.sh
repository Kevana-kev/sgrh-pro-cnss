#!/bin/sh
set -e

cd /app

if [ -z "$APP_KEY" ]; then
  echo "ERROR: APP_KEY is missing. Generate one with: php artisan key:generate --show"
  exit 1
fi

php artisan config:clear
php artisan migrate --force
php artisan storage:link 2>/dev/null || true

# Seed only once (set SEED_ON_BOOT=true in Railway Variables for first deploy)
if [ "$SEED_ON_BOOT" = "true" ]; then
  php artisan db:seed --force
fi

exec php artisan serve --host=0.0.0.0 --port="${PORT:-8000}"
