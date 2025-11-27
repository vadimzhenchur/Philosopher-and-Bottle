from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Order
from .forms import CheckoutForm
from decimal import Decimal

def index(request):
    popular = Product.objects.filter(available=True)[:6]
    categories = Category.objects.all()
    return render(request, 'menu/index.html', {'popular': popular, 'categories': categories})

def home(request):
    products = Product.objects.filter(available=True)
    return render(request, 'menu/index.html', {'products': products})

def category_view(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    products = cat.products.filter(available=True)
    return render(request, 'menu/category.html', {'category': cat, 'products': products})

def product_detail(request, slug):
    p = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'menu/product_detail.html', {'product': p})

def _get_cart(request):
    return request.session.get('cart', {})

def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    cart = _get_cart(request)
    qty = int(request.POST.get('qty', 1))
    if str(pk) in cart:
        cart[str(pk)]['qty'] += qty
    else:
        cart[str(pk)] = {'title': product.title, 'price': str(product.price), 'qty': qty, 'image': product.image.url if product.image else ''}
    _save_cart(request, cart)
    return redirect('cart')

def cart_view(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0')
    for pid, info in cart.items():
        qty = info['qty']
        price = Decimal(info['price'])
        subtotal = price * qty
        items.append({'pid': pid, 'title': info['title'], 'price': price, 'qty': qty, 'subtotal': subtotal, 'image': info.get('image','')})
        total += subtotal
    return render(request, 'menu/cart.html', {'items': items, 'total': total})

def remove_from_cart(request, pid):
    cart = _get_cart(request)
    cart.pop(str(pid), None)
    _save_cart(request, cart)
    return redirect('cart')

def update_cart(request):
    cart = _get_cart(request)
    for pid, qty in request.POST.items():
        if pid.startswith('qty_'):
            key = pid.split('_',1)[1]
            if key in cart:
                try:
                    q = int(qty)
                    if q <= 0:
                        cart.pop(key, None)
                    else:
                        cart[key]['qty'] = q
                except ValueError:
                    pass
    _save_cart(request, cart)
    return redirect('cart')

def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('index')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            total = Decimal('0')
            for info in cart.values():
                total += Decimal(info['price']) * info['qty']
            order = Order.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total=total
            )
            # clear cart
            request.session['cart'] = {}
            return render(request, 'menu/checkout.html', {'order': order, 'success': True})
    else:
        form = CheckoutForm()
    return render(request, 'menu/checkout.html', {'form': form})