#!/usr/bin/env bash
# ── Render build script ──────────────────────────────────────
set -o errexit

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Seeding agriculture products..."
python manage.py seed_agri_products

echo "==> Creating admin user..."
python manage.py ensure_admin

echo "==> Uploading product images to Cloudinary..."
python manage.py upload_images_to_cloudinary || echo "Cloudinary upload skipped (credentials not set)"

echo "==> Build complete."
