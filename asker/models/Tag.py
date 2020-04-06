from django.db import models
from django.db.models import Count

from .Question import Question

class TagManager(models.Manager):
    def popular_tags(self):
        return self.get_queryset().all().annotate(count=Count('questions')).order_by('-count')[:10]


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    questions = models.ManyToManyField(Question, related_name='tags')

    manager = TagManager()

    def __str__(self):
        return self.title