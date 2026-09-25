#!/usr/bin/env bash
set -euo pipefail

cd /app/RH_CNSS/sgrh-pro 2>/dev/null || cd RH_CNSS/sgrh-pro

if [ -z "${APP_KEY:-}" ]; then
  echo "ERROR: APP_KEY is missing. Set it in Railway Variables."
  exit 1
fi

php artisan config:clear || true
php artisan migrate --force

if [ "${SEED_ON_BOOT:-false}" = "true" ]; then
  php artisan db:seed --force || true
fi

php artisan storage:link 2>/dev/null || true

exec php artisan serve --host=0.0.0.0 --port="${PORT:-8000}"
