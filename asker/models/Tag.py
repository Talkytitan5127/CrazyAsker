from django.db import models

from .Question import Question


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    question_id = models.ManyToManyField(Question, related_name='tags')
