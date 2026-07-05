from django.shortcuts import render, redirect

# ── Shared news data ──────────────────────────────────────────
ALL_NEWS = [
    {
        'id': 1, 'category': 'Technology', 'cat_class': 'nt',
        'title': 'EGV Launches Digital Training Portal for East African SMEs',
        'excerpt': 'A new platform supporting over 5,000 small businesses with digital skills training, e-commerce onboarding, and cloud service access launches this quarter across Uganda and Kenya.',
        'date': 'Jun 24, 2026', 'read_time': '4 min',
    },
    {
        'id': 2, 'category': 'Trade', 'cat_class': 'ntr',
        'title': 'EGV Secures Cross-Border Trade Partnership Across 7 Border Points',
        'excerpt': 'A strategic agreement with regional logistics partners expands EGV\'s trade facilitation network, reducing cross-border clearance times by up to 40% and opening new economic corridors.',
        'date': 'Jun 18, 2026', 'read_time': '5 min',
    },
    {
        'id': 3, 'category': 'Agriculture', 'cat_class': 'na',
        'title': 'Q3 Agri Training Cohort Launches with Record 400-Farmer Enrollment',
        'excerpt': 'This season\'s training program begins in Masaka, Soroti, and Gulu, focused on climate-resilient crop management and modern post-harvest techniques.',
        'date': 'Jun 14, 2026', 'read_time': '3 min',
    },
    {
        'id': 4, 'category': 'Infrastructure', 'cat_class': 'ni',
        'title': 'EGV Completes Phase I of Northern Corridor Road Rehabilitation',
        'excerpt': 'The first phase of the Northern Corridor road rehabilitation project has been successfully completed, improving transport connectivity for over 200,000 people across three districts.',
        'date': 'Jun 10, 2026', 'read_time': '6 min',
    },
    {
        'id': 5, 'category': 'Technology', 'cat_class': 'nt',
        'title': 'New Cybersecurity Framework Deployed Across 12 Government Agencies',
        'excerpt': 'EGV\'s technology division has successfully deployed a comprehensive cybersecurity framework across 12 East African government agencies, protecting critical national infrastructure.',
        'date': 'Jun 5, 2026', 'read_time': '4 min',
    },
    {
        'id': 6, 'category': 'Agriculture', 'cat_class': 'na',
        'title': 'EGV Partners with FAO on Climate-Smart Agriculture Initiative',
        'excerpt': 'A new partnership with the Food and Agriculture Organisation will bring climate-smart agricultural practices to 10,000 additional smallholder farmers across Uganda, Kenya and Tanzania.',
        'date': 'May 28, 2026', 'read_time': '5 min',
    },
]

ALL_JOBS = [
    {
        'title': 'Senior Software Engineer', 'sector': 'Technology', 'sector_class': 'tech',
        'location': 'Kampala, Uganda', 'type': 'Full-Time', 'level': 'Senior',
    },
    {
        'title': 'Agricultural Extension Officer', 'sector': 'Agriculture', 'sector_class': 'agri',
        'location': 'Masaka / Soroti, Uganda', 'type': 'Full-Time', 'level': 'Mid-Level',
    },
    {
        'title': 'Trade Compliance Analyst', 'sector': 'Trade', 'sector_class': 'trade',
        'location': 'Nairobi, Kenya', 'type': 'Full-Time', 'level': 'Mid-Level',
    },
    {
        'title': 'Civil Engineer – Roads & Infrastructure', 'sector': 'Infrastructure', 'sector_class': 'infra',
        'location': 'Kampala, Uganda', 'type': 'Full-Time', 'level': 'Senior',
    },
    {
        'title': 'Digital Marketing & Communications Lead', 'sector': 'Technology', 'sector_class': 'tech',
        'location': 'Kampala, Uganda (Hybrid)', 'type': 'Full-Time', 'level': 'Mid-Level',
    },
    {
        'title': 'Agribusiness Development Officer', 'sector': 'Agriculture', 'sector_class': 'agri',
        'location': 'Gulu, Uganda', 'type': 'Full-Time', 'level': 'Entry-Level',
    },
    {
        'title': 'Cross-Border Logistics Coordinator', 'sector': 'Trade', 'sector_class': 'trade',
        'location': 'Busia, Uganda / Malaba', 'type': 'Full-Time', 'level': 'Mid-Level',
    },
    {
        'title': 'Project Manager – Public Works', 'sector': 'Infrastructure', 'sector_class': 'infra',
        'location': 'Kampala, Uganda', 'type': 'Contract', 'level': 'Senior',
    },
]


# ── Views ─────────────────────────────────────────────────────
def home(request):
    return render(request, 'core/home.html', {'news_items': ALL_NEWS[:3]})


def about(request):
    return render(request, 'core/about.html')


def sectors(request):
    active_tab = request.GET.get('tab', 'all')
    valid = ['all', 'technology', 'agriculture', 'trade', 'infrastructure']
    if active_tab not in valid:
        active_tab = 'all'
    return render(request, 'core/sectors.html', {'active_tab': active_tab})


def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        email      = request.POST.get('email', '').strip()
        if first_name and email:
            # PRG: redirect after successful POST so browser refresh doesn't re-submit
            return redirect('/contact/?sent=1')
    success = request.GET.get('sent') == '1'
    return render(request, 'core/contact.html', {'success': success})


def news(request):
    category = request.GET.get('category', 'all').lower()
    if category == 'all':
        filtered = ALL_NEWS
    else:
        filtered = [n for n in ALL_NEWS if n['category'].lower() == category]
    return render(request, 'core/news.html', {
        'news_items': filtered,
        'active_category': category,
        'all_news': ALL_NEWS,
    })


def sustainability(request):
    return render(request, 'core/sustainability.html')


def careers(request):
    sector_filter = request.GET.get('sector', 'all').lower()
    if sector_filter == 'all':
        filtered_jobs = ALL_JOBS
    else:
        filtered_jobs = [j for j in ALL_JOBS if j['sector'].lower() == sector_filter]
    return render(request, 'core/careers.html', {
        'jobs': filtered_jobs,
        'active_sector': sector_filter,
        'total_jobs': len(ALL_JOBS),
    })


def privacy(request):
    return render(request, 'core/privacy.html')


# ── Products & Services views ──────────────────────────────
def products_hub(request):
    return render(request, 'core/products_hub.html')

def products_technology(request):
    return render(request, 'core/products_technology.html')

def products_agriculture(request):
    return render(request, 'core/products_agriculture.html')

def products_trade(request):
    return render(request, 'core/products_trade.html')

def products_infrastructure(request):
    return render(request, 'core/products_infrastructure.html')


def handler404(request, exception):
    return render(request, 'core/404.html', status=404)


# ════════════════════════════════════════════════════════════
# AGRICULTURE SHOP VIEWS
# ════════════════════════════════════════════════════════════
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from decimal import Decimal


def agri_shop(request):
    categories = Category.objects.prefetch_related('products')
    cat_slug   = request.GET.get('category', 'all')
    search     = request.GET.get('q', '').strip()
    min_price  = request.GET.get('min_price', '')
    max_price  = request.GET.get('max_price', '')
    featured_only = request.GET.get('featured', '')

    products = Product.objects.filter(is_available=True).select_related('category')

    if cat_slug != 'all':
        products = products.filter(category__slug=cat_slug)
    if search:
        products = products.filter(name__icontains=search)
    if min_price:
        try: products = products.filter(price_ugx__gte=int(min_price))
        except ValueError: pass
    if max_price:
        try: products = products.filter(price_ugx__lte=int(max_price))
        except ValueError: pass
    if featured_only:
        products = products.filter(is_featured=True)

    all_count = Product.objects.filter(is_available=True).count()
    featured  = Product.objects.filter(is_available=True, is_featured=True).select_related('category')[:6]

    return render(request, 'core/agri_shop.html', {
        'categories':      categories,
        'products':        products,
        'featured':        featured,
        'active_category': cat_slug,
        'search_query':    search,
        'all_count':       all_count,
    })


def agri_product(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=product.pk)[:4]
    return render(request, 'core/agri_product.html', {
        'product': product,
        'related': related,
    })


def agri_cart(request):
    cart = Cart(request)
    return render(request, 'core/agri_cart.html', {'cart': cart})


def agri_cart_add(request, pk):
    product  = get_object_or_404(Product, pk=pk, is_available=True)
    cart     = Cart(request)
    qty      = int(request.POST.get('quantity', 1))
    override = request.POST.get('override') == '1'
    cart.add(product, quantity=qty, override=override)
    next_url = request.POST.get('next') or ''
    if next_url and '?' in next_url:
        next_url += '&cart_added=1'
    elif next_url:
        next_url += '?cart_added=1'
    else:
        next_url = '/agriculture/cart/?cart_added=1'
    return redirect(next_url)


def agri_cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Cart(request).remove(product)
    return redirect('agri_cart')


def agri_cart_update(request):
    cart = Cart(request)
    for key, val in request.POST.items():
        if key.startswith('qty_'):
            pid = key[4:]
            try:
                qty = int(val)
                if qty > 0:
                    cart.cart[pid]['quantity'] = qty
                else:
                    cart.remove_by_id(pid)
            except (ValueError, KeyError):
                pass
    cart._save()
    return redirect('agri_cart')


def agri_checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('agri_shop')

    if request.method == 'POST':
        p = request.POST
        # Validate required fields
        required = ['first_name', 'last_name', 'email', 'phone',
                    'delivery_address', 'district', 'payment_method']
        errors = {f: 'This field is required.' for f in required if not p.get(f, '').strip()}

        if not errors:
            subtotal = cart.subtotal()
            delivery = cart.DELIVERY_FEE
            total    = subtotal + delivery

            order = Order.objects.create(
                first_name       = p['first_name'].strip(),
                last_name        = p['last_name'].strip(),
                email            = p['email'].strip(),
                phone            = p['phone'].strip(),
                delivery_address = p['delivery_address'].strip(),
                district         = p['district'].strip(),
                payment_method   = p['payment_method'],
                payment_phone    = p.get('payment_phone', '').strip(),
                subtotal         = subtotal,
                delivery_fee     = delivery,
                total            = total,
                notes            = p.get('notes', '').strip(),
            )
            for item in cart:
                OrderItem.objects.create(
                    order        = order,
                    product      = item['product'],
                    product_name = item['name'],
                    quantity     = item['quantity'],
                    unit_price   = item['unit_price'],
                )
            cart.clear()
            return redirect('agri_order_success', order_number=order.order_number)

        return render(request, 'core/agri_checkout.html', {
            'cart': cart, 'errors': errors, 'post': p,
        })

    districts = [
        'Kampala','Wakiso','Mukono','Jinja','Mbale','Gulu','Lira',
        'Mbarara','Fort Portal','Kabale','Soroti','Arua','Masaka',
        'Entebbe','Kasese','Hoima','Tororo','Iganga','Mityana','Other',
    ]
    return render(request, 'core/agri_checkout.html', {
        'cart': cart, 'districts': districts, 'errors': {}, 'post': {},
    })


def agri_order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'core/agri_order_success.html', {'order': order})


def agri_order_track(request):
    order  = None
    error  = None
    number = request.GET.get('order_number', '').strip().upper()
    if number:
        try:
            order = Order.objects.get(order_number=number)
        except Order.DoesNotExist:
            error = f'No order found with number "{number}". Please check and try again.'
    return render(request, 'core/agri_order_track.html', {
        'order': order, 'error': error, 'number': number,
    })


def handler500(request, *args, **kwargs):
    return render(request, 'core/500.html', status=500)


def sitemap_xml(request):
    from django.http import HttpResponse
    base = "https://edgar-ventures.onrender.com"
    pages = [
        "/", "/about/", "/sectors/", "/products/",
        "/products/technology/", "/products/agriculture/",
        "/products/trade/", "/products/infrastructure/",
        "/agriculture/shop/", "/sustainability/",
        "/news/", "/careers/", "/contact/",
    ]
    rows = ""
    for p in pages:
        rows += "  <url><loc>{}{}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n".format(base, p)
    header = '<?xml version="1.0" encoding="UTF-8"?>'
    body   = "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n{}\n</urlset>".format(rows)
    return HttpResponse(header + "\n" + body, content_type="application/xml")


def robots_txt(request):
    from django.http import HttpResponse
    txt = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /agriculture/cart/
Disallow: /agriculture/checkout/
Disallow: /agriculture/order/

Sitemap: https://edgar-ventures.onrender.com/sitemap.xml
"""
    return HttpResponse(txt, content_type='text/plain')
