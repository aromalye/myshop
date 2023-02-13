import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mycart.models import MyCartItem
from . forms import AddChoice
from orders.models import Order, OrderProduct, Payment
import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from store.models import Product
# Create your views here.



def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])


    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid  = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to order product table
    cart_items = MyCartItem.objects.filter(user=request.user)

    for x in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = x.product.id
        orderproduct.quantity = x.quantity
        orderproduct.product_price = x.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # reduce the quantity of sold products

        product = Product.objects.get(id=x.product_id)
        product.stock -= x.quantity
        product.save()

    #clear cart
    MyCartItem.objects.filter(user=request.user).delete()

    #send mail

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def delete_order(request, order_number):
    order = Order.objects.get(order_number=order_number, user=request.user)
    order.is_ordered = False
    order.save()
    return redirect('my_orders')


def order_completed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    user = request.user
    try:
        order = Order.objects.get(order_number=order_number)
        ordered_poduct = OrderProduct.objects.filter(order_id=order.id)

        total = 0
        for x in ordered_poduct:
            total += x.product_price * x.quantity
        
        payment = Payment.objects.get(payment_id=transID)

        # order placed mail
        mail_subject = 'Your Order placed successfully'
        message = render_to_string('order_recieved_email.html', {
            'user': user,
            'order': order,
        })
        to_email = order.email
        print(to_email)
        send_email = EmailMessage(
            mail_subject, 
            message,
            settings.EMAIL_HOST_USER, 
            to=[to_email],
            )
        send_email.fail_silently=False
        send_email.send()

        context = {
            'order': order,
            'ordered_product': ordered_poduct,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'total': total,
        }

        return render(request, 'order_completed.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def place_order(request, total=0, quantity=0):
    user = request.user
    cart_items = MyCartItem.objects.filter(user=user)
    
    grand_total = 0
    tax = 0
    dis_price = 0

    for x in cart_items:
        total += (x.product.price * x.quantity)
        quantity += x.quantity
        dis_price += x.discount

    tax = total // 10
    grand_total = total + tax - dis_price

    if request.method == 'POST':
        data = Order()
        data.user = user
        data.first_name = request.POST['firstname']
        data.last_name = request.POST['lastname']
        data.phone = request.POST['phone']
        data.email = request.POST['email']
        data.address_line_1 = request.POST['address1']
        data.address_line_2 = request.POST['address2']
        data.country = request.POST['country']
        data.state = request.POST['state']
        data.city = request.POST['city']
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()

        # Generate order number

        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        order = Order.objects.get(user=user, order_number=order_number)

        context = {
            'cart_items': cart_items,
            'order': order,
            'total': total,
            'tax': tax,
            'grand_total': grand_total
        }

        return render(request, 'payment.html', context) 

    else:
        return redirect('checkout')