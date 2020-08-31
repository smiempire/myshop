from django.urls import path, re_path
from django.contrib.auth.views import (PasswordResetConfirmView, PasswordResetDoneView,
                                       PasswordResetCompleteView, PasswordResetView)
from django.views.decorators.csrf import csrf_exempt

from shop import views


urlpatterns = [
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/password/reset/', PasswordResetView.as_view(), name="password_reset"),
    path('user/password/reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('user/password/reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/orders/', views.ProfileOrdersView.as_view(), name='profile_orders'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('search/', csrf_exempt(views.SearchView.as_view()), name='search'),
    path('cart/', views.CartView.as_view(), name='cart_detail'),
    path('cart-add/<int:product_id>)/', views.cart_add, name='cart_add'),
    path('cart-remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product'),
    path('', views.HomepageView.as_view(), name='index'),
]
