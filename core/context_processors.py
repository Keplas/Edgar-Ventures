def cart_count(request):
    cart = request.session.get('agri_cart', {})
    count = sum(v.get('quantity', 0) for v in cart.values())
    return {'cart_item_count': count}
