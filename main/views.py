from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'user/home.html',{"title":"Home"})

def myregistration(request):
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