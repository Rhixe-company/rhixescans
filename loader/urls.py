from django.urls import path

from . import views

app_name = 'loader'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.comic_search, name='comic_search'),
    path('bookmark/<str:pk>/', views.bookmark, name='bookmark'),
    path('bookmark/', views.bookmark_list, name='bookmark_list'),
    path('like/', views.like, name='like'),
    path('genre/<genre>/', views.CatListView.as_view(), name='genre'),
    path('comics/', views.comics, name='comics'),
    path('comic/<str:pk>/', views.comic, name='comic'),
    path('comic/chapter/<str:pk>/', views.chapterview, name='chapter'),
    path('create-comic/', views.createComic, name="create-comic"),
    path('update-comic/<str:pk>/', views.updateComic, name="update-comic"),
    path('delete-comic/<str:pk>/', views.deleteComic, name="delete-comic"),
    path('create-chapter/', views.createChapter, name="create-chapter"),
    path('update-chapter/<str:pk>/', views.updateChapter, name="update-chapter"),
    path('delete-chapter/<str:pk>/', views.deleteChapter, name="delete-chapter"),
    path('delete-review/<str:pk>/', views.deleteReview, name="delete-review"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
]
