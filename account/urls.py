from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout', views.signout, name='logout'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name='resetpassword_validate'),
]