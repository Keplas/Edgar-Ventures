import os
from django.core.management.base import BaseCommand
from core.models import Product

class Command(BaseCommand):
    help = 'Upload product images from image_url to Cloudinary'
    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true')
    def handle(self, *args, **options):
        try:
            import cloudinary, cloudinary.uploader
        except ImportError:
            self.stdout.write(self.style.ERROR('cloudinary not installed')); return
        if not os.environ.get('CLOUDINARY_CLOUD_NAME'):
            self.stdout.write(self.style.ERROR('CLOUDINARY_CLOUD_NAME not set')); return
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME',''),
            api_key=os.environ.get('CLOUDINARY_API_KEY',''),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET',''),
            secure=True)
        products = Product.objects.filter(is_available=True)
        if not options['overwrite']:
            products = products.filter(image='')
        ok = fail = 0
        for product in products:
            if not product.image_url: continue
            try:
                self.stdout.write(f'  Uploading: {product.name}...', ending=' ')
                r = cloudinary.uploader.upload(product.image_url,
                    public_id=f'egv/products/{product.slug}', overwrite=True,
                    resource_type='image', transformation=[{'width':700,'height':500,'crop':'fill','gravity':'auto','fetch_format':'auto','quality':'auto'}])
                product.image = r['public_id']
                product.save(update_fields=['image'])
                self.stdout.write(self.style.SUCCESS('OK'))
                ok += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'FAIL: {e}')); fail += 1
        self.stdout.write(self.style.SUCCESS(f'\nDone. {ok} uploaded, {fail} failed.'))
