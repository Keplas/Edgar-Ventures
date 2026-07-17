from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['img_preview','name','category','price_ugx','unit','is_available','is_featured']
    list_filter   = ['category','is_available','is_featured']
    list_editable = ['price_ugx','is_available','is_featured']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['img_large']

    @admin.display(description='')
    def img_preview(self, obj):
        url = obj.get_image_url(80,60)
        return format_html('<img src="{}" style="width:80px;height:60px;object-fit:cover;border-radius:4px">',url) if url else '—'

    @admin.display(description='Preview')
    def img_large(self, obj):
        url = obj.get_image_url(400,280)
        return format_html('<img src="{}" style="max-width:400px;border-radius:6px">',url) if url else 'No image'

class OrderItemInline(admin.TabularInline):
    model = OrderItem; extra = 0
    readonly_fields = ['product_name','unit_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['order_number','first_name','last_name','phone','total','payment_method','status','created_at']
    list_filter   = ['status','payment_method']
    list_editable = ['status']
    search_fields = ['order_number','first_name','last_name','phone']
    inlines       = [OrderItemInline]
    readonly_fields = ['order_number','created_at']

from .models import ContactMessage, Newsletter, ProductReview, NewsPost

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['name','email','subject','created_at','is_read']
    list_filter   = ['is_read']
    list_editable = ['is_read']
    search_fields = ['name','email','subject']
    readonly_fields = ['created_at']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display  = ['email','name','subscribed_at','is_active']
    list_filter   = ['is_active']
    list_editable = ['is_active']
    search_fields = ['email','name']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display  = ['name','product','rating','location','is_approved','created_at']
    list_filter   = ['is_approved','rating']
    list_editable = ['is_approved']
    search_fields = ['name','product__name']
    readonly_fields = ['created_at']

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display  = ['title','category','is_published','published_at']
    list_filter   = ['category','is_published']
    list_editable = ['is_published']
    prepopulated_fields = {'slug':('title',)}
    search_fields = ['title']
