from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect


from shop.models import Products
from cart.models import Cart

from cart.models import Order_details


@login_required
def addtocart(request,i):
    u=request.user       #user details
    p=Products.objects.get(id=i)
    try:                #if record is not present
        c=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            c.quantity+=1                              #updates the record already inside the table cart
            c.save()                                   #saves the record
            p.stock-=1
            p.save()

    except:            #if record not present
        if(p.stock):
            c=Cart.objects.create(user=u,product=p,quantity=1)    #new cart record
            c.save()       #saves the record
            p.stock-=1
            p.save()

    return redirect('cart:cartview')

@login_required
def cartview(request):
    u=request.user
    c=Cart.objects.filter(user=u)
    total=0

    for i in c:
        total+=i.quantity*i.product.price

    context={'cart':c,'total':total}
    return render(request,'cart.html',context)

def cart_decrement(request,pk):
    p=Products.objects.get(id=pk)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()
            p.stock+=1
            p.save()
        else:
            cart.delete()
            p.stock+=1
            p.save()
    except:
        pass
    return redirect('cart:cartview')

def cart_delete(request,pk):
    p=Products.objects.get(id=pk)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        cart.delete()
        p.stock+=cart.quantity
        p.save()

    except:
        pass
    return redirect('cart:cartview')

import razorpay
from cart.models import Payment

def order_form(request):
    if (request.method == 'POST'):
        a = request.POST['a']
        p = request.POST['p']
        ph = request.POST['ph']

        u=request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total+=i.quantity*i.product.price
        total=int(total)

        #razorpay client connection
        client=razorpay.Client(auth=('rzp_test_QDjytVY6nAtmnp','Tk6mrMNunAw7rmhER6b5rY5k'))
        #razorpay order creation
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        print(response_payment)
        order_id=response_payment['id']    #retrieve the order id from response
        status=response_payment['status']  #retrive the status from response

        if(status=="created"):
            pa=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            pa.save()

            for i in c:
                o=Order_details.objects.create(product=i.product,user=i.user,phone=ph,address=a,pin=p,order_id=order_id,no_of_items=i.quantity)
                o.save()

            context={'payment':response_payment,'name':u.username} #sends the response from view to payment.html
            return render(request,'payment.html',context)

    return render(request,'orderform.html')

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.models import User

@csrf_exempt
def status(request,n):
    user=User.objects.get(username=n)
    login(request,user)
    response=request.POST
    print(response)

    #to check the validity(authenticity)of razorpay payment details received by application
    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }

    client=razorpay.Client(auth=('rzp_test_QDjytVY6nAtmnp','Tk6mrMNunAw7rmhER6b5rY5k'))
    try:
        status=client.utility.verify_payment_signature(param_dict)   #for checking the payment details
                                                                      #we pass param_dict to verify_payment_signature function
        print(status)
        # To add values in payment & order table that where empty

        pa = Payment.objects.get(order_id=response['razorpay_order_id'])
        pa.paid = True
        pa.razorpay_payment_id = response['razorpay_payment_id']
        pa.save()

        o = Order_details.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:
            i.payment_status = "completed"
            i.save()
        c=Cart.objects.filter(user=user)
        c.delete()
    except:
        pass


    return render(request,"status.html")


def order_view(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status="completed")
    context={'order':o}
    return render(request,'orderview.html',context)

