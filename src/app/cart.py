from django.conf import settings
from app.models import Product, Order


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, cnt=1, update_cnt=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'cnt': 0,
                                     'cost': str(product.cost)}
        if update_cnt:
            self.cart[product_id]['cnt'] = cnt
        else:
            self.cart[product_id]['cnt'] += cnt
        self.save()

    def remove(self, product):
        self.cart.pop(product)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def reduce_amount(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['cnt'] == 1:
                del self.cart[product_id]
            else:
                self.cart[product_id]['cnt'] -= 1
            self.save()

    def increase_amount(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['cnt'] += 1
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['cost'] = float(item['cost'])
            item['total_cost'] = item['cost'] * item['cnt']
            yield item

    def __len__(self):
        return sum(item['cnt'] for item in self.cart.values())

    def get_total_cost(self):
        return sum(float(item['cost']) * item['cnt'] for item in
                   self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
