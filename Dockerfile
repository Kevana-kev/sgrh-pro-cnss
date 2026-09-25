# Build avec Root Directory Railway = RH_CNSS (contexte = RH_CNSS/)
FROM php:8.4-cli-bookworm

ENV COMPOSER_ALLOW_SUPERUSER=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git unzip libzip-dev libicu-dev libpng-dev libonig-dev \
    && docker-php-ext-install pdo_mysql bcmath zip intl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /app

# Contexte Docker = RH_CNSS/ (voir Root Directory Railway)
COPY sgrh-pro/ /app/

RUN composer install --no-dev --optimize-autoloader --no-interaction --no-scripts \
    && mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views storage/logs bootstrap/cache \
    && chmod -R 775 storage bootstrap/cache \
    && (test -f docker/railway-start.sh && cp docker/railway-start.sh /usr/local/bin/railway-start.sh || cp start.sh /usr/local/bin/railway-start.sh) \
    && sed -i 's/\r$//' /usr/local/bin/railway-start.sh \
    && chmod +x /usr/local/bin/railway-start.sh \
    && php artisan package:discover --ansi || true

EXPOSE 8000
CMD ["/usr/local/bin/railway-start.sh"]
