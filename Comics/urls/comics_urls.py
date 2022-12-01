from django.urls import path
from Comics.views import comics_views as views

urlpatterns = [
    path('', views.getComics, name="comics"),
    path('top/', views.getTopComics, name='top-comics'),
    path('<str:pk>/', views.getComic, name="comic"),
    path('create/', views.createComic, name="comic-create"),
    path('upload/', views.uploadImage, name="image-upload"),
    path('update/<str:pk>/', views.updateComic, name="comic-update"),
    path('delete/<str:pk>/', views.deleteComic, name="comic-delete"),
    path('<str:pk>/chapters/', views.getChapters, name="comic-chapters"),
]
