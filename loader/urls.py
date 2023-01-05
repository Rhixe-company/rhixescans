from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.comic_search, name='comic_search'),
    path('bookmark/<str:pk>/', views.bookmark, name='bookmark'),
    path('bookmark/', views.bookmark_list, name='bookmark_list'),
    path('like/', views.like, name='like'),
    path('comics/', views.comics, name='comics'),
    path('comic/<str:pk>/', views.comic, name='comic'),
    path('comic/chapter/<str:pk>/', views.chapterview, name='chapter'),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="signup"),
    path('create-comic/', views.createComic, name="create-comic"),
    path('update-comic/<str:pk>/', views.updateComic, name="update-comic"),
    path('delete-comic/<str:pk>/', views.deleteComic, name="delete-comic"),
    path('create-chapter/', views.createChapter, name="create-chapter"),
    path('update-chapter/<str:pk>/', views.updateChapter, name="update-chapter"),
    path('delete-chapter/<str:pk>/', views.deleteChapter, name="delete-chapter"),
    path('delete-review/<str:pk>/', views.deleteReview, name="delete-review"),
    path('update-user/<str:pk>/', views.updateUser, name="update-user"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
]
