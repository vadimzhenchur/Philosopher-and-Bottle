from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Category
from django.contrib import messages


def index(request):
    products = Product.objects.filter(available=True)
    return render(request, "menu/index.html", {"products": products})

def menu_page(request):
    categories = Category.objects.all().prefetch_related("products")
    return render(request, "menu/menu.html", {"categories": categories})


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)

    categories = Category.objects.all()  # щоб верхнє меню працювало

    return render(request, 'menu/category.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })

from django.shortcuts import redirect, get_object_or_404
from .models import Product

def add_to_cart(request, pk):
    cart = request.session.get('cart', {})

    pk = str(pk)
    if pk in cart:
        cart[pk]['qty'] += 1
    else:
        cart[pk] = {'qty': 1}

    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')


from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from .models import Product

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        qty = item['qty']

        subtotal = product.price * qty
        total += subtotal

        items.append({
            'product': product,
            'qty': qty,
            'subtotal': subtotal,
        })

    return render(request, 'menu/cart.html', {
        'items': items,
        'total': total
    })


# --- Оформлення замовлення ---
def checkout(request):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
        )

        total = 0
        for product_id, qty in cart.items():
            product = Product.objects.get(id=product_id)
            total += product.price * qty
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
            )

        order.total = total
        order.save()

        request.session['cart'] = {}

        return render(request, "menu/success.html", {"order": order})

    return render(request, "menu/checkout.html")