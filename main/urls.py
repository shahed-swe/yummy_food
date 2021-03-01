from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name="home"),
    path('registration/', views.myregistration, name="myregistration"),
    path('login/', views.mylogin, name="mylogin"),
    path('logout/', views.mylogout, name="mylogout"),
    url(r'^resturants/(?P<slug>.*)/$', views.resturant_list, name='resturant_list'),
    path('resturant/', views.resturant_registration,
         name="resturant_registration"),


]
