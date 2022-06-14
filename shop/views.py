from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Product, Slide, CartItem, Order, OrderProduct, Review
from .forms import OrderForm, RateForm


@login_required(login_url='/users/sign_in/')
def products(request):
    products_list = Product.objects.all()
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    slides = Slide.objects.all()
    product_id = request.GET.get('product')
    search = request.GET.get('search')

    if product_id:
        product = Product.objects.get(pk=product_id)
        cart_item = CartItem.objects.filter(product=product)

        if not cart_item:
            CartItem.objects.create(
                customer=request.user,
                product=product,
                quantity=1
            )
            return redirect('shop:products')
        for item in cart_item:
            item.quantity += 1
            item.save()

    products_list = products_list.filter(category=category) if category else products_list
    products_list = products_list.filter(brand=brand) if brand else products_list
    products_list = products_list.filter(
        Q(title__icontains=search) | Q(description__icontains=search)) if search else products_list
    return render(request, 'products.html', {'products': products_list, 'slides': slides})


def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    return render(
        request,
        'cart.html',
        {'cart_items': cart_items, 'total_price': total_price, 'total_quantity': total_quantity}
    )


def delete_cart_item(request, pk):
    CartItem.objects.get(pk=pk).delete()
    return redirect('shop:cart')


def edit_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    action = request.GET.get('action')

    if action == 'decrement' and cart_item.quantity == 1:
        cart_item.delete()
        return redirect('shop:cart')
    if action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('shop:cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('shop:cart')


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    reviews = Review.objects.filter(product=product)
    form = RateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.product = product
        instance.save()
        return redirect('shop:product_detail', pk=product.pk)
    return render(request, 'product_detail.html', {'product': product, 'form': form, 'reviews': reviews})


def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    form = OrderForm(request.POST)

    if not cart_items:
        return render(request, 'error.html')

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            customer=request.user,
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_price=total_price
        )
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price()
            )
        cart_items.delete()
        return redirect('shop:orders')

    return render(request, 'order.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'form': form
    })


def orders(request):
    orders_list = Order.objects.filter(customer=request.user)
    return render(request, 'orders.html', {'orders': orders_list})
