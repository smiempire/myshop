from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import logout as django_logout, login

from core.helpers import json_response, get_client_ip
from shop.cart import Cart
from shop.forms import CartAddProductForm, ProfileForm, SigninForm, SignupForm
from shop.models import Product, UserProfile, Category


# ============================================= Shop ============================================== #

class HomepageView(generic.ListView):
    template_name = 'index.html'
    queryset = Product.objects.available().order_by('-created')[:6]

    def get_context_data(self, **kwargs):
        context_data = super(HomepageView, self).get_context_data(**kwargs)
        context_data['meta_title'] = 'Shop'
        context_data['best_products'] = Product.objects.available().order_by('-views')[:6]
        return context_data


class CategoryView(generic.DetailView):
    template_name = 'category.html'
    model = Category

    def get_context_data(self, **kwargs):
        context_data = super(CategoryView, self).get_context_data(**kwargs)
        context_data['meta_title'] = self.object.name
        context_data['object_list'] = self.object.category_product.available()
        return context_data


class SearchView(generic.ListView):
    template_name = 'search.html'
    paginate_by = 30

    def get_queryset(self):
        q = self.request.POST.get('q', '')
        products = Product.objects.available().filter(name__icontains=q)
        category_slug = self.request.POST.get('category', '')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return products

    def get_context_data(self, **kwargs):
        context_data = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.POST.get('q', '')
        context_data['q'] = q
        context_data['meta_title'] = 'Продукты по запросу ' + q
        return context_data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ProductView(generic.DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context_data = super(ProductView, self).get_context_data(**kwargs)
        context_data['related_products'] = Product.objects.available().filter(
            category=self.object.category.first()).exclude(id=self.object.id)
        context_data['cart_product_form'] = CartAddProductForm()
        return context_data


class CartView(generic.TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context_data = super(CartView, self).get_context_data(**kwargs)
        context_data['cart'] = Cart(self.request)
        return context_data


@require_POST
@csrf_exempt
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, quantity=cd['quantity'], update_quantity=cd['update']
        )
    return redirect('cart_detail')


@require_POST
@csrf_exempt
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

# ============================================= /Shop ============================================== #


# ============================================ Profile ============================================= #

class ProfileView(LoginRequiredMixin, generic.ListView):
    queryset = []
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context_data = super(ProfileView, self).get_context_data(**kwargs)
        context_data['message'] = self.kwargs.get('message', '')
        context_data['meta_title'] = 'Мой профиль'
        context_data['form'] = ProfileForm(instance=self.request.user.userprofile)
        return context_data

    def post(self, request, *args, **kwargs):
        u = get_object_or_404(UserProfile, django_user=request.user)
        if 'old_password' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                message = 'Изменения сохранены'
            else:
                message = '<br>'.join([form.fields[k].label + ': ' + v[0] for k, v in form.errors.items()])
        else:
            form = ProfileForm(request.POST, request.FILES, instance=u)
            if form.is_valid():
                user_profile = form.save()
                user = user_profile.django_user
                user.email = request.POST.get('email')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.save()
                self.request.user = user
                message = 'Изменения сохранены'
            else:
                message = '<br>'.join([form.fields[k].label + ': ' + v[0] for k, v in form.errors.items()])
        self.kwargs['message'] = message
        return self.get(request, *args, **kwargs)


class SigninView(generic.FormView):
    form_class = SigninForm
    success_url = "/"
    template_name = 'profile/signin.html'

    def get_context_data(self, **kwargs):
        context_data = super(SigninView, self).get_context_data(**kwargs)
        context_data['path'] = self.request.META.get('HTTP_REFERER', '/')
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.success_url = self.request.POST.get("next", "/")
        self.user = form.get_user()
        login(self.request, self.user, backend='django.contrib.auth.backends.ModelBackend')
        return json_response({'success': True, 'url': self.success_url})

    def form_invalid(self, form):
        return json_response({
            'success': False,
            'errors': '<br>'.join([v[0] for k, v in form.errors.items()])
        })


class SignupView(generic.FormView):
    form_class = SignupForm
    success_url = "/"
    template_name = 'profile/signup.html'

    def get_context_data(self, **kwargs):
        context_data = super(SignupView, self).get_context_data(**kwargs)
        context_data['path'] = self.request.META.get('HTTP_REFERER', '/')
        return context_data

    def post(self, request, *args, **kwargs):
        form = SignupForm({
            "username": request.POST.get('email'),
            "email": request.POST.get('email'),
            "password1": request.POST.get('password1'),
            "password2": request.POST.get('password2'),
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name'),
        })
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.success_url = self.request.POST.get("next", "/")
        self.user = form.save()
        if self.user:
            user_profile = UserProfile(
                django_user=self.user,
                ip=get_client_ip(self.request),
            )
            user_profile.save()
            login(self.request, self.user, backend='django.contrib.auth.backends.ModelBackend')
        return json_response({'success': True, 'url': self.success_url})

    def form_invalid(self, form):
        return json_response({
            'success': False,
            'errors': '<br>'.join([v[0] for k, v in form.errors.items()])
        })


class LogoutView(generic.View):

    def get(self, request):
        django_logout(request)
        return HttpResponseRedirect(request.GET.get('next', '/'))


class ProfileOrdersView(LoginRequiredMixin, generic.ListView):
    queryset = []
    template_name = 'profile/orders.html'

    def get_context_data(self, **kwargs):
        context_data = super(ProfileOrdersView, self).get_context_data(**kwargs)
        context_data['orders'] = self.request.user.order_set.all()
        return context_data

# ============================================ /Profile ============================================= #
