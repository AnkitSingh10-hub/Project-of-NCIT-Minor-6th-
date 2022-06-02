import decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from .models import Category, Product, UserCreateForm, Cart, Address
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Carousel
from django.contrib.auth.decorators import login_required


# checking git
def Master(request):
    return render(request, 'master.html')


def Index(request):
    obj = Carousel.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(subcategory=categoryID).order_by('-id')
    else:
        product = Product.objects.all()

    context = {
        'category': category,
        'product': product,
        'obj': obj
    }

    return render(request, 'index.html', context)


def signup(request):
    if request.method == "POST":

        # ******** now we take the all the input from the user  which he can enter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if (password == confirm_password):
            # now we check if user is already exist or not
            if User.objects.filter(username=username).exists():
                messages.info(request, "username is already taken ")
                print(" user is already exist ")
                return redirect('signup')

            elif User.objects.filter(email=email):
                messages.info(request, "email is already taken ")
                print(" Email Adress is already exist ")
                return redirect('signup')

            # ******** now we creating the object of User clas
            else:
                myuser = User.objects.create_user(username=username, email=email, password=password)

                myuser.first_name = fname
                myuser.last_name = lname

                # ********** now we save the user from the database
                myuser.save()
                print("account is created")

        else:
            print("password does not match")
            messages.info(request, "password does not match ....")
            return redirect('signup')

        # ********** now we show a message when user create account succesfully
        messages.success(request, "Your account has been succesfully created. ")

        # **********  when account is created succsefully created than he or she redirect the login page
        return redirect('login')

    return render(request, "registration/signup.html")


def signin(request):
    if request.method == 'POST':
        # now here we can get the all field value which user can enter 
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
            print("logged in ")

        else:
            messages.info(request, 'invalid credentials')
            print(" not logeed in")
            return redirect('login')

    else:
        return render(request, "registration/login.html")


def signout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url="/signin/")
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is already in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    return redirect('cart')


@login_required(login_url="/signin/")
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('cart')




@login_required(login_url="/signin/")
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'cart.html', context)


@login_required(login_url="/signin/")
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('cart')


@login_required(login_url="/signin/")
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('cart')

