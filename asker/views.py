from datetime import datetime
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def hot(request):
    pass


def tag_filter(request, tag_name):
    pass


def question(request, question_id):
    question = {
        'header': 'Сколько часов займет у меня долбанная верстка страниц??',
        'body': 'Я не знаю, я не ожидал такого, это очень интересно, но столько нюансов',
        'author': 'developer',
        'create_data': datetime.now(),
        'tags': ['боль', 'coding'],
        'rating': 100,
    }
    return render(request, 'question.html', question)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'register.html')
