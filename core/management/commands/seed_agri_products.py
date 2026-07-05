"""
Run once after first deployment:
  python manage.py seed_agri_products
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Category, Product


CATEGORIES = [
    {'name': 'Coffee',                  'slug': 'coffee',                 'description': 'Premium Ugandan coffee beans and ground coffee',          'order': 1},
    {'name': 'Grains & Cereals',        'slug': 'grains-cereals',         'description': 'Maize, rice, millet, sorghum and more',                  'order': 2},
    {'name': 'Beans & Legumes',         'slug': 'beans-legumes',          'description': 'Kidney beans, groundnuts, soya and more',                 'order': 3},
    {'name': 'Cash Crops & Spices',     'slug': 'cash-crops-spices',      'description': 'Vanilla, sesame, sunflower and spices',                   'order': 4},
    {'name': 'Fresh Produce',           'slug': 'fresh-produce',          'description': 'Fresh fruits and vegetables from Ugandan farms',          'order': 5},
    {'name': 'Fertilizers',             'slug': 'fertilizers',            'description': 'NPK, Urea, DAP, organic and foliar fertilizers',          'order': 6},
    {'name': 'Pesticides & Herbicides', 'slug': 'pesticides-herbicides',  'description': 'Insecticides, herbicides and fungicides for crops',       'order': 7},
]

PRODUCTS = [
    # ── Coffee ──────────────────────────────────────────────────────────────
    {'cat': 'coffee', 'name': 'Arabica Green Coffee Beans', 'price': 8500, 'unit': 'per kg', 'featured': True,
     'desc': 'High-altitude Arabica green coffee beans from Mount Elgon and Rwenzori regions. Naturally sun-dried, hand-sorted, and ready for roasting. Flavour notes: bright acidity, floral aroma, hints of berry.',
     'img': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'coffee', 'name': 'Robusta Green Coffee Beans', 'price': 5500, 'unit': 'per kg',
     'desc': 'Uganda Robusta green beans from the Lake Victoria region. Known for their bold, full-bodied character and earthy flavour profile. Excellent for espresso blends.',
     'img': 'https://images.unsplash.com/photo-1511537190424-bbbab87ac5eb?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'coffee', 'name': 'Arabica Roasted Coffee Beans', 'price': 18000, 'unit': 'per 500g', 'featured': True,
     'desc': 'Medium-roast Arabica beans from certified Ugandan farms. Roasted in small batches to preserve complex flavour notes. Ideal for filter, pour-over, or French press brewing.',
     'img': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'coffee', 'name': 'EGV Premium Ground Coffee', 'price': 14000, 'unit': 'per 250g', 'featured': True,
     'desc': 'Freshly ground Arabica coffee, medium-fine grind suitable for drip coffee makers, French press, and Moka pots. Vacuum-sealed to preserve freshness. A true taste of Uganda in every cup.',
     'img': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'coffee', 'name': 'Instant Arabica Coffee', 'price': 8500, 'unit': 'per 100g',
     'desc': 'Pure Ugandan Arabica instant coffee — no fillers, no additives. Dissolves instantly in hot water for a rich, aromatic cup. Convenient for travel and office.',
     'img': 'https://images.unsplash.com/photo-1512568400610-62da28bc8a13?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'coffee', 'name': 'Coffee Husks (Cascara)', 'price': 4500, 'unit': 'per 200g',
     'desc': 'Dried coffee cherry skins (cascara) from Arabica processing. Brew as a herbal tea for a sweet, fruity, lightly caffeinated drink. A zero-waste coffee by-product rich in antioxidants.',
     'img': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=700&q=80'},

    # ── Grains & Cereals ────────────────────────────────────────────────────
    {'cat': 'grains-cereals', 'name': 'White Maize', 'price': 1200, 'unit': 'per kg', 'featured': True,
     'desc': 'Clean, dry white maize from Eastern Uganda. Sorted and dried to optimal moisture content. Suitable for milling, animal feed, or direct cooking.',
     'img': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Maize Flour Fine Ground', 'price': 5500, 'unit': 'per 2 kg',
     'desc': 'Finely milled white maize flour ideal for making posho, porridge, and baked goods. Freshly milled, no additives, packed in food-grade bags.',
     'img': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Sorghum Grain', 'price': 1800, 'unit': 'per kg',
     'desc': 'Drought-resistant sorghum grain from Northern Uganda. Gluten-free, high in fibre and rich in antioxidants. Used for porridge, local brew, and animal feed.',
     'img': 'https://images.unsplash.com/photo-1508747703725-719777637510?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Brown Rice Local', 'price': 4500, 'unit': 'per kg',
     'desc': 'Locally grown brown rice from the Doho Rice Irrigation Scheme, Eastern Uganda. Unpolished, nutty flavour, higher fibre and nutrition than white rice.',
     'img': 'https://images.unsplash.com/photo-1536304993881-ff86e0c9ef6e?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Finger Millet (Eleusine)', 'price': 2800, 'unit': 'per kg',
     'desc': 'Finger millet from the Rwenzori foothills — nutritious grain rich in calcium and iron. Used for porridge, bread flour, and traditional fermented drinks.',
     'img': 'https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'grains-cereals', 'name': 'Cassava Flour', 'price': 4800, 'unit': 'per 2 kg',
     'desc': 'Sun-dried and finely milled cassava flour from Central Uganda. Gluten-free alternative for baking, thickening sauces, and making traditional cassava dishes.',
     'img': 'https://images.unsplash.com/photo-1600326145552-327f74bd7dca?auto=format&fit=crop&w=700&q=80'},

    # ── Beans & Legumes ─────────────────────────────────────────────────────
    {'cat': 'beans-legumes', 'name': 'Kidney Beans Dark Red', 'price': 5000, 'unit': 'per kg', 'featured': True,
     'desc': 'Large dark red kidney beans from Eastern Uganda. Hand-sorted, clean, and dry. High in protein and fibre — ideal for stews, rice dishes, and soups.',
     'img': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'beans-legumes', 'name': 'White Beans (Nambale)', 'price': 4500, 'unit': 'per kg',
     'desc': 'Small white Nambale beans — a Ugandan staple. Clean, sorted, and dry. Perfect for traditional bean stew, soups, or mixed rice dishes.',
     'img': 'https://images.unsplash.com/photo-1498979104386-e00dca9d7b93?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'beans-legumes', 'name': 'Soyabeans', 'price': 3500, 'unit': 'per kg',
     'desc': 'Yellow soyabeans from Northern Uganda. Versatile protein source for human consumption and livestock feed.',
     'img': 'https://images.unsplash.com/photo-1573246123716-6b1782bfc499?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'beans-legumes', 'name': 'Groundnuts / Peanuts Raw', 'price': 6500, 'unit': 'per kg', 'featured': True,
     'desc': 'Freshly harvested raw groundnuts from Lira and Soroti districts. Unsalted, unroasted. Used for groundnut paste, roasting, or pressing for oil.',
     'img': 'https://images.unsplash.com/photo-1567892320421-47f71d0a8ef8?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'beans-legumes', 'name': 'Green Grams (Mung Beans)', 'price': 5500, 'unit': 'per kg',
     'desc': 'Green grams from Eastern Uganda. Quick-cooking, high-protein legume excellent for soups, salads, stews, and sprouting.',
     'img': 'https://images.unsplash.com/photo-1612257416648-2f665a3d2e37?auto=format&fit=crop&w=700&q=80'},

    # ── Cash Crops & Spices ─────────────────────────────────────────────────
    {'cat': 'cash-crops-spices', 'name': 'Vanilla Beans Grade A', 'price': 48000, 'unit': 'per 50g (approx 5 pods)', 'featured': True,
     'desc': 'Premium Grade A vanilla pods from West Uganda. Long, plump, moist beans with intense vanilla fragrance. Perfect for baking, ice cream, and extracts.',
     'img': 'https://images.unsplash.com/photo-1626544827763-d516dce335e2?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'cash-crops-spices', 'name': 'Simsim / Sesame Seeds', 'price': 7500, 'unit': 'per kg',
     'desc': 'White sesame seeds from Northern Uganda. Hulled, clean, and dried. Used for cooking oil, tahini, baking, and nutritional supplements.',
     'img': 'https://images.unsplash.com/photo-1609501676725-7186f017a4b7?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'cash-crops-spices', 'name': 'Sunflower Seeds Oil Variety', 'price': 4500, 'unit': 'per kg',
     'desc': 'High-oil content sunflower seeds from Eastern Uganda. Suitable for pressing into cooking oil, roasting as a snack, or processing into sunflower flour.',
     'img': 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'cash-crops-spices', 'name': 'Dried Chili Peppers', 'price': 4000, 'unit': 'per 100g',
     'desc': 'Sun-dried hot chili peppers from Nakaseke. Intense heat with smoky undertones. Grind for chili powder or use whole in stews.',
     'img': 'https://images.unsplash.com/photo-1526346698789-22fd84314424?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'cash-crops-spices', 'name': 'Turmeric Root Dried and Ground', 'price': 6000, 'unit': 'per 100g',
     'desc': 'Freshly dried and ground turmeric from Central Uganda. Deep orange colour, earthy aroma, and high curcumin content. Used in cooking, natural remedies, and health drinks.',
     'img': 'https://images.unsplash.com/photo-1615485500704-8e990f9900f7?auto=format&fit=crop&w=700&q=80'},

    # ── Fresh Produce ───────────────────────────────────────────────────────
    {'cat': 'fresh-produce', 'name': 'Fresh Pineapple', 'price': 3500, 'unit': 'per piece', 'featured': True,
     'desc': 'Sweet, juicy Ugandan pineapples from Kayunga district — among the world\'s finest for their unique sugar content and low acidity. Typically 1-1.5 kg each.',
     'img': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fresh-produce', 'name': 'Passion Fruit', 'price': 4500, 'unit': 'per kg (approx 8-10 fruits)',
     'desc': 'Ripe yellow and purple passion fruits from Western Uganda highlands. Intensely aromatic with sweet-tart pulp. Excellent for fresh juice, yoghurt, desserts, and smoothies.',
     'img': 'https://images.unsplash.com/photo-1604495636756-e71ab36b89c4?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fresh-produce', 'name': 'Sweet Potatoes', 'price': 1500, 'unit': 'per kg',
     'desc': 'Orange-fleshed sweet potatoes from Apac district — rich in beta-carotene, vitamin A, and fibre. Can be boiled, roasted, fried, or mashed.',
     'img': 'https://images.unsplash.com/photo-1596097635121-14b38c5d7a27?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fresh-produce', 'name': 'Ripe Matooke Banana Bunch', 'price': 8000, 'unit': 'per bunch (3-4 kg)',
     'desc': 'East African Highland Bananas (Matooke) from Mbarara — the most popular staple food in Uganda. Starchy, filling, and versatile. Boil, steam, or fry.',
     'img': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=700&q=80'},

    # ── Fertilizers ─────────────────────────────────────────────────────────
    {'cat': 'fertilizers', 'name': 'NPK 17-17-17 Compound Fertilizer', 'price': 145000, 'unit': 'per 50 kg bag', 'featured': True,
     'desc': 'Balanced NPK fertilizer with equal Nitrogen, Phosphorus and Potassium (17-17-17). Ideal at planting and top-dressing for maize, beans, coffee and vegetables. The most popular all-purpose fertilizer for Ugandan smallholder farmers.',
     'img': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'Urea Fertilizer 46% Nitrogen', 'price': 125000, 'unit': 'per 50 kg bag', 'featured': True,
     'desc': 'High-nitrogen urea (46-0-0) — the most concentrated solid nitrogen fertilizer available. Best as top-dressing for maize, sorghum, rice and pasture grasses. Rapidly boosts leafy growth and green colour.',
     'img': 'https://images.unsplash.com/photo-1560493676-04071c5f467b?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'DAP Diammonium Phosphate', 'price': 165000, 'unit': 'per 50 kg bag', 'featured': True,
     'desc': 'DAP (18-46-0) — the most widely used phosphorus fertilizer in East Africa. Applied at planting to promote strong roots, early establishment and improved flowering on maize, beans, potatoes and coffee.',
     'img': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'CAN Calcium Ammonium Nitrate', 'price': 115000, 'unit': 'per 50 kg bag',
     'desc': 'CAN (27% N) combines fast-acting nitrate with slower ammonium nitrogen plus calcium. Less volatile than urea — ideal for acidic Ugandan soils. Suitable for maize, vegetables and cereals.',
     'img': 'https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'Organic Compost Manure', 'price': 35000, 'unit': 'per 50 kg bag',
     'desc': 'Fully composted organic manure from animal waste and crop residues. Improves soil structure, moisture retention and microbial activity. Safe for all crops. Ideal for organic and climate-smart farming.',
     'img': 'https://images.unsplash.com/photo-1523741543316-beb7fc7023d8?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'Foliar Liquid Micronutrient Fertilizer', 'price': 28000, 'unit': 'per 1 litre',
     'desc': 'Complete liquid foliar feed with NPK plus Zinc, Boron, Iron, Magnesium and Manganese. Applied directly to leaves for fast absorption during critical growth stages. Corrects nutrient deficiencies rapidly on all crops.',
     'img': 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'Muriate of Potash MOP 60%', 'price': 88000, 'unit': 'per 25 kg bag',
     'desc': 'MOP (0-0-60) high-potassium fertilizer that improves drought resistance, fruit quality and disease resistance. Recommended for banana, potato, tomato, passion fruit and most fruiting crops grown in Uganda.',
     'img': 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'Single Super Phosphate SSP', 'price': 72000, 'unit': 'per 50 kg bag',
     'desc': 'SSP (0-18-0) enriched with Sulphur and Calcium. Promotes strong root formation, seed germination and early establishment. Cost-effective phosphate source for sulphur-deficient Ugandan soils.',
     'img': 'https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'Chicken Manure Pellets Organic', 'price': 42000, 'unit': 'per 50 kg bag',
     'desc': 'Processed and pelletised chicken manure — odour-controlled, pathogen-free and nutrient-rich. Contains NPK plus calcium and organic matter. Slow-release feeding over several months. Excellent for vegetable gardens and fruit trees.',
     'img': 'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'fertilizers', 'name': 'Zinc Sulphate Micronutrient', 'price': 18000, 'unit': 'per 1 kg',
     'desc': 'Zinc Sulphate (21% Zn) corrects zinc deficiency — one of the most common micronutrient problems in Ugandan maize. Apply as soil drench or foliar spray to fix stunted growth and poor cob formation.',
     'img': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=700&q=80'},

    # ── Pesticides & Herbicides ──────────────────────────────────────────────
    {'cat': 'pesticides-herbicides', 'name': 'Glyphosate 480 Herbicide', 'price': 18500, 'unit': 'per 1 litre', 'featured': True,
     'desc': 'Systemic non-selective herbicide (480g/L Glyphosate) controlling annual and perennial weeds. Applied post-emergence before planting or between rows. For maize, beans, coffee, banana and non-crop areas.',
     'img': 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Lambda Cyhalothrin Insecticide', 'price': 12000, 'unit': 'per 100 ml', 'featured': True,
     'desc': 'Fast-acting pyrethroid (50g/L Lambda Cyhalothrin) controlling aphids, stalkborers, bollworms, whiteflies, thrips and caterpillars. Quick knockdown with residual control on maize, beans, vegetables and coffee.',
     'img': 'https://images.unsplash.com/photo-1574943320219-553eb213f72d?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Mancozeb 80% Fungicide', 'price': 9500, 'unit': 'per 200 g',
     'desc': 'Broad-spectrum protective fungicide (800g/kg Mancozeb) for blight, leaf spot, anthracnose, rust and downy mildew. For tomato, potato, beans, onion, maize and coffee. Apply every 7-14 days in wet season.',
     'img': 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Imidacloprid Systemic Insecticide', 'price': 22000, 'unit': 'per 100 ml',
     'desc': 'Systemic neonicotinoid (200g/L Imidacloprid) absorbed through roots and leaves. Long-lasting protection against aphids, whiteflies, thrips, leafhoppers and soil insects on vegetables, maize, beans and coffee.',
     'img': 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Atrazine 50% Maize Herbicide', 'price': 14000, 'unit': 'per 500 g',
     'desc': 'Selective pre-emergence herbicide (500g/kg Atrazine) for weed control in maize. Controls broadleaf weeds and grasses including couch grass, black jack and wandering Jew. Apply within 3 days of planting.',
     'img': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Copper Oxychloride Fungicide', 'price': 8500, 'unit': 'per 200 g',
     'desc': 'Protective copper-based fungicide for angular leaf spot, anthracnose, coffee berry disease, black sigatoka and downy mildew. Highly effective and affordable for all major crop diseases in Uganda.',
     'img': 'https://images.unsplash.com/photo-1560493676-04071c5f467b?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Emamectin Benzoate Caterpillar Control', 'price': 24000, 'unit': 'per 100 ml',
     'desc': 'Highly effective (19g/L Emamectin Benzoate) for fall armyworm, stalkborers, caterpillars and leaf miners. Essential for controlling fall armyworm — the most destructive pest of Ugandan maize crops.',
     'img': 'https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Chlorpyrifos Soil Insecticide', 'price': 16000, 'unit': 'per 500 ml',
     'desc': 'Organophosphate (480g/L Chlorpyrifos) for soil pests: termites, cutworms, nematodes, ants and beetles. Applied as soil drench or furrow treatment at planting. Protects young seedling roots, bulbs and tubers.',
     'img': 'https://images.unsplash.com/photo-1574943320219-553eb213f72d?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Metalaxyl Anti-Downy Mildew Fungicide', 'price': 19500, 'unit': 'per 100 g',
     'desc': 'Systemic fungicide (350g/kg Metalaxyl) effective against downy mildew, late blight, damping-off and Phytophthora. Applied as seed treatment or foliar spray on maize, beans, potato, tomato and vegetables.',
     'img': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?auto=format&fit=crop&w=700&q=80'},
    {'cat': 'pesticides-herbicides', 'name': 'Neem Organic Pesticide Extract', 'price': 14000, 'unit': 'per 500 ml', 'featured': True,
     'desc': 'Cold-pressed neem oil (Azadirachtin) — 100% organic, environmentally safe pesticide and fungicide. Controls aphids, mites, whiteflies, mealybugs and fungal diseases. Safe for beneficial insects and mammals. Perfect for organic farming.',
     'img': 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?auto=format&fit=crop&w=700&q=80'},
]


class Command(BaseCommand):
    help = 'Seed agriculture products into the database'

    def handle(self, *args, **options):
        cats = {}
        for c in CATEGORIES:
            obj, created = Category.objects.update_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'description': c['description'], 'order': c['order']}
            )
            cats[c['slug']] = obj
            self.stdout.write(f"  Category: {obj.name} ({'created' if created else 'updated'})")

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
