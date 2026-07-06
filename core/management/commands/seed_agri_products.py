"""
Run once after first deployment:
  python manage.py seed_agri_products

Images sourced from Pexels (free commercial use, no attribution required)
and matched to local East African / Ugandan market context.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Category, Product

# Pexels image base URL — free, commercial use, no attribution needed
P = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=700&h=500&fit=crop"

def px(photo_id):
    """Return Pexels image URL for a given photo ID."""
    return P.format(id=photo_id)


CATEGORIES = [
    {'name': 'Coffee',                  'slug': 'coffee',                 'description': 'Premium Ugandan coffee beans and ground coffee',       'order': 1},
    {'name': 'Grains & Cereals',        'slug': 'grains-cereals',         'description': 'Maize, rice, millet, sorghum and more',               'order': 2},
    {'name': 'Beans & Legumes',         'slug': 'beans-legumes',          'description': 'Kidney beans, groundnuts, soya and more',              'order': 3},
    {'name': 'Cash Crops & Spices',     'slug': 'cash-crops-spices',      'description': 'Vanilla, sesame, sunflower and spices',                'order': 4},
    {'name': 'Fresh Produce',           'slug': 'fresh-produce',          'description': 'Fresh fruits and vegetables from Ugandan farms',       'order': 5},
    {'name': 'Fertilizers',             'slug': 'fertilizers',            'description': 'NPK, Urea, DAP, organic and foliar fertilizers',       'order': 6},
    {'name': 'Pesticides & Herbicides', 'slug': 'pesticides-herbicides',  'description': 'Insecticides, herbicides and fungicides for crops',    'order': 7},
]

PRODUCTS = [
    # ══ COFFEE ══════════════════════════════════════════════════════════════
    # 669162  = pile of roasted brown coffee beans (Pexels — Lukas Blazek)
    # 1695052 = green raw coffee beans
    # 302899  = dark roasted coffee beans top view
    # 312418  = ground coffee and beans
    # 374885  = coffee in cup, dark background
    # 1002740 = coffee beans filling frame

    {'cat': 'coffee', 'name': 'Arabica Green Coffee Beans', 'price': 8500, 'unit': 'per kg', 'featured': True,
     'img': px(1695052),
     'desc': 'High-altitude Arabica green coffee beans from Mount Elgon and Rwenzori regions. Naturally sun-dried, hand-sorted, and ready for roasting. Flavour notes: bright acidity, floral aroma, hints of berry.'},

    {'cat': 'coffee', 'name': 'Robusta Green Coffee Beans', 'price': 5500, 'unit': 'per kg',
     'img': px(1002740),
     'desc': 'Uganda Robusta green beans from the Lake Victoria region. Known for their bold, full-bodied character and earthy flavour profile. Excellent for espresso blends.'},

    {'cat': 'coffee', 'name': 'Arabica Roasted Coffee Beans', 'price': 18000, 'unit': 'per 500g', 'featured': True,
     'img': px(302899),
     'desc': 'Medium-roast Arabica beans from certified Ugandan farms. Roasted in small batches to preserve complex flavour notes. Ideal for filter, pour-over, or French press brewing.'},

    {'cat': 'coffee', 'name': 'EGV Premium Ground Coffee', 'price': 14000, 'unit': 'per 250g', 'featured': True,
     'img': px(312418),
     'desc': 'Freshly ground Arabica coffee, medium-fine grind suitable for drip coffee makers, French press, and Moka pots. Vacuum-sealed to preserve freshness. A true taste of Uganda in every cup.'},

    {'cat': 'coffee', 'name': 'Instant Arabica Coffee', 'price': 8500, 'unit': 'per 100g',
     'img': px(374885),
     'desc': 'Pure Ugandan Arabica instant coffee — no fillers, no additives. Dissolves instantly in hot water for a rich, aromatic cup. Convenient for travel and office.'},

    {'cat': 'coffee', 'name': 'Coffee Husks (Cascara)', 'price': 4500, 'unit': 'per 200g',
     'img': px(669162),
     'desc': 'Dried coffee cherry skins (cascara) from Arabica processing. Brew as a herbal tea for a sweet, fruity, lightly caffeinated drink. A zero-waste coffee by-product rich in antioxidants.'},

    # ══ GRAINS & CEREALS ════════════════════════════════════════════════════
    # 1508666 = white maize/corn cobs (local market)
    # 4110252 = maize grain pile
    # 6153369 = sorghum grain
    # 4198019 = rice grain
    # 7263396 = millet grain
    # 5419146 = flour/white powder
    # 36470055 = Jinja Central Market Uganda (general market)

    {'cat': 'grains-cereals', 'name': 'White Maize', 'price': 1200, 'unit': 'per kg', 'featured': True,
     'img': px(1508666),
     'desc': 'Clean, dry white maize from Eastern Uganda. Sorted and dried to optimal moisture content. Suitable for milling, animal feed, or direct cooking.'},

    {'cat': 'grains-cereals', 'name': 'Maize Flour Fine Ground', 'price': 5500, 'unit': 'per 2 kg',
     'img': px(5419146),
     'desc': 'Finely milled white maize flour ideal for making posho, porridge, and baked goods. Freshly milled, no additives, packed in food-grade bags.'},

    {'cat': 'grains-cereals', 'name': 'Sorghum Grain', 'price': 1800, 'unit': 'per kg',
     'img': px(6153369),
     'desc': 'Drought-resistant sorghum grain from Northern Uganda. Gluten-free, high in fibre and rich in antioxidants. Used for porridge, local brew, and animal feed.'},

    {'cat': 'grains-cereals', 'name': 'Brown Rice Local', 'price': 4500, 'unit': 'per kg',
     'img': px(4198019),
     'desc': 'Locally grown brown rice from the Doho Rice Irrigation Scheme, Eastern Uganda. Unpolished, nutty flavour, higher fibre and nutrition than white rice.'},

    {'cat': 'grains-cereals', 'name': 'Finger Millet (Eleusine)', 'price': 2800, 'unit': 'per kg',
     'img': px(7263396),
     'desc': 'Finger millet from the Rwenzori foothills — rich in calcium and iron. Used for porridge, bread flour, and traditional fermented drinks.'},

    {'cat': 'grains-cereals', 'name': 'Cassava Flour', 'price': 4800, 'unit': 'per 2 kg',
     'img': px(4110252),
     'desc': 'Sun-dried and finely milled cassava flour from Central Uganda. Gluten-free alternative for baking, thickening sauces, and making traditional cassava dishes.'},

    # ══ BEANS & LEGUMES ═════════════════════════════════════════════════════
    # 6294337 = red kidney beans close-up (local market)
    # 7657292 = dry beans in sack (African market)
    # 3735221 = groundnuts/peanuts in hands
    # 1656663 = mixed beans
    # 4911714 = soyabeans
    # 8892419 = green mung beans/green grams

    {'cat': 'beans-legumes', 'name': 'Kidney Beans Dark Red', 'price': 5000, 'unit': 'per kg', 'featured': True,
     'img': px(6294337),
     'desc': 'Large dark red kidney beans from Eastern Uganda. Hand-sorted, clean, and dry. High in protein and fibre — ideal for stews, rice dishes, and soups.'},

    {'cat': 'beans-legumes', 'name': 'White Beans (Nambale)', 'price': 4500, 'unit': 'per kg',
     'img': px(1656663),
     'desc': 'Small white Nambale beans — a Ugandan staple. Clean, sorted, and dry. Perfect for traditional bean stew, soups, or mixed rice dishes.'},

    {'cat': 'beans-legumes', 'name': 'Soyabeans', 'price': 3500, 'unit': 'per kg',
     'img': px(4911714),
     'desc': 'Yellow soyabeans from Northern Uganda. Versatile protein source for human consumption and livestock feed.'},

    {'cat': 'beans-legumes', 'name': 'Groundnuts / Peanuts Raw', 'price': 6500, 'unit': 'per kg', 'featured': True,
     'img': px(3735221),
     'desc': 'Freshly harvested raw groundnuts from Lira and Soroti districts. Unsalted, unroasted. Used for groundnut paste, roasting, or pressing for oil.'},

    {'cat': 'beans-legumes', 'name': 'Green Grams (Mung Beans)', 'price': 5500, 'unit': 'per kg',
     'img': px(8892419),
     'desc': 'Green grams from Eastern Uganda. Quick-cooking, high-protein legume excellent for soups, salads, stews, and sprouting.'},

    # ══ CASH CROPS & SPICES ═════════════════════════════════════════════════
    # 4198705 = vanilla pods (dark background, luxury feel)
    # 2802527 = sesame seeds
    # 5765 = sunflower / seeds
    # 4022184 = dried chili peppers (red)
    # 1340116 = turmeric powder

    {'cat': 'cash-crops-spices', 'name': 'Vanilla Beans Grade A', 'price': 48000, 'unit': 'per 50g (approx 5 pods)', 'featured': True,
     'img': px(4198705),
     'desc': 'Premium Grade A vanilla pods from West Uganda. Long, plump, moist beans with intense vanilla fragrance. Perfect for baking, ice cream, and extracts.'},

    {'cat': 'cash-crops-spices', 'name': 'Simsim / Sesame Seeds', 'price': 7500, 'unit': 'per kg',
     'img': px(2802527),
     'desc': 'White sesame seeds from Northern Uganda. Hulled, clean, and dried. Used for cooking oil, tahini, baking, and nutritional supplements.'},

    {'cat': 'cash-crops-spices', 'name': 'Sunflower Seeds Oil Variety', 'price': 4500, 'unit': 'per kg',
     'img': px(5765),
     'desc': 'High-oil content sunflower seeds from Eastern Uganda. Suitable for pressing into cooking oil, roasting as a snack, or processing into sunflower flour.'},

    {'cat': 'cash-crops-spices', 'name': 'Dried Chili Peppers', 'price': 4000, 'unit': 'per 100g',
     'img': px(4022184),
     'desc': 'Sun-dried hot chili peppers from Nakaseke. Intense heat with smoky undertones. Grind for chili powder or use whole in stews.'},

    {'cat': 'cash-crops-spices', 'name': 'Turmeric Root Dried and Ground', 'price': 6000, 'unit': 'per 100g',
     'img': px(1340116),
     'desc': 'Freshly dried and ground turmeric from Central Uganda. Deep orange colour, earthy aroma, and high curcumin content. Used in cooking, natural remedies, and health drinks.'},

    # ══ FRESH PRODUCE ═══════════════════════════════════════════════════════
    # 35811589 = Workers unloading bananas from truck (Uganda, Pexels kderrick049)
    # 7027604  = banana tree in Uganda (Pexels ushindinamegabe)
    # 38191101 = Kampala market stall with red apron (Pexels senyonga)
    # 35811576 = African woman vendor with vegetables in bucket (Uganda)
    # 36470055 = Jinja Central Market bustling scene (Uganda, Pexels ana-kenk)
    # 2894019  = pineapple top-down
    # 1132047  = passion fruit
    # 2286776  = sweet potatoes

    {'cat': 'fresh-produce', 'name': 'Fresh Pineapple', 'price': 3500, 'unit': 'per piece', 'featured': True,
     'img': px(2894019),
     'desc': "Sweet, juicy Ugandan pineapples from Kayunga district — among the world's finest for their unique sugar content and low acidity. Typically 1–1.5 kg each."},

    {'cat': 'fresh-produce', 'name': 'Passion Fruit', 'price': 4500, 'unit': 'per kg (approx 8-10 fruits)',
     'img': px(1132047),
     'desc': 'Ripe yellow and purple passion fruits from Western Uganda highlands. Intensely aromatic with sweet-tart pulp. Excellent for fresh juice, yoghurt, desserts, and smoothies.'},

    {'cat': 'fresh-produce', 'name': 'Sweet Potatoes', 'price': 1500, 'unit': 'per kg',
     'img': px(2286776),
     'desc': 'Orange-fleshed sweet potatoes from Apac district — rich in beta-carotene, vitamin A, and fibre. Can be boiled, roasted, fried, or mashed.'},

    {'cat': 'fresh-produce', 'name': 'Ripe Matooke Banana Bunch', 'price': 8000, 'unit': 'per bunch (3-4 kg)',
     'img': px(35811589),
     'desc': 'East African Highland Bananas (Matooke) from Mbarara — workers unloading fresh bunches straight off the farm truck. Starchy, filling, and versatile. Boil, steam, or fry.'},

    # ══ FERTILIZERS ═════════════════════════════════════════════════════════
    # 28101456 = Farmers tending crops in Kitgum Uganda (Pexels illustrate-digital-ug)
    # 36185282 = Hands holding seedling in nursery Uganda
    # 36185281 = Hands planting sapling Uganda
    # 28101457 = Elderly woman farming in Ugandan field
    # 1090977  = farm soil / earth
    # 6280298  = plant growing from soil (fertilizer concept)
    # 1084584  = green leaves / plant nutrition
    # 5473960  = fertilizer granules (generic)
    # 3094208  = green field agriculture
    # 1382102  = soil/compost
    # 2132250  = farm field crop rows
    # 28100859 = man in crop field Northern Uganda

    {'cat': 'fertilizers', 'name': 'NPK 17-17-17 Compound Fertilizer', 'price': 145000, 'unit': 'per 50 kg bag', 'featured': True,
     'img': px(28101456),
     'desc': 'Balanced NPK fertilizer (17-17-17). Ideal at planting and top-dressing for maize, beans, coffee and vegetables. The most popular all-purpose fertilizer for Ugandan smallholder farmers.'},

    {'cat': 'fertilizers', 'name': 'Urea Fertilizer 46% Nitrogen', 'price': 125000, 'unit': 'per 50 kg bag', 'featured': True,
     'img': px(28100859),
     'desc': 'High-nitrogen urea (46-0-0). Best as top-dressing for maize, sorghum, rice and pasture grasses. Rapidly boosts leafy growth and green colour across Ugandan croplands.'},

    {'cat': 'fertilizers', 'name': 'DAP Diammonium Phosphate', 'price': 165000, 'unit': 'per 50 kg bag', 'featured': True,
     'img': px(36185282),
     'desc': 'DAP (18-46-0) — the most widely used phosphorus fertilizer in East Africa. Applied at planting to promote strong roots, early establishment and improved flowering.'},

    {'cat': 'fertilizers', 'name': 'CAN Calcium Ammonium Nitrate', 'price': 115000, 'unit': 'per 50 kg bag',
     'img': px(3094208),
     'desc': 'CAN (27% N) combines fast-acting nitrate with slower ammonium nitrogen plus calcium. Less volatile than urea — ideal for acidic Ugandan soils. Suitable for maize, vegetables and cereals.'},

    {'cat': 'fertilizers', 'name': 'Organic Compost Manure', 'price': 35000, 'unit': 'per 50 kg bag',
     'img': px(1382102),
     'desc': 'Fully composted organic manure from animal waste and crop residues. Improves soil structure, moisture retention and microbial activity. Safe for all crops. Ideal for organic farming.'},

    {'cat': 'fertilizers', 'name': 'Foliar Liquid Micronutrient Fertilizer', 'price': 28000, 'unit': 'per 1 litre',
     'img': px(1084584),
     'desc': 'Complete liquid foliar feed with NPK plus Zinc, Boron, Iron, Magnesium and Manganese. Applied directly to leaves for fast absorption. Corrects nutrient deficiencies rapidly on all crops.'},

    {'cat': 'fertilizers', 'name': 'Muriate of Potash MOP 60%', 'price': 88000, 'unit': 'per 25 kg bag',
     'img': px(2132250),
     'desc': 'MOP (0-0-60) high-potassium fertilizer that improves drought resistance, fruit quality and disease resistance. Recommended for banana, potato, tomato, passion fruit and fruiting crops.'},

    {'cat': 'fertilizers', 'name': 'Single Super Phosphate SSP', 'price': 72000, 'unit': 'per 50 kg bag',
     'img': px(6280298),
     'desc': 'SSP (0-18-0) enriched with Sulphur and Calcium. Promotes strong root formation, seed germination and early establishment. Cost-effective phosphate source for Ugandan soils.'},

    {'cat': 'fertilizers', 'name': 'Chicken Manure Pellets Organic', 'price': 42000, 'unit': 'per 50 kg bag',
     'img': px(1090977),
     'desc': 'Processed and pelletised chicken manure — odour-controlled, pathogen-free and nutrient-rich. Slow-release feeding over several months. Excellent for vegetable gardens and fruit trees.'},

    {'cat': 'fertilizers', 'name': 'Zinc Sulphate Micronutrient', 'price': 18000, 'unit': 'per 1 kg',
     'img': px(36185281),
     'desc': 'Zinc Sulphate (21% Zn) corrects zinc deficiency — one of the most common micronutrient problems in Ugandan maize. Apply as soil drench or foliar spray.'},

    # ══ PESTICIDES & HERBICIDES ═════════════════════════════════════════════
    # 36390057 = outdoor grocery stall with bottles (local agro-shop Uganda)
    # 38191101 = Kampala market stall woman (local supply context)
    # 35811576 = African vendor outdoors (local market)
    # 28101470 = children with baskets in Uganda field
    # 3680956  = hand spraying plant (pesticide application)
    # 4503277  = herbicide sprayer in field
    # 4439460  = crop protection / field spraying
    # 5748809  = weed in field (herbicide target)
    # 4022183  = chemical bottles/containers
    # 2737258  = tractor spraying field
    # 1537570  = plant disease / fungus on leaves

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
     'desc': 'Cold-pressed neem oil (Azadirachtin) — 100% organic, environmentally safe pesticide and fungicide. Controls aphids, mites, whiteflies and mealybugs. Safe for beneficial insects. Available at EGV-certified agro-dealers across Uganda.'},
]


class Command(BaseCommand):
    help = 'Seed agriculture products with local-market Pexels images'

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
                    'category':     cats[p['cat']],
                    'name':         p['name'],
                    'description':  p['desc'],
                    'price_ugx':    p['price'],
                    'unit':         p['unit'],
                    'image_url':    p.get('img', ''),
                    'is_featured':  p.get('featured', False),
                    'is_available': True,
                    'image':        '',   # cleared so Cloudinary auto-upload re-runs
                }
            )
            count += 1
            self.stdout.write(f"  {obj.name} — UGX {obj.price_ugx:,}")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {count} products seeded across {len(CATEGORIES)} categories.'
            f'\nImages sourced from Pexels (free, local East African market context).'
        ))
