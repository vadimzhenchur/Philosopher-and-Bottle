from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Dish, Order, OrderItem
from decimal import Decimal


# ---------- ГОЛОВНА ----------
def index(request):
    categories = Category.objects.all()
    dishes = Dish.objects.all()[:8]  # популярні

    return render(request, 'menu/index.html', {
        'categories': categories,
        'dishes': dishes,
    })


# ---------- МЕНЮ (ВСЕ) ----------
def menu_page(request):
    categories = Category.objects.all()
    dishes = Dish.objects.all()

    return render(request, 'menu/menu.html', {
        'categories': categories,
        'dishes': dishes,
    })


# ---------- КАТЕГОРІЯ ----------
def category_view(request, id):
    category = get_object_or_404(Category, id=id)
    categories = Category.objects.all()
    dishes = Dish.objects.filter(category=category)

    return render(request, 'menu/category.html', {
        'category': category,
        'categories': categories,
        'dishes': dishes,
    })


# ---------- ДОДАТИ В КОШИК ----------
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = request.session.get('cart', {})

    dish_id = str(dish.id)

    if dish_id in cart:
        cart[dish_id]['qty'] += 1
    else:
        cart[dish_id] = {
            'title': dish.title,
            'price': str(dish.price),
            'qty': 1
        }

    request.session['cart'] = cart
    return redirect('cart')


# ---------- КОШИК ----------
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0')

    for dish_id, item in cart.items():
        price = Decimal(item['price'])
        qty = item['qty']
        subtotal = price * qty
        total += subtotal

        items.append({
            'id': dish_id,
            'title': item['title'],
            'price': price,
            'qty': qty,
            'subtotal': subtotal,
        })

    return render(request, 'menu/cart.html', {
        'items': items,
        'total': total,
    })


# ---------- ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ----------
def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0')

    for dish_id, item in cart.items():
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

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total=total
        )

        request.session['cart'] = {}
        return redirect('cart')

    return render(request, 'menu/checkout.html', {
        'items': items,
        'total': total
    })