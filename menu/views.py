from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Dish

def home(request):
    return render(request, "menu/home.html", {
        "categories": Category.objects.all(),
    })

def menu_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    dishes = Dish.objects.filter(category=category)

    return render(request, "menu/category.html", {
        "category": category,
        "dishes": dishes,
        "categories": Category.objects.all(),
    })


def add_to_cart(request, dish_id):
    cart = request.session.get("cart", {})

    # +1 товар
    cart[dish_id] = cart.get(dish_id, 0) + 1

    request.session["cart"] = cart
    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})

    items = []
    total = 0

    for dish_id, qty in cart.items():
        dish = Dish.objects.get(id=dish_id)
        subtotal = dish.price * qty
        items.append({
            "dish": dish,
            "qty": qty,
            "subtotal": subtotal,
        })
        total += subtotal

    return render(request, "menu/cart.html", {
        "items": items,
        "total": total,
        "categories": Category.objects.all(),
    })


def checkout(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")


        request.session["cart"] = {}

        return render(request, "menu/success.html", {
            "name": name
        })

    return render(request, "menu/checkout.html", {
        "categories": Category.objects.all(),
    })