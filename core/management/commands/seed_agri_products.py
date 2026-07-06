"""
Run once after first deployment:
  python manage.py seed_agri_products

Categories: Coffee | Fertilizers | Pesticides & Herbicides
Images: Pexels (free, commercial use, no attribution required)
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Category, Product

P = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=700&h=500&fit=crop"
def px(photo_id): return P.format(id=photo_id)


CATEGORIES = [
    {'name': 'Coffee',                  'slug': 'coffee',                'description': 'Premium Ugandan coffee beans and ground coffee',    'order': 1},
    {'name': 'Fertilizers',             'slug': 'fertilizers',           'description': 'NPK, Urea, DAP, organic and foliar fertilizers',   'order': 2},
    {'name': 'Pesticides & Herbicides', 'slug': 'pesticides-herbicides', 'description': 'Insecticides, herbicides and fungicides for crops', 'order': 3},
]

PRODUCTS = [
    # ══ COFFEE (6) ══════════════════════════════════════════════════════════
    {'cat': 'coffee', 'name': 'Arabica Green Coffee Beans', 'price': 8500, 'unit': 'per kg', 'featured': True,
     'img': px(1695052),
     'desc': 'High-altitude Arabica green coffee beans from Mount Elgon and Rwenzori regions. Naturally sun-dried, hand-sorted, and ready for roasting. Flavour notes: bright acidity, floral aroma, hints of berry.'},

    {'cat': 'coffee', 'name': 'Robusta Green Coffee Beans', 'price': 5500, 'unit': 'per kg',
     'img': px(1002740),
     'desc': 'Uganda Robusta green beans from the Lake Victoria region. Known for their bold, full-bodied character and earthy flavour profile. Excellent for espresso blends and dark roasts.'},

    {'cat': 'coffee', 'name': 'Arabica Roasted Coffee Beans', 'price': 18000, 'unit': 'per 500g', 'featured': True,
     'img': px(302899),
     'desc': 'Medium-roast Arabica beans from certified Ugandan farms. Roasted in small batches to preserve complex flavour notes. Ideal for filter, pour-over, or French press brewing.'},

    {'cat': 'coffee', 'name': 'EGV Premium Ground Coffee', 'price': 14000, 'unit': 'per 250g', 'featured': True,
     'img': px(312418),
     'desc': 'Freshly ground Arabica coffee, medium-fine grind suitable for drip coffee makers, French press, and Moka pots. Vacuum-sealed to preserve freshness. A true taste of Uganda in every cup.'},

    {'cat': 'coffee', 'name': 'Instant Arabica Coffee', 'price': 8500, 'unit': 'per 100g',
     'img': px(374885),
     'desc': 'Pure Ugandan Arabica instant coffee — no fillers, no additives. Dissolves instantly in hot water for a rich, aromatic cup. Convenient for travel, home, and office.'},

    {'cat': 'coffee', 'name': 'Coffee Husks (Cascara)', 'price': 4500, 'unit': 'per 200g',
     'img': px(669162),
     'desc': 'Dried coffee cherry skins (cascara) from Arabica processing. Brew as a herbal tea for a sweet, fruity, lightly caffeinated drink. A zero-waste coffee by-product rich in antioxidants.'},

    # ══ FERTILIZERS (10) ════════════════════════════════════════════════════
    {'cat': 'fertilizers', 'name': 'NPK 17-17-17 Compound Fertilizer', 'price': 145000, 'unit': 'per 50 kg bag', 'featured': True,
     'img': px(28101456),
     'desc': 'Balanced NPK fertilizer (17-17-17) with equal Nitrogen, Phosphorus and Potassium. Ideal at planting and top-dressing for maize, beans, coffee and vegetables. The most popular all-purpose fertilizer for Ugandan smallholder farmers.'},

    {'cat': 'fertilizers', 'name': 'Urea Fertilizer 46% Nitrogen', 'price': 125000, 'unit': 'per 50 kg bag', 'featured': True,
     'img': px(28100859),
     'desc': 'High-nitrogen urea (46-0-0) — the most concentrated solid nitrogen fertilizer available. Best as top-dressing for maize, sorghum, rice and pasture grasses. Rapidly boosts leafy growth and green colour.'},

    {'cat': 'fertilizers', 'name': 'DAP Diammonium Phosphate', 'price': 165000, 'unit': 'per 50 kg bag', 'featured': True,
     'img': px(36185282),
     'desc': 'DAP (18-46-0) — the most widely used phosphorus fertilizer in East Africa. Applied at planting to promote strong roots, early establishment and improved flowering on maize, beans, potatoes and coffee.'},

    {'cat': 'fertilizers', 'name': 'CAN Calcium Ammonium Nitrate', 'price': 115000, 'unit': 'per 50 kg bag',
     'img': px(3094208),
     'desc': 'CAN (27% N) combines fast-acting nitrate with slower ammonium nitrogen plus calcium. Less volatile than urea — ideal for acidic Ugandan soils. Suitable for maize, vegetables and cereals.'},

    {'cat': 'fertilizers', 'name': 'Organic Compost Manure', 'price': 35000, 'unit': 'per 50 kg bag',
     'img': px(1382102),
     'desc': 'Fully composted organic manure from animal waste and crop residues. Improves soil structure, moisture retention and microbial activity. Safe for all crops. Ideal for organic and climate-smart farming.'},

    {'cat': 'fertilizers', 'name': 'Foliar Liquid Micronutrient Fertilizer', 'price': 28000, 'unit': 'per 1 litre',
     'img': px(1084584),
     'desc': 'Complete liquid foliar feed with NPK plus Zinc, Boron, Iron, Magnesium and Manganese. Applied directly to leaves for fast absorption. Corrects nutrient deficiencies rapidly on all crops.'},

    {'cat': 'fertilizers', 'name': 'Muriate of Potash MOP 60%', 'price': 88000, 'unit': 'per 25 kg bag',
     'img': px(2132250),
     'desc': 'MOP (0-0-60) high-potassium fertilizer that improves drought resistance, fruit quality and disease resistance. Recommended for banana, potato, tomato, passion fruit and most fruiting crops.'},

    {'cat': 'fertilizers', 'name': 'Single Super Phosphate SSP', 'price': 72000, 'unit': 'per 50 kg bag',
     'img': px(6280298),
     'desc': 'SSP (0-18-0) enriched with Sulphur and Calcium. Promotes strong root formation, seed germination and early establishment. Cost-effective phosphate source for sulphur-deficient Ugandan soils.'},

    {'cat': 'fertilizers', 'name': 'Chicken Manure Pellets Organic', 'price': 42000, 'unit': 'per 50 kg bag',
     'img': px(1090977),
     'desc': 'Processed and pelletised chicken manure — odour-controlled, pathogen-free and nutrient-rich. Slow-release feeding over several months. Excellent for vegetable gardens and fruit trees.'},

    {'cat': 'fertilizers', 'name': 'Zinc Sulphate Micronutrient', 'price': 18000, 'unit': 'per 1 kg',
     'img': px(36185281),
     'desc': 'Zinc Sulphate (21% Zn) corrects zinc deficiency — one of the most common micronutrient problems in Ugandan maize. Apply as soil drench or foliar spray to fix stunted growth and poor cob formation.'},

    # ══ PESTICIDES & HERBICIDES (10) ════════════════════════════════════════
    {'cat': 'pesticides-herbicides', 'name': 'Glyphosate 480 Herbicide', 'price': 18500, 'unit': 'per 1 litre', 'featured': True,
     'img': px(36390057),
     'desc': 'Systemic non-selective herbicide (480g/L Glyphosate) controlling annual and perennial weeds. Available at local EGV agro-supply points across Uganda. For maize, beans, coffee, banana and non-crop areas.'},

    {'cat': 'pesticides-herbicides', 'name': 'Lambda Cyhalothrin Insecticide', 'price': 12000, 'unit': 'per 100 ml', 'featured': True,
     'img': px(3680956),
     'desc': 'Fast-acting pyrethroid (50g/L Lambda Cyhalothrin) controlling aphids, stalkborers, bollworms, whiteflies, thrips and caterpillars. Quick knockdown with residual control on maize, beans and coffee.'},

    {'cat': 'pesticides-herbicides', 'name': 'Mancozeb 80% Fungicide', 'price': 9500, 'unit': 'per 200 g',
     'img': px(1537570),
     'desc': 'Broad-spectrum protective fungicide (800g/kg Mancozeb) for blight, leaf spot, anthracnose, rust and downy mildew. Apply every 7-14 days in wet season on tomato, potato, beans and coffee.'},

    {'cat': 'pesticides-herbicides', 'name': 'Imidacloprid Systemic Insecticide', 'price': 22000, 'unit': 'per 100 ml',
     'img': px(4022183),
     'desc': 'Systemic neonicotinoid (200g/L Imidacloprid) absorbed through roots and leaves. Long-lasting protection against aphids, whiteflies, thrips, leafhoppers and soil insects on vegetables, maize and coffee.'},

    {'cat': 'pesticides-herbicides', 'name': 'Atrazine 50% Maize Herbicide', 'price': 14000, 'unit': 'per 500 g',
     'img': px(5748809),
     'desc': 'Selective pre-emergence herbicide (500g/kg Atrazine) for weed control in maize. Controls broadleaf weeds and grasses including couch grass and black jack. Apply within 3 days of planting.'},

    {'cat': 'pesticides-herbicides', 'name': 'Copper Oxychloride Fungicide', 'price': 8500, 'unit': 'per 200 g',
     'img': px(4439460),
     'desc': 'Protective copper-based fungicide for angular leaf spot, anthracnose, coffee berry disease, black sigatoka and downy mildew. Highly effective for all major crop diseases in Uganda.'},

    {'cat': 'pesticides-herbicides', 'name': 'Emamectin Benzoate Caterpillar Control', 'price': 24000, 'unit': 'per 100 ml',
     'img': px(4503277),
     'desc': 'Highly effective (19g/L Emamectin Benzoate) for fall armyworm, stalkborers, caterpillars and leaf miners. Essential for controlling fall armyworm — the most destructive pest of Ugandan maize.'},

    {'cat': 'pesticides-herbicides', 'name': 'Chlorpyrifos Soil Insecticide', 'price': 16000, 'unit': 'per 500 ml',
     'img': px(2737258),
     'desc': 'Organophosphate (480g/L Chlorpyrifos) for soil pests: termites, cutworms, nematodes, ants and beetles. Applied as soil drench or furrow treatment at planting. Protects seedling roots and tubers.'},

    {'cat': 'pesticides-herbicides', 'name': 'Metalaxyl Anti-Downy Mildew Fungicide', 'price': 19500, 'unit': 'per 100 g',
     'img': px(35811576),
     'desc': 'Systemic fungicide (350g/kg Metalaxyl) for downy mildew, late blight, damping-off and Phytophthora. Applied as seed treatment or foliar spray on maize, beans, potato, tomato and vegetables.'},

    {'cat': 'pesticides-herbicides', 'name': 'Neem Organic Pesticide Extract', 'price': 14000, 'unit': 'per 500 ml', 'featured': True,
     'img': px(38191101),
     'desc': '100% organic neem oil (Azadirachtin) — environmentally safe pesticide and fungicide. Controls aphids, mites, whiteflies and mealybugs. Safe for beneficial insects. Available at EGV-certified agro-dealers across Uganda.'},
]


class Command(BaseCommand):
    help = 'Seed Coffee, Fertilizer and Pesticide products'

    def handle(self, *args, **options):
        # Remove old categories that are no longer needed
        old_slugs = ['grains-cereals', 'beans-legumes', 'cash-crops-spices', 'fresh-produce']
        removed = Category.objects.filter(slug__in=old_slugs)
        if removed.exists():
            names = list(removed.values_list('name', flat=True))
            # Remove products first (to avoid FK constraint)
            Product.objects.filter(category__slug__in=old_slugs).delete()
            removed.delete()
            self.stdout.write(f"  Removed old categories: {names}")

        # Seed active categories
        cats = {}
        for c in CATEGORIES:
            obj, created = Category.objects.update_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'description': c['description'], 'order': c['order']}
            )
            cats[c['slug']] = obj
            self.stdout.write(f"  Category: {obj.name} ({'created' if created else 'updated'})")

        # Seed products
        count = 0
        for p in PRODUCTS:
            slug = slugify(p['name'])
            obj, created = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    'category':     cats[p['cat']],
                    'name':         p['name'],
                    'description':  p['desc'],
                    'price_ugx':    p['price'],
                    'unit':         p['unit'],
                    'image_url':    p.get('img', ''),
                    'is_featured':  p.get('featured', False),
                    'is_available': True,
                    'image':        '',
                }
            )
            count += 1
            self.stdout.write(f"  {obj.name} — UGX {obj.price_ugx:,}")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {count} products across {len(CATEGORIES)} categories.'
        ))
