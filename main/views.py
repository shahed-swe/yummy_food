from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
import json
from .utils import cartData, cookieCart,guestOrder
import datetime
# Create your views here.
def home(request):
    data = cartData(request)
    order = data['order']
    items = data['items']

    place = Place.objects.all()
    context = {"title": "Home | Yummy Food",
               "place": place, "items": items, "order": order}
    return render(request, 'user/home.html',context)

def handler404(request, exception, template_name="404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response

def myregistration(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User(
                username = request.POST.get('username'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
                is_customer = True,
                is_active = True,

            )
            user.set_password(request.POST.get('password1'))
            user.save()
            print(user.password)
            customer = Customer(
                user = user,
                full_name = user.first_name + ' ' +user.last_name,
                phone_no = request.POST.get('phone_no'),
            )
            customer.save()
        else:
            return redirect('/registration')
    data = cartData(request)
    order = data['order']
    items = data['items']
    return render(request, 'user/registration.html', {"title": "Registration", "order": order, "items": items})

def mylogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        utxt = request.POST.get('username')
        upass = request.POST.get('password')
        if utxt != '' and upass != '':
            user = authenticate(username=utxt, password=upass)
            if user != None:
                login(request, user)
                return redirect('/')
        else:
            return redirect('/login')
    data = cartData(request)
    order = data['order']
    items = data['items']
    context = {"title":"Login","order":order,"items":items}
    return render(request, 'login.html', context)

def mylogout(request):
    logout(request)
    return redirect('/login')

def userprofile(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    if request.user.is_customer and request.user.is_authenticated:
        user = Customer.objects.get(pk=request.user.pk)
        context = {"title": f"Profile | {request.user.username.title()}", "order": order, "items": items,"otheruser":user}
    elif request.user.is_resturent and request.user.is_authenticated:
        user = ResturantUser.objects.get(pk=request.user.pk)
        food = FoodName.objects.filter(provider=user)
        context = {"title": f"Profile | {request.user.username.title()}","order": order, "items": items, "otheruser": user, "food": len(food)}
    else:
        user = request.user
        context = {"title": f"Profile | {request.user.username.title()}", "order": order, "items": items,"otheruser":user}
    print(user)
    if request.method == "POST":
        password = request.POST.get('password1')
        conf_pass = request.POST.get('password2')
        if password == conf_pass:
            user = User.objects.get(username=request.user.username)
            user.set_password(password)
            user.save()
            return redirect('/')
        else:
            return HttpResponse("<h1>Password Doesn't Match</h1><a href='/profile'>Back</a>")
    
    return render(request, 'user/profile.html', context)

def foods(request, slug):
    data = cartData(request)
    order = data['order']
    items = data['items']

    place = Place.objects.filter(district_name=slug)
    resturants = ResturantUser.objects.filter(position=place[0].pk)
    foods = []
    for i in resturants:
        foods.append(FoodName.objects.filter(provider=i.pk))

    categories = []
    for i in foods:
        for j in i:
            if j.category.category_name not in categories:
                categories.append(j.category.category_name)
    context = {"title":"Foods","slug":slug,"foods":foods,"resturants":resturants,"categories":categories,"items":items, "order":order}
    return render(request, 'user/food_list.html', context)

def resturant_registration(request):
    data = cartData(request)
    order = data['order']
    items = data['items']


    place = Place.objects.all()
    context = {"title": "Registration | Yummy Foods", 'place': place}
    if request.user.is_authenticated and request.user.is_customer:
        if request.method == "POST":
            User.objects.filter(pk=request.user.pk).update(is_resturent=True, is_customer=False,is_staff=True)
            user = request.user
            resturent = ResturantUser(
                user = user,
                full_name = user.first_name +' '+user.last_name,
                resturant_name = request.POST.get('resturantname'),
                resturant_front=request.FILES['resturant_image'],
                description = request.POST.get('description'),
                menu_list = request.FILES['menu-image'],
                phone_no = request.POST.get('phone_no'),
                position = Place.objects.get(district_name=request.POST.get('cityname')),
            )
            resturent.save()
            return redirect('/')
        return render(request, 'resturant/registration.html', context)
        
    else:
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user = User(
                    username = request.POST.get('username'),
                    first_name = request.POST.get('first_name'),
                    last_name = request.POST.get('last_name'),
                    email = request.POST.get('email'),
                    is_resturent = True,
                    is_active = True,
                    is_staff = True,
                )
                user.set_password(request.POST.get('password1'))
                user.save()
                print(user)
                resturent = ResturantUser(
                    user = user,
                    full_name = user.first_name + ' ' + user.last_name,
                    resturant_name = request.POST.get('resturantname'),
                    resturant_front=request.FILES['resturant_image'],
                    description = request.POST.get('description'),
                    menu_list = request.FILES['menu-image'],
                    phone_no=request.POST.get('phone_no'),
                    position = Place.objects.get(district_name=request.POST.get('cityname')),
                )
                resturent.save()
                return redirect('/')
        return render(request, 'resturant/registration.html', context)
        
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = Customer.objects.get(user=request.user.pk)
    # print(customer)
    product = FoodName.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, food=product)
    if action ==  'add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()
        response = "Item has added"
    elif action == "remove":
        orderItem.delete()
        response = "Item has deleted Successfully"
    return JsonResponse(response, safe=False)


def cart(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    context = {"title":"Food Cart", "items":items, "order":order}
    return render(request, 'user/cart.html',context)


def checkout(request):

    data = cartData(request)
    order = data['order']
    items = data['items']

    context = {"title":"Checkout", "items":items, "order":order}
    return render(request, 'user/checkout.html',context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(int(transaction_id))
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user.pk)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request,data)

    total = int(data['form']['total'])
    order.transaction_id = int(transaction_id)

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    # print(customer.user.email)
    shipping = ShippingAddress(
        customer=customer,
        order=order,
        name=customer.full_name,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        phone_no=data['shipping']['phone'],
        email=customer.user.email,
    )
    shipping.save()
    response = "Transaction Successfull"
    return JsonResponse(response, safe=False)


def track_order(request):
    if request.user.is_authenticated and request.user.is_customer:
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.filter(customer=customer)
        
        context = {"title":"Track Order","orders":order}
        return render(request, 'user/track_order.html',context)
    else:
        return redirect('/')
