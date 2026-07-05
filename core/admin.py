from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageWidget(admin.ModelAdmin):
    """Mixin that adds a Cloudinary upload widget to the Product admin."""
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['image_preview', 'name', 'category', 'price_ugx',
                     'unit', 'stock_quantity', 'is_available', 'is_featured']
    list_filter   = ['category', 'is_available', 'is_featured']
    list_editable = ['price_ugx', 'stock_quantity', 'is_available', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview_large', 'cloudinary_help']

    fieldsets = [
        ('Basic Info', {
            'fields': ['name', 'slug', 'category', 'description']
        }),
        ('Pricing & Stock', {
            'fields': ['price_ugx', 'unit', 'stock_quantity', 'is_available', 'is_featured']
        }),
        ('Image — Upload to Cloudinary', {
            'fields': ['cloudinary_help', 'image', 'image_preview_large', 'image_url'],
            'description': 'Upload an image via the widget below. '
                           'If no Cloudinary image is set, the external URL is used as fallback.'
        }),
    ]

    @admin.display(description='Preview')
    def image_preview(self, obj):
        url = obj.get_image_url(width=80, height=60)
        if url:
            return format_html(
                '<img src="{}" style="width:80px;height:60px;object-fit:cover;'
                'border-radius:6px;border:1px solid #eee">',
                url
            )
        return '—'

    @admin.display(description='Current Image')
    def image_preview_large(self, obj):
        url = obj.get_image_url(width=400, height=280)
        if url:
            return format_html(
                '<img src="{}" style="max-width:400px;max-height:280px;'
                'object-fit:cover;border-radius:8px;border:1px solid #ddd;margin-top:8px">',
                url
            )
        return 'No image uploaded yet.'

    @admin.display(description='')
    def cloudinary_help(self, obj):
        if obj.image:
            return format_html(
                '<div style="background:#e8f5e9;border:1px solid #a5d6a7;padding:10px 14px;'
                'border-radius:6px;font-size:13px;margin-bottom:8px">'
                '✅ <strong>Cloudinary image set:</strong> <code>{}</code><br>'
                '<small>Clear the field above and save to remove it.</small></div>',
                obj.image
            )
        return format_html(
            '<div style="background:#fff8e1;border:1px solid #ffe082;padding:10px 14px;'
            'border-radius:6px;font-size:13px;margin-bottom:8px">'
            '📷 <strong>How to upload:</strong> '
            'Paste the Cloudinary <em>public_id</em> into the Image field, '
            'or use the Cloudinary Media Library widget. '
            'After saving, the image will be served at optimised size automatically.</div>'
        )


class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 0
    fields = ['product', 'product_name', 'quantity', 'unit_price']
    readonly_fields = ['product_name', 'unit_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ['order_number', 'first_name', 'last_name', 'phone',
                      'total_display', 'payment_method', 'status', 'created_at']
    list_filter    = ['status', 'payment_method', 'district']
    list_editable  = ['status']
    search_fields  = ['order_number', 'first_name', 'last_name', 'email', 'phone']
    inlines        = [OrderItemInline]
    readonly_fields= ['order_number', 'created_at']
    fieldsets = [
        ('Order Info',   {'fields': ['order_number', 'status', 'created_at', 'notes']}),
        ('Customer',     {'fields': ['first_name', 'last_name', 'email', 'phone']}),
        ('Delivery',     {'fields': ['delivery_address', 'district']}),
        ('Payment',      {'fields': ['payment_method', 'payment_phone']}),
        ('Totals',       {'fields': ['subtotal', 'delivery_fee', 'total']}),
    ]

    @admin.display(description='Total', ordering='total')
    def total_display(self, obj):
        return f"UGX {int(obj.total):,}"
