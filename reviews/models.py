from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.fields.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ganre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.fields.SlugField(unique=True)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(max_length=150)

    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900),
                    MaxValueValidator(datetime.now().year)],
        help_text="Use the following format: <YYYY>")

    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='title'
                                 )

    ganre = models.ForeignKey(Ganre,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='title'
                              )

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              null=True,
                              related_name='review'
                              )

    text = models.TextField(verbose_name='Комментарий',
                            help_text='Добавьте комментарий'
                            )

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               null=False,
                               related_name='review'
                               )

    pub_date = models.DateTimeField('date published', auto_now_add=True)

    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Use the following range: <1-10')

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(verbose_name='Commetnts',
                            help_text='Add comment'
                            )

    pub_date = models.DateTimeField('date published', auto_now_add=True)

    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               null=False,
                               related_name='сomment'
                               )

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comment'
                               )

    def __str__(self):
        return self.text[:15]
