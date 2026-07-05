"""
Automatically creates a superuser during build if none exists.
Reads credentials from environment variables:
  ADMIN_USERNAME  (default: admin)
  ADMIN_PASSWORD  (default: EGV@admin2026)
  ADMIN_EMAIL     (default: admin@egv.com)
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create superuser from env vars if none exists'

    def handle(self, *args, **options):
        User     = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'EGV@admin2026')
        email    = os.environ.get('ADMIN_EMAIL',    'admin@egv.com')

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(f'  Superuser already exists — skipping.')
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(
            f'  Superuser "{username}" created successfully.'
        ))
