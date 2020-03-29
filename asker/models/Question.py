from django.db import models

from datetime import datetime

from .User import User


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    title = models.TextField()
    text = models.TextField()
    updated_at = models.DateTimeField(default=datetime.now())
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
