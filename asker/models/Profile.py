from django.db import models
from django.contrib.auth.models import User

# def sort_user_by_rating(user):
#     rating = 0
#     for answer in user.answer_set.all():
#         rating += answer.rating()
#     return rating

#
# class ProfileManager(models.Manager):
#     def popular_users(self):
#         return sorted(self.get_queryset().all(), key=sort_user_by_rating, reverse=True)[:10]
#


class Profile(models.Model):
    avatar = models.ImageField(upload_to='media', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
