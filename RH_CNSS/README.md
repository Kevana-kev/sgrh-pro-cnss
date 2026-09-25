# RH_CNSS — SGRH Pro

## Application active (Hostinger / MySQL)

Voir **`sgrh-pro/README.md`** — Laravel 11, 8 modules mémoire.

```bash
cd sgrh-pro
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate --seed
php artisan serve
```

## Biométrie

`fingerprint-service/` — bridge ZK-9500 (localhost:5002)

## Legacy

`legacy/flask-app/` — ancienne app Flask (archivée)
