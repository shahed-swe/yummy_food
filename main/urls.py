from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name="home"),
    path('registration/', views.myregistration, name="myregistration"),
    path('login/', views.mylogin, name="mylogin"),
    path('logout/', views.mylogout, name="mylogout"),
    url(r'^foods/(?P<slug>.*)/$', views.foods, name='foods'),
    path('resturant/', views.resturant_registration,name="resturant_registration"),
    path('profile/', views.userprofile, name="userprofile"),
    path('update_item/', views.update_item, name="update_item"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('process_order/', views.processOrder, name="processOrder"),
    path('track_order/', views.track_order, name="track_order"),

]
