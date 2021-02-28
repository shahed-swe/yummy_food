from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name="home"),
    path('registration/', views.myregistration, name="myregistration"),
    path('login/', views.mylogin, name="mylogin"),
    path('logout/', views.mylogout, name="mylogout"),
    url(r'^foods/(?P<slug>.*)/$', views.food_list, name='food_list'),

]
