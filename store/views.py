from itertools import product
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from .models import Product, ProductColor, ProductSize, RateProduct, ReviewProduct
from orders.models import OrderProduct
from category.models import Category
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from collections import Counter
from django.contrib import messages

# Create your views here.



def store(request):
    product = Product.objects.all()
    paginator = Paginator(product, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'product': paged_products,
    }

    return render(request, 'store.html', context)


def product_detail(request, category_slug, product_slug):
    rating_rounded = 0
    is_product_odered = False

    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    product_review = ReviewProduct.objects.filter(product__slug=product_slug)
    review_count = product_review.count()
    product_rating = RateProduct.objects.filter(product__slug=product_slug)
    rating_count = product_rating.count()

    value = []
    for x in product_rating:
        value.append(x.rating)

    d = Counter(value)
    star_5 = d[5]
    star_4 = d[4]
    star_3 = d[3]
    star_2 = d[2]
    star_1 = d[1]

    total_star = (star_5 * 5) + (star_4 * 4) + (star_3 * 3) + (star_2 * 2) + star_1
    if rating_count >= 1:
        overall_rating = total_star / rating_count
        rating_rounded = round(overall_rating, 1)

    if request.user.id is not None:
        is_product_odered = OrderProduct.objects.filter(
            order__status='Completed', 
            user=request.user,
            product=single_product
            ).exists()


 
    context = {
        'single_product': single_product,
        'product_review': product_review,
        'is_product_odered':is_product_odered,
        'star_count_5': star_5,
        'star_count_4': star_4,
        'star_count_3': star_3,
        'star_count_2': star_2,
        'star_count_1': star_1,
        'review_count': review_count,
        'rating_count': rating_count,
        'rating_rounded': rating_rounded,
    }

    return render(request, 'product_detail.html', context)


def review_and_rating(request, category_slug, product_slug):
    user = request.user
    product = Product.objects.get(category__slug=category_slug, slug=product_slug)

    if request.method == 'POST':
        if 'review' in request.POST:
            title = request.POST['title']
            review = request.POST['review']

            ReviewProduct.objects.create(
                user=user,
                product=product,
                review_title=title,
                review=review,
            )

        if 'rating_value' in request.POST:
            rating = request.POST['rating_value']
            is_product_rated = RateProduct.objects.filter(user=user, product=product).exists()
            if is_product_rated is True:
                messages.error(request, 'you already rated this product')
            else:
                RateProduct.objects.create(
                    user=user,
                    product=product,
                    rating=rating,
                )

        return render(request, 'review_and_rating.html')
    else:
        return render(request, 'review_and_rating.html')


def category_detail(request, category_slug):
    try:
        single_category = Product.objects.filter(category__slug=category_slug).order_by('id')
        si_count = single_category.count()
        paginator = Paginator(single_category, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    except Exception as e:
        raise e
    context = {
        'single_category': paged_products,
        'si_count': si_count,
    }

    return render(request, 'store.html', context)


def search(request):
    product = None
    result_count = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            result_count = product.count()
    context = {
        'search_products':product,
        'result_count': result_count,
    }
    return render(request, 'store.html', context)
        

