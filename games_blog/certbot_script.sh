#!/usr/bin/env bash

if [ -f .env ]; then
    export $(cat .env | xargs)
fi

certbot certonly --webroot --webroot-path=/var/www/certbot/ --email "$CERTBOT_EMAIL" --agree-tos --no-eff-email -d "$DOMAIN_NAME" -d "$WWW_DOMAIN_NAME"