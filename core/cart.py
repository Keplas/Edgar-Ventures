from decimal import Decimal
from core.models import Product

CART_KEY = 'egv_cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(CART_KEY, {})

    def add(self, product, qty=1):
        pid = str(product.pk)
        if pid not in self.cart:
            self.cart[pid] = {'qty': 0, 'price': str(product.price_ugx)}
        self.cart[pid]['qty'] += qty
        self.save()

    def remove(self, product):
        pid = str(product.pk)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def update(self, product, qty):
        pid = str(product.pk)
        if pid in self.cart:
            if qty > 0:
                self.cart[pid]['qty'] = qty
            else:
                del self.cart[pid]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[CART_KEY] = {}
        self.session.modified = True

    def __iter__(self):
        pids = self.cart.keys()
        products = Product.objects.filter(pk__in=pids)
        cart = dict(self.cart)
        for product in products:
            item = cart[str(product.pk)]
            item['product']    = product
            item['unit_price'] = Decimal(item['price'])
            item['total']      = Decimal(item['price']) * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def get_total(self):
        return self.get_subtotal() + Decimal('10000')
