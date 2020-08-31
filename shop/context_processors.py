from shop.cart import Cart
from shop.models import Category


def main_data(request):
    return {
        "categories": Category.objects.all(),
        'cart': Cart(request)
    }
