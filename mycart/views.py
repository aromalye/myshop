from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from . models import Coupons, MyCartItem, MyFav
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from coupon_management.models import Coupon
from coupon_management.validations import validate_coupon
from coupon_management.models import Discount
from .forms import CouponForm
# Create your views here.


@login_required(login_url='signin')
def add_cart(request, product_id, size, color):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    if 'size' in request.GET:
        size = request.GET['size']
    if 'color' in request.GET:
        color = request.GET['color'] 

    is_cart_item_exists = MyCartItem.objects.filter(
        product=product, 
        user=current_user,
        size=size,
        color=color,
        ).exists()

    if is_cart_item_exists:
        cart_item = MyCartItem.objects.filter(
            product=product, 
            user=current_user,
            size=size,
            color=color,
            )
        for x in cart_item:
            x.quantity += 1
            x.save()
        return redirect('cart')

    else:         
        cart_item = MyCartItem.objects.create(
            user=request.user,
            product=product,
            quantity=1,
            size=size,
            color=color,
            )
        cart_item.save()
        return redirect('cart')


@login_required(login_url='signin')
def remove_cart(request, product_id, size, color):
    product = Product.objects.get(id=product_id)
    cart_item = MyCartItem.objects.get(
        product=product, 
        user=request.user,
        size=size,
        color=color,
        )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('cart')
    else:
        cart_item.delete()
        return redirect('cart')


@login_required(login_url='signin')
def delete_cart(request, product_id, size, color):
    product = Product.objects.get(id=product_id)
    cart_item = MyCartItem.objects.get(
        product=product, 
        user=request.user,
        size=size,
        color=color,
        )
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='signin')
def cart(request):
    coupon_code = None
    form = None
    total = 0
    dis_price = 0

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            coupon_code = form.cleaned_data['code']
    else:
        form = CouponForm()

    user = request.user
    status = validate_coupon(coupon_code=coupon_code, user=user)
    if status['valid']:
        coupon = Coupon.objects.get(code=coupon_code)
        coupon.use_coupon(user=user)

        discount = coupon.get_discount() # Example: {'value': 50, 'is_percentage': True}
        dis_price = discount["value"]


    cart_item = MyCartItem.objects.filter(user=request.user)

    for x in cart_item:
        x.discount = dis_price
        x.save()
        total += (x.product.price * x.quantity)

    tax = total // 10
    grand_total = total + tax - dis_price
    context = {
        'cart_item': cart_item,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'form':form,
    }
    return render(request, 'cart.html', context)


@login_required(login_url='signin')
def checkout(request):
    total = 0

   
    cart_item = MyCartItem.objects.filter(user=request.user)
    cart_count = cart_item.count()

    for x in cart_item:
        total += (x.product.price * x.quantity)
        dis_price = x.discount
    

    tax = total // 10
    grand_total = total + tax - dis_price
    context = {
        'cart_item': cart_item,
        'cart_count': cart_count,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'checkout.html', context)


@login_required(login_url='signin')
def favourite(request):
    if request.user.id is not None:
        fav = MyFav.objects.filter(user=request.user)
        fav_count = fav.count()

        context = {
            'fav': fav,
            'fav_count': fav_count,
        }
        return render(request, 'favourite.html', context)
    else:
        return render(request, 'favourite.html')


@login_required(login_url='signin')
def add_fav(request, slug):
    user = request.user
    product = Product.objects.get(slug=slug)
    fav = MyFav.objects.filter(user=user, Product__slug=slug).exists()
    if fav == False:
        fav = MyFav.objects.create(user=user, Product=product)
        
    return redirect('favourite')


def remove_fav(request, slug):
    user = request.user
    fav = MyFav.objects.filter(user=user, Product__slug=slug)
    fav.delete()
    return redirect('favourite')





