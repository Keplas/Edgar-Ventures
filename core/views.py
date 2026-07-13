from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Category, Product, Order, OrderItem
from .cart import Cart


# ── Core pages ────────────────────────────────────────────────
def home(request):
    featured = Product.objects.filter(is_featured=True, is_available=True)[:3]
    return render(request, 'core/home.html', {'featured_products': featured})

def about(request):           return render(request, 'core/about.html')
def sectors(request):         return render(request, 'core/sectors.html')
def contact(request):         return render(request, 'core/contact.html')
def news(request):            return render(request, 'core/news.html')
def sustainability(request):  return render(request, 'core/sustainability.html')
def careers(request):         return render(request, 'core/careers.html')
def privacy(request):         return render(request, 'core/privacy.html')

# ── Product sector pages ───────────────────────────────────────
def products_hub(request):            return render(request, 'core/products_hub.html')
def products_technology(request):     return render(request, 'core/products_technology.html')
def products_agriculture(request):    return render(request, 'core/products_agriculture.html')
def products_trade(request):          return render(request, 'core/products_trade.html')
def products_infrastructure(request): return render(request, 'core/products_infrastructure.html')

# ── Agriculture shop ──────────────────────────────────────────
def agri_shop(request):
    categories = Category.objects.all()
    products   = Product.objects.filter(is_available=True)
    cat_slug   = request.GET.get('category')
    q          = request.GET.get('q', '')
    if cat_slug:
        products = products.filter(category__slug=cat_slug)
    if q:
        products = products.filter(name__icontains=q)
    active_cat = None
    if cat_slug:
        try: active_cat = Category.objects.get(slug=cat_slug)
        except Category.DoesNotExist: pass
    return render(request, 'core/agri_shop.html', {
        'products': products, 'categories': categories,
        'active_cat': active_cat, 'q': q,
    })

def agri_product(request, slug):
    product  = get_object_or_404(Product, slug=slug, is_available=True)
    related  = Product.objects.filter(category=product.category, is_available=True).exclude(pk=product.pk)[:4]
    return render(request, 'core/agri_product.html', {'product': product, 'related': related})

def agri_cart(request):
    cart = Cart(request)
    return render(request, 'core/agri_cart.html', {'cart': cart})

def agri_cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart    = Cart(request)
    qty     = int(request.POST.get('quantity', 1))
    cart.add(product, qty)
    next_url = request.POST.get('next', '')
    sep = '&' if '?' in next_url else '?'
    return redirect((next_url + sep + 'cart_added=1') if next_url else '/agriculture/cart/?cart_added=1')

def agri_cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Cart(request).remove(product)
    return redirect('agri_cart')

def agri_cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        for key, val in request.POST.items():
            if key.startswith('qty_'):
                try:
                    pk  = int(key.split('_')[1])
                    qty = int(val)
                    p   = Product.objects.get(pk=pk)
                    cart.update(p, qty)
                except Exception:
                    pass
    return redirect('agri_cart')

def agri_checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('agri_cart')
    if request.method == 'POST':
        d = request.POST
        order = Order.objects.create(
            first_name=d.get('first_name',''), last_name=d.get('last_name',''),
            email=d.get('email',''), phone=d.get('phone',''),
            delivery_address=d.get('delivery_address',''), district=d.get('district',''),
            payment_method=d.get('payment_method','cod'), payment_phone=d.get('payment_phone',''),
            subtotal=cart.get_subtotal(), delivery_fee=10000, total=cart.get_total(),
            notes=d.get('notes',''),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order, product=item['product'],
                product_name=item['product'].name,
                quantity=item['qty'], unit_price=item['unit_price'],
            )
        cart.clear()
        return redirect('agri_order_success', order_number=order.order_number)
    return render(request, 'core/agri_checkout.html', {'cart': cart})

def agri_order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'core/agri_order_success.html', {'order': order})

def agri_order_track(request):
    order  = None; error = None
    number = request.GET.get('order_number', '').strip().upper()
    if number:
        try: order = Order.objects.get(order_number=number)
        except Order.DoesNotExist: error = f'No order found with number "{number}".'
    return render(request, 'core/agri_order_track.html', {'order': order, 'error': error, 'number': number})

# ── SEO & utilities ───────────────────────────────────────────
def handler404(request, exception=None):
    return render(request, 'core/404.html', status=404)

def handler500(request, *a, **k):
    return render(request, 'core/500.html', status=500)

def sitemap_xml(request):
    base  = 'https://edgar-ventures.onrender.com'
    pages = ['/','/about/','/sectors/','/products/','/products/technology/',
             '/products/agriculture/','/products/trade/','/products/infrastructure/',
             '/agriculture/shop/','/sustainability/','/news/','/careers/','/contact/']
    rows  = ''.join(f'  <url><loc>{base}{p}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n' for p in pages)
    xml   = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>'
    return HttpResponse(xml, content_type='application/xml')

def robots_txt(request):
    txt = "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /agriculture/cart/\nDisallow: /agriculture/checkout/\nSitemap: https://edgar-ventures.onrender.com/sitemap.xml\n"
    return HttpResponse(txt, content_type='text/plain')
