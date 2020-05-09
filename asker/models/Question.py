from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

from datetime import timedelta

from .LikeDislike import LikeDislike
from .Profile import User


class QuestionManager(models.Manager):
    def new_today(self):
        last_day = timezone.now() - timedelta(1)
        return self.get_queryset().filter(updated_at__gte=last_day)

    def hot_today(self):
        today_questions = self.new_today()
        return sorted(today_questions, key=lambda elem: elem.rating(), reverse=True)


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    title = models.TextField()
    text = models.TextField()
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    votes = GenericRelation(LikeDislike, related_query_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def count_rating(self):
        return self.votes.likes().count() - self.votes.dislikes().count()

    def author_name(self):
        return self.author.username
