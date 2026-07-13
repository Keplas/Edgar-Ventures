#!/usr/bin/env bash
set -o errexit
echo "==> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "==> Collecting static files..."
python manage.py collectstatic --noinput
echo "==> Running migrations..."
python manage.py migrate --noinput
echo "==> Seeding products..."
python manage.py seed_agri_products
echo "==> Creating admin user..."
python manage.py ensure_admin
echo "==> Uploading images to Cloudinary..."
python manage.py upload_images_to_cloudinary || echo "Skipped (credentials not set)"
echo "==> Build complete."
