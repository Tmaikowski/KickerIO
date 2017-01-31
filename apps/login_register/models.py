from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

#Extend User model to add more fields
#Make a one-to-one relationship with User and add any additional fields
#If self join/one-to-one relationship doesn't work for friends feature, try proxy model
#Proxy Model link: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', blank=True, symmetrical=False)
    birthday = models.DateTimeField()
    bio = models.TextField(max_length=1000)
