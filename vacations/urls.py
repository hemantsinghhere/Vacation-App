from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('create/', views.create_vacation, name='create_vacation'),
    path('vacation/<int:vacation_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/upvote/', views.upvote_comment, name='upvote_comment'),
    path('search/', views.search_vacations, name='search_vacations'),
    path('register/', views.register, name='register'),
    path('vacation/<int:pk>/', views.vacation_detail, name='vacation_detail'),
]