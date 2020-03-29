from django.db import models

from .User import User
from .Question import Question
from .Answer import Answer


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        to_field='question_id',
        null=True
    )
    answer_id = models.OneToOneField(
        Answer,
        on_delete=models.CASCADE,
        to_field='answer_id',
        null=True
    )
