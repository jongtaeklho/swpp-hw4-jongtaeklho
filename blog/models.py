from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Article(models.Model):
    title=models.CharField(max_length=64)
    content=models.TextField()
    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_set',
    )
class Comment(models.Model):
    article=models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='article_set'
    )
    content=models.TextField()
    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commentauthor_set'
    )