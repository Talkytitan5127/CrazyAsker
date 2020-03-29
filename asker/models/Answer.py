from django.db import models

from datetime import datetime

from .Question import Question
from .User import User


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    text = models.TextField()
    updated_at = models.DateTimeField(default=datetime.now())
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.OneToOneField(Question, on_delete=models.CASCADE, to_field='question_id')
    is_correct = models.BooleanField(default=False)
