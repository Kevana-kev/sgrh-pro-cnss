#!/bin/sh
set -e

cd /app

if [ -z "$APP_KEY" ]; then
  echo "ERROR: APP_KEY is missing. Set it in Railway Variables."
  exit 1
fi

php artisan config:clear || true
php artisan migrate --force
php artisan storage:link 2>/dev/null || true

if [ "$SEED_ON_BOOT" = "true" ]; then
  php artisan db:seed --force || true
fi

exec php artisan serve --host=0.0.0.0 --port="${PORT:-8000}"
