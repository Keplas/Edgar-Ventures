from decimal import Decimal
from .models import Product


class Cart:
    """Session-backed shopping cart."""

    DELIVERY_FEE = Decimal('10000')   # UGX 10,000 flat delivery

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault('agri_cart', {})

    # ── Mutators ──────────────────────────────────────────────
    def add(self, product: Product, quantity: int = 1, override: bool = False):
        pid = str(product.pk)
        if pid not in self.cart:
            self.cart[pid] = {'quantity': 0, 'price': str(product.price_ugx),
                              'name': product.name, 'unit': product.unit}
        if override:
            self.cart[pid]['quantity'] = quantity
        else:
            self.cart[pid]['quantity'] += quantity
        if self.cart[pid]['quantity'] <= 0:
            self.remove_by_id(pid)
        self._save()

    def remove(self, product: Product):
        self.remove_by_id(str(product.pk))

    def remove_by_id(self, pid: str):
        if pid in self.cart:
            del self.cart[pid]
            self._save()

    def clear(self):
        self.session['agri_cart'] = {}
        self._save()

    def _save(self):
        self.session.modified = True

    # ── Iteration ─────────────────────────────────────────────
    def __iter__(self):
        pids     = self.cart.keys()
        products = {str(p.pk): p for p in Product.objects.filter(pk__in=pids)}
        for pid, data in self.cart.items():
            product    = products.get(pid)
            unit_price = Decimal(data['price'])
            qty        = data['quantity']
            yield {
                'product':    product,
                'pid':        pid,
                'name':       data['name'],
                'unit':       data['unit'],
                'quantity':   qty,
                'unit_price': unit_price,
                'line_total': unit_price * qty,
                'fmt_price':  f"UGX {int(unit_price):,}",
                'fmt_total':  f"UGX {int(unit_price * qty):,}",
            }

    def __len__(self):
        return sum(d['quantity'] for d in self.cart.values())

    # ── Totals ────────────────────────────────────────────────
    def subtotal(self) -> Decimal:
        return sum(Decimal(d['price']) * d['quantity'] for d in self.cart.values())

    def total(self) -> Decimal:
        return self.subtotal() + self.DELIVERY_FEE if self.cart else Decimal('0')

    def fmt_subtotal(self): return f"UGX {int(self.subtotal()):,}"
    def fmt_delivery(self): return f"UGX {int(self.DELIVERY_FEE):,}"
    def fmt_total(self):    return f"UGX {int(self.total()):,}"
