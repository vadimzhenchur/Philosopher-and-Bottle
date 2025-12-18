from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Category, Review
from django.contrib import messages
from .forms import ReviewForm, CheckoutForm


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


def reviews_page(request):
    reviews = Review.objects.order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews')
    else:
        form = ReviewForm()

    return render(request, 'menu/reviews.html', {
        'reviews': reviews,
        'form': form
    })

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            total = Decimal('0')

            new_order = Order.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total=total
            )
            for key, item in cart.items():
                item_db = Product.objects.get(id=key)
                if item_db:
                    order_item = OrderItem.objects.create(order=new_order, product=item_db, quantity=item['qty'])
                    total += Decimal(item['qty'] * item_db.price)

            new_order.total = total
            new_order.save()

            request.session['cart'] = {}
            return redirect('success')

    else:
        form = CheckoutForm()

    return render(request, 'menu/checkout.html', {'form': form})


def success_page(request):
    return render(request, 'menu/success.html')