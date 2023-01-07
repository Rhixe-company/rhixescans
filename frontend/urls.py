from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('comic/<str:pk>/', views.comic, name='comic'),
    path('chapter/<str:pk>/', views.chapter, name='chapter'),
    path('create-comic/', views.createComic, name="create-comic"),
    path('update-comic/<str:pk>/', views.updateComic, name="update-comic"),
    path('delete-comic/<str:pk>/', views.deleteComic, name="delete-comic"),
    path('create-chapter/', views.createChapter, name="create-chapter"),
    path('update-chapter/<str:pk>/', views.updateChapter, name="update-chapter"),
    path('delete-chapter/<str:pk>/', views.deleteChapter, name="delete-chapter"),
    path('delete-review/<str:pk>/', views.deleteReview, name="delete-review"),
]
