from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Cart,Order,CartItems
from accounts.models import User
from django.contrib import messages
import razorpay
from django.views.generic.list import ListView
# Create your views here.
def home(request):
    return render(request, 'home.html')

def notfound(request):
    return render(request,'404.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'product_details.html', {'product': product})

def checkout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            pincode = request.POST.get('pin')
            city = request.POST.get('city')
            state = request.POST.get('state')
            user = request.user
            print(name,email,address,phone,pincode,city,state)
            cart = Cart.objects.get(user=user)
            cart_item = CartItems.objects.filter(cart=cart).first()
            cart_product = cart_item.product.id
            product = Product.objects.get(id=cart_product)
            price = cart_item.product.price
            client = razorpay.Client(auth = ("rzp_test_1zE4jRy2JKhcJq","j6Jv36KmPOlJMB7YQIbbrz4Y"))
            payment = client.order.create({'amount':price*100, 'currency':"INR",'payment_capture':'1'})

            order = Order.objects.create(
                user = user,
                product = product,
                name = name,
                email = email,
                address = address,
                phone = phone,
                pincode = pincode,
                city = city,
                state = state,
                payment_id = payment['id']
            )
            order.save()
            cart_item.delete()
            return render(request,'checkout.html',{'payment':payment,'name':name,'email':email,'phone':phone,'address':address})
        else:
            return redirect('login')
    return render(request, 'checkout.html')





def account(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(user=user,paid=True)
        if orders:
            return render(request, 'account.html',{"orders":orders,"user":user})
        return render(request, 'account.html',{"user":user})
    else:
        return redirect('login')
    

def add_to_cart(request,id):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        product = Product.objects.get(id=id)
        if cart:
            cart_items = CartItems.objects.filter(cart=cart.first())
            if cart_items:
                messages.error(request,"Product is already added to cart")
            else:
                cart_items = CartItems.objects.create(cart=cart.first(),product=product)
                messages.success(request,"Product added to cart")
        else:
            new_cart = Cart.objects.create(user=user)
            cart_items = CartItems.objects.create(cart=new_cart,product=product)
            messages.success(request,"Product added to cart")
    else:
        messages.error(request,"Please Login!")
    return redirect('checkout')
def remove_from_cart(request,id):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get(user=user)
        product = Product.objects.get(id=id)
        if cart:
            cart_item = CartItems.objects.filter(cart=cart,product=product)
            if cart_item:
                cart_item.delete()
                messages.success(request,"Product removed from cart")
            else:
                messages.error(request,"Product is not in cart")
        else:
            messages.error(request,"No items in cart")
    else:
        messages.error(request,"Please Login!")
    return redirect('cart')

def success(request,id):
    order = Order.objects.get(payment_id=id)
    order.paid = True
    order.save()
    return render(request,'success.html')

def failed(request):
    return render(request,'failed.html')