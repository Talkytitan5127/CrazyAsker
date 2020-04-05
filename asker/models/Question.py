from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation

from .LikeDislike import LikeDislike
from .User import User


class QuestionManager(models.Manager):
    pass


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    title = models.TextField()
    text = models.TextField()
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    votes = GenericRelation(LikeDislike, related_query_name='questions')

    manager = QuestionManager()

    def __str__(self):
        return self.title

    def rating(self):
        return 100
