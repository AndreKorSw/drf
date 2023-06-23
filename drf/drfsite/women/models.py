from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Women(models.Model):
    title=models.CharField(max_length=255, verbose_name="Заголовок")
    content=models.TextField(blank=True, verbose_name="Текст статьи")
    time_create=models.DateTimeField(auto_now_add=True, verbose_name="Время сооздания")
    time_update=models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published=models.BooleanField(default=True, verbose_name="Публикация")
    cat=models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категория")
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    name=models.CharField(max_length=100, db_index=True, verbose_name="Категория")

    def __str__(self):
        return self.name

