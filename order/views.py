from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic

from order.forms import OrderCreateForm
from order.models import OrderItem
from shop.cart import Cart


class OrderView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'order.html'
    login_url = '/signup/'

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if cart:
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                cart.clear()
                return redirect('profile_orders')
        return self.get(request, *args, **kwargs)
