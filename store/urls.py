from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/<slug:product_slug>/review_and_rating/', views.review_and_rating, name='review_and_rating'),
    path('search', views.search, name='search'),
]