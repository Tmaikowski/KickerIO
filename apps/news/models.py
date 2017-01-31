from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# IDEA: Look into url shorteners. Bit.ly?
class Article(models.Model):
    title = models.CharField(max_length=255)
    summarized_text = models.TextField()
    url = models.URLField()
    published_on = models.DateTimeField()
    main_image = models.URLField()
    creator = models.ForeignKey(User, related_name="creator", default=0)
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=45)
    articles = models.ManyToManyField(Article)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    created_at = models.DateTimeField(auto_now_add=True)
