from django.urls import path

from order import views


urlpatterns = [
    path('', views.OrderView.as_view(), name='order'),
]
