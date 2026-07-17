from django.db import models
import random, string

class Category(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order       = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ['order','name']; verbose_name_plural='Categories'
    def __str__(self): return self.name

class Product(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    description = models.TextField()
    price_ugx   = models.DecimalField(max_digits=12, decimal_places=0)
    unit        = models.CharField(max_length=60)
    image       = models.CharField(max_length=500, blank=True, help_text='Cloudinary public_id')
    image_url   = models.URLField(blank=True, help_text='Fallback image URL')
    stock_quantity = models.PositiveIntegerField(default=500)
    is_available   = models.BooleanField(default=True)
    is_featured    = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['category__order','name']
    def __str__(self): return self.name
    def formatted_price(self): return f"UGX {int(self.price_ugx):,}"
    def get_image_url(self, width=700, height=500):
        if self.image:
            try:
                import cloudinary
                return cloudinary.CloudinaryImage(self.image).build_url(
                    width=width, height=height, crop='fill', gravity='auto',
                    fetch_format='auto', quality='auto')
            except Exception:
                pass
        return self.image_url or ''
    def get_thumb_url(self): return self.get_image_url(width=400, height=300)

def _order_number():
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits  = ''.join(random.choices(string.digits, k=4))
    return f"EGV-{letters}{digits}"

class Order(models.Model):
    STATUS  = [('pending','Pending'),('confirmed','Confirmed'),('processing','Processing'),('dispatched','Dispatched'),('delivered','Delivered'),('cancelled','Cancelled')]
    PAYMENT = [('mtn_momo','MTN Mobile Money'),('airtel','Airtel Money'),('cod','Cash on Delivery'),('bank','Bank Transfer')]
    order_number     = models.CharField(max_length=20, unique=True, editable=False)
    first_name       = models.CharField(max_length=100)
    last_name        = models.CharField(max_length=100)
    email            = models.EmailField()
    phone            = models.CharField(max_length=20)
    delivery_address = models.TextField()
    district         = models.CharField(max_length=100)
    payment_method   = models.CharField(max_length=20, choices=PAYMENT)
    payment_phone    = models.CharField(max_length=20, blank=True)
    subtotal         = models.DecimalField(max_digits=15, decimal_places=0)
    delivery_fee     = models.DecimalField(max_digits=10, decimal_places=0, default=10000)
    total            = models.DecimalField(max_digits=15, decimal_places=0)
    status           = models.CharField(max_length=20, choices=STATUS, default='pending')
    notes            = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def save(self, *args, **kwargs):
        if not self.order_number:
            while True:
                n = _order_number()
                if not Order.objects.filter(order_number=n).exists():
                    self.order_number = n; break
        super().save(*args, **kwargs)
    def __str__(self): return self.order_number

class OrderItem(models.Model):
    order        = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product      = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    quantity     = models.PositiveIntegerField()
    unit_price   = models.DecimalField(max_digits=12, decimal_places=0)
    @property
    def line_total(self): return self.unit_price * self.quantity
    def formatted_total(self): return f"UGX {int(self.line_total):,}"
    def __str__(self): return f"{self.quantity} x {self.product_name}"


# ── Contact Messages ──────────────────────────────────────────
class ContactMessage(models.Model):
    name       = models.CharField(max_length=120)
    email      = models.EmailField()
    phone      = models.CharField(max_length=25, blank=True)
    subject    = models.CharField(max_length=200, blank=True)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f"{self.name} — {self.subject or 'No subject'}"

# ── Newsletter ────────────────────────────────────────────────
class Newsletter(models.Model):
    email         = models.EmailField(unique=True)
    name          = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active     = models.BooleanField(default=True)
    class Meta: ordering = ['-subscribed_at']
    def __str__(self): return self.email

# ── Product Reviews ───────────────────────────────────────────
class ProductReview(models.Model):
    RATINGS = [(i, f'{i} Star{"s" if i>1 else ""}') for i in range(1,6)]
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name        = models.CharField(max_length=100)
    location    = models.CharField(max_length=100, blank=True)
    rating      = models.PositiveSmallIntegerField(choices=RATINGS, default=5)
    comment     = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f"{self.name} — {self.product.name} ({self.rating}★)"
    @property
    def stars(self): return '★' * self.rating + '☆' * (5 - self.rating)

# ── News Posts ────────────────────────────────────────────────
class NewsPost(models.Model):
    CATS = [('agriculture','Agriculture'),('technology','Technology'),('trade','Trade'),('infrastructure','Infrastructure'),('company','Company')]
    title      = models.CharField(max_length=200)
    slug       = models.SlugField(unique=True)
    category   = models.CharField(max_length=30, choices=CATS, default='company')
    summary    = models.TextField(max_length=300)
    body       = models.TextField(blank=True)
    image_url  = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-published_at']
    def __str__(self): return self.title
