from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/', views.Forum.as_view(), name='forum'),
    path('rent/<int:pk>/', views.RentDetail.as_view(), name='rent'),
] 