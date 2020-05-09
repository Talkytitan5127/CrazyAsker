from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new_questions'),
    path('hot/', views.hot, name='hot_questions'),
    path('tag/<str:tag_name>/', views.tag_filter, name='tag_filter'),
    path('question/<int:question_id>/', views.question, name='question_index'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('one_question/', views.one_quest, name='one_question'),
    path('profile/edit', views.settings, name='settings'),
    path('api/add_like', views.add_like, name='add_like'),
    path('api/correct_answer', views.correct_answer, name='correct_answer'),
]
