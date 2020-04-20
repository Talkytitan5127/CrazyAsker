from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import Question, Tag, Profile
from .forms import LoginForm, SignupForm


def index(request):
    questions = Question.manager.order_by('-updated_at')
    page_obj = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {
                      'page_obj': page_obj,
                      #'popular_tags': Tag.manager.popular_tags,
                      #'popular_users': User.manager.popular_users,
                  })


def new(request):
    questions = Question.manager.new_today()
    page_obj = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {
                      'page_obj': page_obj,
                      'popular_tags': Tag.manager.popular_tags,
                      'popular_users': User.manager.popular_users,
                      'user': {
                          'is_authorized': False,
                      }
                  })

def hot(request):
    questions = Question.manager.hot_today()
    page_obj = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {
                      'page_obj': page_obj,
                      'popular_tags': Tag.manager.popular_tags,
                      'popular_users': User.manager.popular_users,
                      'user': {
                          'is_authorized': False,
                      }
                  })


def tag_filter(request, tag_name):
    tag = get_object_or_404(Tag, title=tag_name)
    questions = tag.questions.all()
    page_obj = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {
                      'page_obj': page_obj,
                      'search_tag': tag_name,
                      'popular_tags': Tag.manager.popular_tags,
                      'popular_users': User.manager.popular_users,
                  })


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.all()
    page_obj = paginate(answers, request, 20)
    return render(request, 'question.html',
                  {
                      'question': question,
                      'page_obj': page_obj,
                      'popular_tags': Tag.manager.popular_tags,
                      'popular_users': User.manager.popular_users,
                  })

def ask(request):
    return render(request, 'ask.html')


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, 'deactivated user')
                    return redirect('login')
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')
    else:
        form = LoginForm()

        return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = form.save()
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.email = data.get('email')
            user.save()

            username = data.get('username')
            password = data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Smth wrong with user')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def one_quest(request):
    return render(request, 'primitives/one_question.html')


def settings(request):
    return render(request, 'settings.html')


def paginate(objects_list, request, count_per_page):
    paginator = Paginator(objects_list, count_per_page)
    page = request.GET.get('page', 1)
    result_list = paginator.get_page(page)
    return result_list


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)
