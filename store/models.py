from django.db import models
from category.models import Category
from django.urls import reverse
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField

User = get_user_model()

# Create your models here.


class ProductSize(models.Model):
    size = models.CharField(max_length=100, unique=True)

    def __str__(self) :
        return self.size


class ProductColor(models.Model):
    color = models.CharField(max_length=100, unique=True)

    def __str__(self) :
        return self.color


class Product(models.Model):
    size_choices = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )

    color_choices = (
        ('Red', 'Red'),
        ('Black', 'Black'),
        ('Blue', 'Blue'),
    )

    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(null=True, default=False)
    size = MultiSelectField(choices=size_choices, max_length=30, null=True)
    color = MultiSelectField(choices=color_choices, max_length=30, null=True)


    def __str__(self):
        return self.product_name


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def get_url_review(self):
        return reverse('review_and_rating', args=[self.category.slug, self.slug])


class ReviewProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=800)
    created_date = models.DateTimeField(auto_now_add=True)


class RateProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)