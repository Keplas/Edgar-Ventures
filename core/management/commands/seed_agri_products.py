from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Category, Product

P = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=700&h=500&fit=crop"
def px(i): return P.format(id=i)

CATEGORIES = [
    {'name':'Coffee','slug':'coffee','description':'Premium Ugandan coffee','order':1},
    {'name':'Fertilizers','slug':'fertilizers','description':'NPK, Urea, DAP and organic fertilizers','order':2},
    {'name':'Pesticides & Herbicides','slug':'pesticides-herbicides','description':'Insecticides, herbicides, fungicides','order':3},
]
PRODUCTS = [
    {'cat':'coffee','name':'Arabica Green Coffee Beans','price':8500,'unit':'per kg','featured':True,'img':px(1695052),'desc':'High-altitude Arabica green coffee beans from Mount Elgon and Rwenzori. Naturally sun-dried, hand-sorted, ready for roasting. Flavour notes: bright acidity, floral aroma, hints of berry.'},
    {'cat':'coffee','name':'Robusta Green Coffee Beans','price':5500,'unit':'per kg','img':px(1002740),'desc':'Uganda Robusta green beans from the Lake Victoria region. Bold, full-bodied character and earthy flavour. Excellent for espresso blends.'},
    {'cat':'coffee','name':'Arabica Roasted Coffee Beans','price':18000,'unit':'per 500g','featured':True,'img':px(302899),'desc':'Medium-roast Arabica beans from certified Ugandan farms. Roasted in small batches for complex flavour. Ideal for filter, pour-over or French press.'},
    {'cat':'coffee','name':'EGV Premium Ground Coffee','price':14000,'unit':'per 250g','featured':True,'img':px(312418),'desc':'Freshly ground Arabica coffee, medium-fine grind. Vacuum-sealed for freshness. Suitable for drip coffee makers, French press and Moka pots.'},
    {'cat':'coffee','name':'Instant Arabica Coffee','price':8500,'unit':'per 100g','img':px(374885),'desc':'Pure Ugandan Arabica instant coffee — no fillers or additives. Dissolves instantly for a rich aromatic cup. Ideal for travel and office.'},
    {'cat':'coffee','name':'Coffee Husks (Cascara)','price':4500,'unit':'per 200g','img':px(669162),'desc':'Dried coffee cherry skins from Arabica processing. Brew as herbal tea for a sweet, fruity, lightly caffeinated drink. Rich in antioxidants.'},
    {'cat':'fertilizers','name':'NPK 17-17-17 Compound Fertilizer','price':145000,'unit':'per 50 kg bag','featured':True,'img':px(28101456),'desc':'Balanced NPK (17-17-17) for general crop nutrition. Ideal at planting and top-dressing for maize, beans, coffee and vegetables.'},
    {'cat':'fertilizers','name':'Urea Fertilizer 46% Nitrogen','price':125000,'unit':'per 50 kg bag','featured':True,'img':px(28100859),'desc':'High-nitrogen urea (46-0-0). Best as top-dressing for maize, sorghum, rice and grasses. Rapidly boosts leafy growth and green colour.'},
    {'cat':'fertilizers','name':'DAP Diammonium Phosphate','price':165000,'unit':'per 50 kg bag','featured':True,'img':px(36185282),'desc':'DAP (18-46-0) — most widely used phosphorus fertilizer in East Africa. Promotes strong roots and early establishment.'},
    {'cat':'fertilizers','name':'CAN Calcium Ammonium Nitrate','price':115000,'unit':'per 50 kg bag','img':px(3094208),'desc':'CAN (27% N) combines nitrate with ammonium nitrogen plus calcium. Ideal for acidic Ugandan soils and most cereals and vegetables.'},
    {'cat':'fertilizers','name':'Organic Compost Manure','price':35000,'unit':'per 50 kg bag','img':px(1382102),'desc':'Fully composted organic manure. Improves soil structure, moisture retention and microbial activity. Safe for all crops.'},
    {'cat':'fertilizers','name':'Foliar Liquid Micronutrient Fertilizer','price':28000,'unit':'per 1 litre','img':px(1084584),'desc':'Complete liquid foliar feed with NPK plus Zinc, Boron, Iron and Magnesium. Applied directly to leaves for fast absorption.'},
    {'cat':'fertilizers','name':'Muriate of Potash MOP 60%','price':88000,'unit':'per 25 kg bag','img':px(2132250),'desc':'MOP (0-0-60) high-potassium fertilizer. Improves drought resistance and fruit quality on banana, potato, tomato and passion fruit.'},
    {'cat':'fertilizers','name':'Single Super Phosphate SSP','price':72000,'unit':'per 50 kg bag','img':px(6280298),'desc':'SSP (0-18-0) with Sulphur and Calcium. Promotes root formation and early establishment. Cost-effective for sulphur-deficient soils.'},
    {'cat':'fertilizers','name':'Chicken Manure Pellets Organic','price':42000,'unit':'per 50 kg bag','img':px(1090977),'desc':'Processed pelletised chicken manure — odour-controlled, pathogen-free. Slow-release feeding for vegetable gardens and fruit trees.'},
    {'cat':'fertilizers','name':'Zinc Sulphate Micronutrient','price':18000,'unit':'per 1 kg','img':px(36185281),'desc':'Zinc Sulphate (21% Zn) corrects zinc deficiency in Ugandan maize. Apply as soil drench or foliar spray.'},
    {'cat':'pesticides-herbicides','name':'Glyphosate 480 Herbicide','price':18500,'unit':'per 1 litre','featured':True,'img':px(36390057),'desc':'Systemic non-selective herbicide (480g/L) controlling annual and perennial weeds. For maize, beans, coffee, banana and non-crop areas.'},
    {'cat':'pesticides-herbicides','name':'Lambda Cyhalothrin Insecticide','price':12000,'unit':'per 100 ml','featured':True,'img':px(3680956),'desc':'Fast-acting pyrethroid (50g/L) controlling aphids, stalkborers, bollworms, whiteflies and caterpillars on maize, beans and coffee.'},
    {'cat':'pesticides-herbicides','name':'Mancozeb 80% Fungicide','price':9500,'unit':'per 200 g','img':px(1537570),'desc':'Broad-spectrum fungicide (800g/kg) for blight, leaf spot, anthracnose, rust and downy mildew. Apply every 7-14 days in wet season.'},
    {'cat':'pesticides-herbicides','name':'Imidacloprid Systemic Insecticide','price':22000,'unit':'per 100 ml','img':px(4022183),'desc':'Systemic neonicotinoid (200g/L) for long-lasting protection against aphids, whiteflies, thrips and leafhoppers.'},
    {'cat':'pesticides-herbicides','name':'Atrazine 50% Maize Herbicide','price':14000,'unit':'per 500 g','img':px(5748809),'desc':'Selective pre-emergence herbicide (500g/kg) for weed control in maize. Apply within 3 days of planting.'},
    {'cat':'pesticides-herbicides','name':'Copper Oxychloride Fungicide','price':8500,'unit':'per 200 g','img':px(4439460),'desc':'Protective copper-based fungicide for angular leaf spot, anthracnose, coffee berry disease, black sigatoka and downy mildew.'},
    {'cat':'pesticides-herbicides','name':'Emamectin Benzoate Caterpillar Control','price':24000,'unit':'per 100 ml','img':px(4503277),'desc':'Highly effective (19g/L) for fall armyworm, stalkborers and caterpillars. Essential for controlling fall armyworm on Ugandan maize.'},
    {'cat':'pesticides-herbicides','name':'Chlorpyrifos Soil Insecticide','price':16000,'unit':'per 500 ml','img':px(2737258),'desc':'Organophosphate (480g/L) for soil pests: termites, cutworms, nematodes and ants. Applied as soil drench or furrow treatment.'},
    {'cat':'pesticides-herbicides','name':'Metalaxyl Anti-Downy Mildew Fungicide','price':19500,'unit':'per 100 g','img':px(35811576),'desc':'Systemic fungicide (350g/kg) for downy mildew, late blight and Phytophthora. Applied as seed treatment or foliar spray.'},
    {'cat':'pesticides-herbicides','name':'Neem Organic Pesticide Extract','price':14000,'unit':'per 500 ml','featured':True,'img':px(38191101),'desc':'100% organic neem oil (Azadirachtin). Environmentally safe for aphids, mites, whiteflies and mealybugs. Safe for beneficial insects.'},
]

class Command(BaseCommand):
    help = 'Seed Coffee, Fertilizers and Pesticides products'
    def handle(self, *args, **options):
        old = ['grains-cereals','beans-legumes','cash-crops-spices','fresh-produce']
        from core.models import Category as C, Product as Pr
        removed = C.objects.filter(slug__in=old)
        if removed.exists():
            Pr.objects.filter(category__slug__in=old).delete()
            names = list(removed.values_list('name',flat=True))
            removed.delete()
            self.stdout.write(f'  Removed: {names}')
        cats = {}
        for c in CATEGORIES:
            obj,_ = C.objects.update_or_create(slug=c['slug'], defaults={k:v for k,v in c.items() if k!='slug'})
            cats[c['slug']] = obj
            self.stdout.write(f'  Category: {obj.name}')
        for p in PRODUCTS:
            Pr.objects.update_or_create(slug=slugify(p['name']), defaults={
                'category':cats[p['cat']],'name':p['name'],'description':p['desc'],
                'price_ugx':p['price'],'unit':p['unit'],'image_url':p.get('img',''),
                'is_featured':p.get('featured',False),'is_available':True,'image':'',
            })
            self.stdout.write(f'  {p["name"]}')
        self.stdout.write(self.style.SUCCESS(f'\nDone. {len(PRODUCTS)} products across {len(CATEGORIES)} categories.'))
