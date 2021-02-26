from django.urls import path
from . import views
from hashlib import md5

urlpatterns = [
    path('', views.home, name="home"),
    path('registration/', views.myregistration, name="myregistration"),
    path('login/', views.mylogin, name="mylogin"),
    path('logout/', views.mylogout, name="mylogout"),

]