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
