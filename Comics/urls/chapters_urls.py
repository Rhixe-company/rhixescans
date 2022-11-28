from django.urls import path
from Comics.views import chapters_views as views

urlpatterns = [
    path('', views.getChapters, name="chapters"),
    path('<str:pk>/', views.getChapter, name="chapter"),
    path('top/', views.getTopChapters, name='top-chapters'),
    path('create/', views.createChapter, name="chapter-create"),
    path('<str:pk>/reviews/', views.createChapterReview,
         name="chapter-create-review"),
    path('update/<str:pk>/', views.updateChapter, name="chapter-update"),
    path('delete/<str:pk>/', views.deleteChapter, name="chapter-delete"),
]
