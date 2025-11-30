from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<int:category_id>/", views.menu_by_category, name="menu_by_category"),
    path("cart/", views.cart_view, name="cart"),
    path("add/<int:dish_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
]
