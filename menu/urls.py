from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<int:id>/', views.category_view, name='category'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('menu/', views.menu_page, name='menu'),
]