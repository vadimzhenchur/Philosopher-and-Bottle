from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success_page, name='success'),
    path('reviews/', views.reviews_page, name='reviews'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
]