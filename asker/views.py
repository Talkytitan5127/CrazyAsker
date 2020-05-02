import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Question, Tag, Profile, LikeDislike, Answer
from .forms import LoginForm, SignupForm, ProfileForm
from .forms import QuestionForm, AnswerForm


def index(request):
    questions = Question.objects.order_by('-updated_at')
    page_obj = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {
                      'page_obj': page_obj,
                      #'popular_tags': Tag.objects.popular_tags,
                      #'popular_users': User.objects.popular_users,
                  })


def new(request):
    questions = Question.objects.new_today()
    page_obj = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {
                      'page_obj': page_obj,
                      'popular_tags': Tag.objects.popular_tags,
                      'popular_users': User.objects.popular_users,
                      'user': {
                          'is_authorized': False,
                      }
                  })

def hot(request):
    questions = Question.objects.hot_today()
    page_obj = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {
                      'page_obj': page_obj,
                      'popular_tags': Tag.objects.popular_tags,
                      'popular_users': User.objects.popular_users,
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
                      'popular_tags': Tag.objects.popular_tags,
                      #'popular_users': User.objects.popular_users,
                  })


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.all()
    page_obj = paginate(answers, request, 20)
    if request.method == 'POST':
        form = AnswerForm(request.user, question, request.POST)
        if form.is_valid():
            answer = form.save()
            return redirect('question_index', question_id=question.question_id)
    else:
        form = AnswerForm(request.user, question)
    return render(request, 'question.html',
                  {
                      'form': form,
                      'question': question,
                      'page_obj': page_obj,
                      'popular_tags': Tag.objects.popular_tags,
                      #'popular_users': User.objects.popular_users,
                  })

def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('question_index', question_id=question.question_id)
    else:
        form = QuestionForm(request.user)
    return render(request, 'ask.html', {'form': form})


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

            profile = Profile(user=user)
            profile.save()

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
    if request.method == 'POST':
        profile_form = ProfileForm(request.user, request.POST, request.FILES)
        user_form = SignupForm(request.POST)
        if 'avatar' in request.FILES and profile_form.is_valid():
            profile_form.save()
        else:
            if user_form.is_valid():
                user_data = user_form.cleaned_data
                user = request.user
                user.username = user_data['username']
    else:
        user = request.user
        profile_form = ProfileForm(user)
        user_form = SignupForm(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    return render(request, 'settings.html', {'profile_form': profile_form, 'user_form': user_form})


def paginate(objects_list, request, count_per_page):
    paginator = Paginator(objects_list, count_per_page)
    page = request.GET.get('page', 1)
    result_list = paginator.get_page(page)
    return result_list


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)


def add_like(request):
    user = request.user
    if user is None:
        return JsonResponse({'message': 'not authorized'}, status=401)

    data = request.POST
    object_id = data.get('object')
    content = data.get('content')
    object = None
    if content == 'question':
        object = get_object_or_404(Question, pk=object_id)
    elif content == 'answer':
        object = get_object_or_404(Answer, pk=object_id)
    else:
        return JsonResponse({'status': 'OK'}, status=200)

    like = LikeDislike.objects.filter(object_id=object_id, vote=LikeDislike.LIKE, author=user).first()
    if like is None:
        object.votes.create(author_id=user.id, vote=LikeDislike.LIKE)
        object.rating += 1
        object.save()
    else:
        like.delete()
        object.rating = object.count_rating()
        object.save()

    return JsonResponse({'rating': object.rating}, status=200)
