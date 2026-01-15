from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Dish, Order, OrderItem, Review
from decimal import Decimal


def index(request):
    categories = Category.objects.all()
    dishes = Dish.objects.all()[:8]

    return render(request, 'menu/index.html', {
        'categories': categories,
        'products': dishes,
    })


def menu_page(request):
    categories = Category.objects.all()
    dishes = Dish.objects.all()

    return render(request, 'menu/menu.html', {
        'categories': categories,
        'dishes': dishes,
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
    # ❗ НЕ перекидає в кошик
    return redirect(request.META.get('HTTP_REFERER', 'menu'))


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


def checkout(request):
    if request.method == 'POST':
        order = Order.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total=0
        )

        cart = request.session.get('cart', {})
        total = Decimal('0')

        for key, item in cart.items():
            dish = Dish.objects.get(id=key)
            OrderItem.objects.create(
                order=order,
                dish=dish,
                quantity=item['qty']
            )
            total += Decimal(item['price']) * item['qty']

        order.total = total
        order.save()

        request.session['cart'] = {}
        return render(request, 'menu/success.html', {'order': order})

    return render(request, 'menu/checkout.html')


def add_review(request):
    if request.method == 'POST':
        Review.objects.create(
            name=request.POST.get('name'),
            text=request.POST.get('text')
        )
        return redirect('home')

