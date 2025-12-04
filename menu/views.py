from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib import messages


def index(request):
    products = Product.objects.filter(available=True)
    return render(request, "menu/index.html", {"products": products})


# --- Кошик в session ---
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session['cart'] = cart
    messages.success(request, f"{product.title} додано у кошик!")

    return redirect('home')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * qty
        total += item_total

        cart_items.append({
            "product": product,
            "quantity": qty,
            "item_total": item_total
        })

    return render(request, "menu/cart.html", {
        "cart_items": cart_items,
        "total": total,
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