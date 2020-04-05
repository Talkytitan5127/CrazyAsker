from django.db import models

from .Question import Question


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    questions = models.ManyToManyField(Question, related_name='tags')

    def __str__(self):
        return self.title