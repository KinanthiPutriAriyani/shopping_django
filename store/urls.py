from django.contrib import admin
from django.urls import path
#from .views import home,signup
from .views import update_cart_quantity
from .views import remove_from_cart
from store import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('product-detail/<int:pk>', views.productdetail, name='product-detail'),
    path('logout', views.logout, name='logout'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('show_cart', views.show_cart, name='show_cart'),
    path('update_cart_quantity/<int:cart_item_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('order/', views.order, name='order'),
    path('search/', views.search, name='search')
]   

