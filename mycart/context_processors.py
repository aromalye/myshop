from . models import MyCartItem, MyFav


def cart_count(request):
    fav_count = 0
    count = 0
    if request.user.is_authenticated:
        cart_item = MyCartItem.objects.filter(user=request.user)
        fav = MyFav.objects.filter(user=request.user)
        fav_count = fav.count()
        count = cart_item.count()
    return dict(count=count, fav_count=fav_count)