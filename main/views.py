from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    place = Place.objects.all()
    context = {"title": "Home | Yummy Food", "place":place}
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
    return render(request, 'user/registration.html', {"title":"Registration"})

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
    context = {"title":"Login"}
    return render(request, 'login.html', context)

def mylogout(request):
    logout(request)
    return redirect('/login')

def resturant_list(request, slug):
    return HttpResponse("<h1>City name is {}</h1>".format(slug))

def resturant_registration(request):
    # if request.user.is_resturent or request.user.is_authenticated:
    #     return redirect('/')
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
            )
            user.set_password(request.POST.get('password1'))
            user.save()
            print(user)
            resturent = ResturantUser(
                user = user,
                full_name = user.first_name + ' ' + user.last_name,
                resturant_name = request.POST.get('resturantname'),
                description = request.POST.get('description'),
                menu_list = request.FILES['menu-image'],
                position = Place.objects.get(district_name=request.POST.get('cityname')),
            )
            resturent.save()
            return redirect('/')
        else:
            return redirect('/resturant')
    place = Place.objects.all()
    context = {"title":"Registration | Yummy Foods",'place':place}
    
    return render(request, 'resturant/registration.html',context)
