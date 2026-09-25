# Build depuis la racine du repo GitHub (Railway n'a pas besoin de Root Directory)
FROM php:8.4-cli-bookworm

ENV COMPOSER_ALLOW_SUPERUSER=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git unzip libzip-dev libicu-dev libpng-dev libonig-dev \
    && docker-php-ext-install pdo_mysql bcmath zip intl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /app

COPY RH_CNSS/sgrh-pro/composer.json RH_CNSS/sgrh-pro/composer.lock ./
RUN composer install --no-dev --optimize-autoloader --no-interaction --no-scripts

COPY RH_CNSS/sgrh-pro/ ./
RUN composer dump-autoload --optimize \
    && mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views storage/logs bootstrap/cache \
    && chmod -R 775 storage bootstrap/cache \
    && php artisan package:discover --ansi || true

COPY RH_CNSS/sgrh-pro/docker/railway-start.sh /usr/local/bin/railway-start.sh
RUN sed -i 's/\r$//' /usr/local/bin/railway-start.sh && chmod +x /usr/local/bin/railway-start.sh

EXPOSE 8000
CMD ["/usr/local/bin/railway-start.sh"]
