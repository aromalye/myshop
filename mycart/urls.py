from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/<str:size>/<str:color>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<str:size>/<str:color>/', views.remove_cart, name='remove_cart'),
    path('delete_cart/<int:product_id>/<str:size>/<str:color>/', views.delete_cart, name='delete_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('favourite/', views.favourite, name='favourite'),
    path('add_fav/<slug:slug>/', views.add_fav, name='add_fav'),
    path('remove_fav/<slug:slug>/', views.remove_fav, name='remove_fav'),

]