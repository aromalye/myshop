from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from store.models import Product
# Create your views here.


def home(request):
    category = Category.objects.all()
    products = Product.objects.filter(is_featured=True)

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'home.html', context)