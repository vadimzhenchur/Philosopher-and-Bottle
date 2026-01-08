from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Dish, Order
from decimal import Decimal


def index(request):
    categories = Category.objects.all()
    dishes = Dish.objects.all()[:8]  # популярні страви

    return render(request, 'menu/index.html', {
        'categories': categories,
        'products': dishes,   # ВАЖЛИВО: для головної
    })


def category_view(request, id):
    category = get_object_or_404(Category, id=id)
    categories = Category.objects.all()
    dishes = Dish.objects.filter(category=category)

    return render(request, 'menu/category.html', {
        'category': category,
        'categories': categories,
        'dishes': dishes,
    })


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0')

    for key, item in cart.items():
        price = Decimal(item['price'])
        qty = item['qty']
        subtotal = price * qty
        total += subtotal
        items.append({
            'title': item['title'],
            'price': price,
            'qty': qty,
            'subtotal': subtotal,
        })

    return render(request, 'menu/cart.html', {
        'items': items,
        'total': total
    })


def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = request.session.get('cart', {})

    if str(dish.id) in cart:
        cart[str(dish.id)]['qty'] += 1
    else:
        cart[str(dish.id)] = {
            'title': dish.title,
            'price': str(dish.price),
            'qty': 1
        }

    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    return render(request, 'menu/checkout.html')