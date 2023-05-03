from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/', views.Forum.as_view(), name='forum'),
    path('forum/rent/create/', views.CreateRent.as_view(), name='create_rent'),
    path('forum/rent/<int:pk>/', views.RentDetail.as_view(), name='rent'),
    path('forum/rent/<int:pk>/update', views.UpdateRent.as_view(), name='update_rent'),
    path('forum/rent/<int:pk>/join', views.JoinRent.as_view(), name='join_rent'),
    path('forum/rent/<int:pk>/undo', views.UndoRent.as_view(), name='undo_rent'),
    path('forum/<int:pk>/comment/create', views.CreateComment.as_view(), name='create_comment'),
    path('forum/<int:pk>/comment/update', views.UpdateComment.as_view(), name='update_comment'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)