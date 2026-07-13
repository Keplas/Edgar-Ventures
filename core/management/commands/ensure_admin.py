import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create superuser from env vars if none exists'
    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('  Superuser already exists.'); return
        User.objects.create_superuser(
            username=os.environ.get('ADMIN_USERNAME','admin'),
            email=os.environ.get('ADMIN_EMAIL','admin@egv.com'),
            password=os.environ.get('ADMIN_PASSWORD','EGV@admin2026'),
        )
        self.stdout.write(self.style.SUCCESS('  Superuser created.'))
