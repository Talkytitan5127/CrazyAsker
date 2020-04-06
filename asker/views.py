from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404

from .models import Question, Tag, User


def index(request):
    questions = Question.manager.order_by('-updated_at').all()
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


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')

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
