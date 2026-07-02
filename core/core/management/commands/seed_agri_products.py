"""
Run once after first deployment:
  python manage.py seed_agri_products
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Category, Product


CATEGORIES = [
    {'name': 'Coffee', 'slug': 'coffee', 'description': 'Premium Ugandan coffee beans and ground coffee', 'order': 1},
    {'name': 'Grains & Cereals', 'slug': 'grains-cereals', 'description': 'Maize, rice, millet, sorghum and more', 'order': 2},
    {'name': 'Beans & Legumes', 'slug': 'beans-legumes', 'description': 'Kidney beans, groundnuts, soya and more', 'order': 3},
    {'name': 'Cash Crops & Spices', 'slug': 'cash-crops-spices', 'description': 'Vanilla, sesame, sunflower and spices', 'order': 4},
    {'name': 'Fresh Produce', 'slug': 'fresh-produce', 'description': 'Fresh fruits and vegetables from Ugandan farms', 'order': 5},
]

PRODUCTS = [
    # ── Coffee ──────────────────────────────────────────────────────────────
    {'cat': 'coffee', 'name': 'Arabica Green Coffee Beans', 'price': 8500, 'unit': 'per kg',
     'desc': 'High-altitude Arabica green coffee beans from Mount Elgon and Rwenzori regions. Naturally sun-dried, hand-sorted, and ready for roasting. Flavour notes: bright acidity, floral aroma, hints of berry.',
     'img': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=700&q=80', 'featured': True},
    {'cat': 'coffee', 'name': 'Robusta Green Coffee Beans', 'price': 5500, 'unit': 'per kg',
     'desc': 'Uganda Robusta green beans from the Lake Victoria region. Known for their bold, full-bodied character and earthy flavour profile. Excellent for espresso blends.',
     'img': 'https://images.unsplash.com/photo-1511537190424-bbbab87ac5eb?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'coffee', 'name': 'Arabica Roasted Coffee Beans', 'price': 18000, 'unit': 'per 500g',
     'desc': 'Medium-roast Arabica beans from certified Ugandan farms. Roasted in small batches to preserve the complex flavour notes. Ideal for filter, pour-over, or French press brewing.',
     'img': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=700&q=80', 'featured': True},
    {'cat': 'coffee', 'name': 'EGV Premium Ground Coffee', 'price': 14000, 'unit': 'per 250g',
     'desc': 'Freshly ground Arabica coffee, medium-fine grind suitable for drip coffee makers, French press, and Moka pots. Vacuum-sealed to preserve freshness. A true taste of Uganda in every cup.',
     'img': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=700&q=80', 'featured': True},
    {'cat': 'coffee', 'name': 'Instant Arabica Coffee', 'price': 8500, 'unit': 'per 100g',
     'desc': 'Pure Ugandan Arabica instant coffee — no fillers, no additives. Dissolves instantly in hot water for a rich, aromatic cup. Convenient for travel and office.',
     'img': 'https://images.unsplash.com/photo-1512568400610-62da28bc8a13?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'coffee', 'name': 'Coffee Husks (Cascara)', 'price': 4500, 'unit': 'per 200g',
     'desc': 'Dried coffee cherry skins (cascara) from Arabica processing. Brew as a herbal tea for a sweet, fruity, lightly caffeinated drink. A zero-waste coffee by-product rich in antioxidants.',
     'img': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=700&q=80'},

    # ── Grains & Cereals ────────────────────────────────────────────────────
    {'cat': 'grains-cereals', 'name': 'White Maize', 'price': 1200, 'unit': 'per kg',
     'desc': 'Clean, dry white maize from Eastern Uganda. Sorted and dried to optimal moisture content. Suitable for milling, animal feed, or direct cooking.',
     'img': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=700&q=80', 'featured': True},
    {'cat': 'grains-cereals', 'name': 'Maize Flour — Fine Ground', 'price': 5500, 'unit': 'per 2 kg',
     'desc': 'Finely milled white maize flour ideal for making posho (ugali), porridge, and baked goods. Freshly milled, no additives, and packed in food-grade bags.',
     'img': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Sorghum Grain', 'price': 1800, 'unit': 'per kg',
     'desc': 'Drought-resistant sorghum grain from Northern Uganda. Gluten-free, high in fibre, and rich in antioxidants. Used for porridge, local brew, and animal feed.',
     'img': 'https://images.unsplash.com/photo-1508747703725-719777637510?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Brown Rice — Local', 'price': 4500, 'unit': 'per kg',
     'desc': 'Locally grown brown rice from the Doho Rice Irrigation Scheme, Eastern Uganda. Unpolished, nutty flavour, higher fibre and nutrition than white rice.',
     'img': 'https://images.unsplash.com/photo-1536304993881-ff86e0c9ef6e?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Finger Millet (Eleusine)', 'price': 2800, 'unit': 'per kg',
     'desc': 'Finger millet from the Rwenzori foothills — one of the most nutritious grains grown in Uganda. Rich in calcium and iron. Used for porridge, bread flour, and traditional fermented drinks.',
     'img': 'https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Cassava Flour', 'price': 4800, 'unit': 'per 2 kg',
     'desc': 'Sun-dried and finely milled cassava flour from Central Uganda. Gluten-free alternative for baking, thickening sauces, and making traditional cassava dishes.',
     'img': 'https://images.unsplash.com/photo-1600326145552-327f74bd7dca?auto=format&fit=crop&w=700&q=80'},

    # ── Beans & Legumes ─────────────────────────────────────────────────────
    {'cat': 'beans-legumes', 'name': 'Kidney Beans — Dark Red', 'price': 5000, 'unit': 'per kg',
     'desc': 'Large dark red kidney beans from Eastern Uganda. Hand-sorted, clean, and dry. High in protein and fibre — ideal for stews, rice dishes, and soups.',
     'img': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=700&q=80', 'featured': True},
    {'cat': 'beans-legumes', 'name': 'White Beans (Nambale)', 'price': 4500, 'unit': 'per kg',
     'desc': 'Small white Nambale beans — a Ugandan staple. Clean, sorted, and dry. Perfect for traditional Ugandan bean stew, soups, or mixed rice dishes.',
     'img': 'https://images.unsplash.com/photo-1498979104386-e00dca9d7b93?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'beans-legumes', 'name': 'Soyabeans', 'price': 3500, 'unit': 'per kg',
     'desc': 'Yellow soyabeans from Northern Uganda. Versatile protein source for human consumption and livestock feed. Also used for soya milk, soya flour, and tofu production.',
     'img': 'https://images.unsplash.com/photo-1573246123716-6b1782bfc499?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'beans-legumes', 'name': 'Groundnuts / Peanuts — Raw', 'price': 6500, 'unit': 'per kg',
     'desc': 'Freshly harvested raw groundnuts from Lira and Soroti districts. Unsalted, unroasted. Used for groundnut paste (g-nut sauce), roasting, or pressing for oil.',
     'img': 'https://images.unsplash.com/photo-1567892320421-47f71d0a8ef8?auto=format&fit=crop&w=700&q=80', 'featured': True},
    {'cat': 'beans-legumes', 'name': 'Green Grams (Mung Beans)', 'price': 5500, 'unit': 'per kg',
     'desc': 'Green grams from Eastern Uganda. Quick-cooking, high-protein legume. Excellent for soups, salads, stews, and sprouting. A nutritious addition to any diet.',
     'img': 'https://images.unsplash.com/photo-1612257416648-2f665a3d2e37?auto=format&fit=crop&w=700&q=80'},

    # ── Cash Crops & Spices ─────────────────────────────────────────────────
    {'cat': 'cash-crops-spices', 'name': 'Vanilla Beans — Grade A', 'price': 48000, 'unit': 'per 50g (approx 5 pods)',
     'desc': 'Premium Grade A vanilla pods from West Uganda — among the finest in the world. Long, plump, moist beans with intense vanilla fragrance and flavour. Perfect for baking, ice cream, and extracts.',
     'img': 'https://images.unsplash.com/photo-1626544827763-d516dce335e2?auto=format&fit=crop&w=700&q=80', 'featured': True},
    {'cat': 'cash-crops-spices', 'name': 'Simsim / Sesame Seeds', 'price': 7500, 'unit': 'per kg',
     'desc': 'White sesame seeds from Northern Uganda. Hulled, clean, and dried to optimal moisture. Used for cooking oil, tahini, baking, and nutritional supplements.',
     'img': 'https://images.unsplash.com/photo-1609501676725-7186f017a4b7?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'cash-crops-spices', 'name': 'Sunflower Seeds — Oil Variety', 'price': 4500, 'unit': 'per kg',
     'desc': 'High-oil content sunflower seeds from Eastern Uganda. Suitable for pressing into cooking oil, roasting as a snack, or processing into sunflower flour.',
     'img': 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'cash-crops-spices', 'name': 'Dried Chili Peppers', 'price': 4000, 'unit': 'per 100g',
     'desc': 'Sun-dried hot chili peppers from Nakaseke. Intense heat with complex smoky undertones. Whole dried form preserves maximum flavour. Grind for chili powder or use whole in stews.',
     'img': 'https://images.unsplash.com/photo-1526346698789-22fd84314424?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'cash-crops-spices', 'name': 'Turmeric Root — Dried & Ground', 'price': 6000, 'unit': 'per 100g',
     'desc': 'Freshly dried and ground turmeric from Central Uganda. Deep orange colour, earthy aroma, and high curcumin content. Used in cooking, natural remedies, and health drinks.',
     'img': 'https://images.unsplash.com/photo-1615485500704-8e990f9900f7?auto=format&fit=crop&w=700&q=80'},

    # ── Fresh Produce ───────────────────────────────────────────────────────
    {'cat': 'fresh-produce', 'name': 'Fresh Pineapple', 'price': 3500, 'unit': 'per piece',
     'desc': 'Sweet, juicy Ugandan pineapples — considered among the world\'s finest for their unique sugar content and low acidity. Freshly harvested from Kayunga district. Typically 1–1.5 kg each.',
     'img': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?auto=format&fit=crop&w=700&q=80', 'featured': True},
    {'cat': 'fresh-produce', 'name': 'Passion Fruit', 'price': 4500, 'unit': 'per kg (approx 8–10 fruits)',
     'desc': 'Ripe yellow and purple passion fruits from Western Uganda highlands. Intensely aromatic with a sweet-tart pulp. Excellent for fresh juice, yoghurt, desserts, and smoothies.',
     'img': 'https://images.unsplash.com/photo-1604495636756-e71ab36b89c4?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fresh-produce', 'name': 'Sweet Potatoes', 'price': 1500, 'unit': 'per kg',
     'desc': 'Orange-fleshed sweet potatoes from Apac district — rich in beta-carotene, vitamin A, and fibre. Naturally sweet. Can be boiled, roasted, fried, or mashed.',
     'img': 'https://images.unsplash.com/photo-1596097635121-14b38c5d7a27?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fresh-produce', 'name': 'Ripe Matooke Banana (Bunch)', 'price': 8000, 'unit': 'per bunch (3–4 kg)',
     'desc': 'East African Highland Bananas (Matooke) from Mbarara — the most popular staple food in Uganda. Starchy, filling, and versatile. Boil, steam, or fry. A true Ugandan favourite.',
     'img': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=700&q=80'},
]


class Command(BaseCommand):
    help = 'Seed agriculture products into the database'

    def handle(self, *args, **options):
        # Categories
        cats = {}
        for c in CATEGORIES:
            obj, created = Category.objects.update_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'description': c['description'], 'order': c['order']}
            )
            cats[c['slug']] = obj
            self.stdout.write(f"  Category: {obj.name} ({'created' if created else 'updated'})")

        # Products
        count = 0
        for p in PRODUCTS:
            slug = slugify(p['name'])
            obj, created = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    'category':       cats[p['cat']],
                    'name':           p['name'],
                    'description':    p['desc'],
                    'price_ugx':      p['price'],
                    'unit':           p['unit'],
                    'image_url':      p.get('img', ''),
                    'is_featured':    p.get('featured', False),
                    'is_available':   True,
                }
            )
            count += 1
            self.stdout.write(f"  Product: {obj.name} — UGX {obj.price_ugx:,} ({obj.unit})")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {count} products seeded across {len(CATEGORIES)} categories.'))


