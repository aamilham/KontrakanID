from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'account'

urlpatterns = [
    path('register', views.MyRegisterView.as_view(), name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='account:login'), name='logout'),
    path('profile/<int:pk>', views.MyProfile.as_view(), name='profile'),
    path('profile/<int:pk>/waiting/list', views.MyWaitingList.as_view(), name='waiting_list'),
    path('profile/<int:pk>/rent/list', views.MyRent.as_view(), name='rent_list'),
    path('profile/<int:pk>/comment/list', views.MyComment.as_view(), name='comment_list'),
    path('profile/<int:pk>/create', views.CreateProfile.as_view(), name='create_profile'),
    path('profile/<int:pk>/update', views.UpdateProfile.as_view(), name='update_profile'),

]