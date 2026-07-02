from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'price_ugx', 'unit',
                     'stock_quantity', 'is_available', 'is_featured']
    list_filter   = ['category', 'is_available', 'is_featured']
    list_editable = ['price_ugx', 'stock_quantity', 'is_available', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 0
    fields = ['product', 'product_name', 'quantity', 'unit_price']
    readonly_fields = ['product_name', 'unit_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ['order_number', 'first_name', 'last_name', 'phone',
                      'total', 'payment_method', 'status', 'created_at']
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
