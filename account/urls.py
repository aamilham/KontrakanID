from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import MyRegisterView, MyLoginView

app_name = 'account'

urlpatterns = [
    path('register', MyRegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='account:login'), name='logout'),
]