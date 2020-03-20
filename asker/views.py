from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render


def index(request):
    questions = [
        {
            'header': 'Сколько часов займет у меня долбанная верстка страниц??',
            'body': 'Я не знаю, я не ожидал такого, это очень интересно, но столько нюансов',
            'author': 'developer',
            'create_data': datetime.now(),
            'tags': ['боль', 'coding'],
            'rating': 100,
        },
        {
            'header': 'Сколько часов займет у меня долбанная верстка страниц??',
            'body': 'Я не знаю, я не ожидал такого, это очень интересно, но столько нюансов',
            'author': 'developer',
            'create_data': datetime.now(),
            'tags': ['боль', 'coding'],
            'rating': 100,
        },
        {
            'header': 'Сколько часов займет у меня долбанная верстка страниц??',
            'body': 'Я не знаю, я не ожидал такого, это очень интересно, но столько нюансов',
            'author': 'developer',
            'create_data': datetime.now(),
            'tags': ['боль', 'coding'],
            'rating': 100,
        }

    ]
    return render(request, 'index.html',
                  {
                      'questions': questions,
                      'tags': ['aa', 'bb', 'cc', 'dd'],
                      'user': {
                          'is_authorized': False,
                      }
                  })


def hot(request):
    pass


def tag_filter(request, tag_name):
    questions = [
        {
            'header': 'Сколько часов займет у меня долбанная верстка страниц??',
            'body': 'Я не знаю, я не ожидал такого, это очень интересно, но столько нюансов',
            'author': 'developer',
            'create_data': datetime.now(),
            'tags': ['aa', 'coding'],
            'rating': 100,
        },
        {
            'header': 'Сколько часов займет у меня долбанная верстка страниц??',
            'body': 'Я не знаю, я не ожидал такого, это очень интересно, но столько нюансов',
            'author': 'developer',
            'create_data': datetime.now(),
            'tags': ['боль', 'aa'],
            'rating': 100,
        }
    ]
    return render(request, 'index.html', {'questions': questions, 'search_tag': tag_name})


def question(request, question_id):
    question = {
        'header': 'Сколько часов займет у меня долбанная верстка страниц??',
        'body': 'Я не знаю, я не ожидал такого, это очень интересно, но столько нюансов',
        'author': 'developer',
        'create_data': datetime.now(),
        'tags': ['боль', 'coding'],
        'rating': 100,
    }
    answers = [
        {
            'body': 'Чувак забей это же вери изи',
            'author': 'user',
            'create_data': datetime.now(),
            'rating': 100,
        },
        {
            'body': 'gg wp',
            'author': 'user',
            'create_data': datetime.now(),
            'rating': 100,
        }
    ]
    return render(request, 'question.html', {
        'question': question,
        'answers': answers
    })


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'register.html')

def one_quest(request):
    return render(request, 'primitives/one_question.html')

def settings(request):
    return render(request, 'settings.html')


def paginate(objects_list, request, count_per_page):
    paginator = Paginator(objects_list, count_per_page)
    page = request.GET.page('page')
    result_list = paginator.get_page(page)
    return result_list