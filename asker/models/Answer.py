from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation

from .Question import Question
from .LikeDislike import LikeDislike
from .User import User


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    text = models.TextField()
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    votes = GenericRelation(LikeDislike, related_query_name='answers')

    def __str__(self):
        return self.text

    def rating(self):
        return 50