from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='best_questions'),
    path('tag/<str:tag_name>/', views.tag_filter, name='tag_filter'),
    path('question/<int:question_id>/', views.question, name='question_index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
]