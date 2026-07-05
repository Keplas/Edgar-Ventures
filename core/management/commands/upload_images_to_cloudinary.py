"""
Automatically downloads each product's image_url and uploads it to Cloudinary.
Run once after deployment:
  python manage.py upload_images_to_cloudinary

Requires environment variables:
  CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
"""
import os
import urllib.request
import tempfile
from django.core.management.base import BaseCommand
from core.models import Product


class Command(BaseCommand):
    help = 'Upload all product images from image_url to Cloudinary automatically'

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite', action='store_true',
            help='Re-upload even if a Cloudinary image is already set'
        )

    def handle(self, *args, **options):
        try:
            import cloudinary
            import cloudinary.uploader
        except ImportError:
            self.stdout.write(self.style.ERROR(
                'cloudinary package not installed. Run: pip install cloudinary'))
            return

        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
        api_key    = os.environ.get('CLOUDINARY_API_KEY', '')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET', '')

        if not all([cloud_name, api_key, api_secret]):
            self.stdout.write(self.style.ERROR(
                'Missing Cloudinary credentials.\n'
                'Set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, '
                'CLOUDINARY_API_SECRET environment variables.'
            ))
            return

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True,
        )

        products = Product.objects.filter(is_available=True)
        if not options['overwrite']:
            products = products.filter(image='')

        total   = products.count()
        success = 0
        failed  = 0

        self.stdout.write(f'\nUploading images for {total} products to Cloudinary...\n')

        for product in products:
            if not product.image_url:
                self.stdout.write(f'  SKIP  {product.name} — no image_url set')
                continue

            # Build a clean Cloudinary public_id from the product slug
            public_id = f'egv/products/{product.slug}'

            try:
                self.stdout.write(f'  Uploading: {product.name}...', ending=' ')

                result = cloudinary.uploader.upload(
                    product.image_url,
                    public_id    = public_id,
                    folder       = '',           # folder already in public_id
                    overwrite    = True,
                    resource_type= 'image',
                    transformation = [
                        {'width': 700, 'height': 500,
                         'crop': 'fill', 'gravity': 'auto',
                         'fetch_format': 'auto', 'quality': 'auto'}
                    ]
                )

                # Save the public_id back to the product
                product.image = result['public_id']
                product.save(update_fields=['image'])

                self.stdout.write(self.style.SUCCESS(f'OK → {result["public_id"]}'))
                success += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'FAILED — {e}'))
                failed += 1

        self.stdout.write('\n' + '─' * 56)
        self.stdout.write(self.style.SUCCESS(f'Done. {success} uploaded, {failed} failed.'))
        if failed:
            self.stdout.write('Re-run with --overwrite to retry failed uploads.')
