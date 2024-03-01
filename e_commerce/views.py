from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .models import *
from .models import Product
from .models import Cart

from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'fontends/index.html', { 'products': products })
    
    # return render(request, 'fontends/index.html')

def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        password = request.POST.get('password')
        
        user = authenticate( request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_messsage = "Invalid login credentials. Please try again!"
            return render(request, 'auth/login.html', {'error_messsage': error_messsage})

        
    return render(request, 'auth/login.html')
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        
      
        if password == password_confirmation:
            if User.objects.filter(username = username).exists():
                return render(request, 'auth/register.html', {'error_message' : 'Username is already Taken'})
             
            if User.objects.filter(email= email).exists():
                return render(request, 'auth/register.html', {'error_message' : 'Email is already Taken'})
            
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/')
        else:
            error_message = "Passwords didn't match." 
            return render(request,'auth/register.html',{'error_message':error_message})
                
        
    return render(request, 'auth/register.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'fontends/shop.html', { 'products': products })


def productDetails(request,id):
    product = Product.objects.get(pk=id)
    return render(request, 'fontends/productDetails.html', { 'product': product })

def cart(request):
    user = request.user
    # carts = Cart.objects.filter(user = user)
    
    if user.is_authenticated:
        carts = Cart.objects.filter(user = user)
        
        total_price = 0
        for cart_item in carts:
            total_price += int(cart_item.product.price) * int (cart_item.quantity)
            
    else:
        
        carts = None
        total_price = None
    return render(request, 'fontends/cart.html', {'carts':carts, 'total_price':total_price })


def user_logout(request):
    logout(request)
    return redirect('/')

    
@login_required(login_url = '/login/')

def addToCart(request, product_id):
    product = Product.objects.get(pk = product_id)
    user = request.user
    quantity = request.POST.get('quantity')
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
        
    else:
        cart_item.quantity = int(quantity)
        cart_item.save()
        
    return redirect('/cart/')


# removing carts items
# def removeFromCart(request, cart_id):
def removeFromCart(request, product_id):
    # This code can do the same thing
#      cart_item = Cart.objects.filter(pk=cart_id)
#      cart_item.delete()
#      return redirect('/')
    
    cart_item = get_object_or_404(Cart, pk=product_id) 
    cart_item.delete()
    return redirect('/cart/')

@login_required(login_url= '/login/')
def checkout(request):
    # user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        user = request.user
        carts = Cart.objects.filter(user = user)
        
        new_order = Order.objects.create(user = user, name = name, address = address, phone_number = phone_number)
        for cart_item in carts:
            new_cart_item = OrderDetail.objects.create(order = new_order, product = cart_item.product, quantity = cart_item.quantity, unit_price= cart_item.product.price)
            new_cart_item.save()
            cart_item.delete()
        
        return redirect('/')
    
    user = request.user
    if user.is_authenticated:
        carts = Cart.objects.filter(user = user)
        total_price = 0
        for cart_item in carts:
            total_price += int(cart_item.product.price) * int (cart_item.quantity)
        
    else:
        carts = None
        total_price = None
        
    return render(request, 'fontends/checkout.html', {'carts': carts, 'total_price': total_price})


# @login_required(login_url= '/login/') django build in function: if user is not login in it redirect to the
#  /login page otherwise continue with the code below
def myOrder(request):
     
     user = request.user
    
     if user.is_authenticated:
     
        orders = Order.objects.filter(user = user)
       
     else:
        # total_price = None
        orders = None
        # logout(request)
    
        # return redirect('/')
        # return redirect('/login/')
       
    
     return render(request, 'fontends/myorder.html', {'orders':orders})

def addToWishlist(request, product_id):
    user = request.user
    
    if user.is_authenticated:
        product = Product.objects.get(pk = product_id)
        wishlist_item,created = WishList.objects.create(user = user, product = product)
    if created:
        # created.save()
        wishlist_item.save()
        return redirect('/wishlist/')
        
def wishList(request):
    user = request.user
    if user.is_authenticated:
        wishlist_item = WishList.objects.filter(user = user)
    else:
        wishlist_item = None
        
  
    return render(request, 'fontends/wishlist.html', {'wishlists':wishlist_item})

def removeFromWishlist(request, wishlist_id):
    wishlist_item = WishList.objects.get(pk=wishlist_id)
    wishlist_item = WishList.objects.get(pk=wishlist_id)
    wishlist_item = WishList.objects.get(pk=wishlist_id)
    wishlist_item.delete()  
    return redirect('/wishlist/')

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'fontends/profile.html')



# api urls functions
# def getProducts(request):