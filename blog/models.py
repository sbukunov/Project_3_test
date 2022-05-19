from django.db import models
from django.contrib.auth.models import User
#from django.utils.translation import gettext_lazy as _


class Note(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    message = models.TextField(default='', verbose_name='Текст')
    public = models.BooleanField(default=False, verbose_name='Опубликовать')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
        #return f"Запись №{self.id}" #Т.е. можем перегрузить вывод как угодно

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['id']

class Comment(models.Model):
    """Комментарии и оценки к статьям"""
    class Rating(models.IntegerChoices):
        WITHOUT_RATING = 0, "Без оценки"
        TERRIBLE = 1, "Ужасно"
        BADLY = 2, "Плохо"
        NORMAL = 3, "Нормально"
        GOOD = 4, "Хорошо"
        EXCELLENT = 5, "Отлично"

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Автор")
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null = True, verbose_name="Сообщение")
    rating = models.IntegerField(default=Rating.WITHOUT_RATING, choices=Rating.choices, verbose_name="Оценка")

    def __str__(self):
        return f"{self.get_rating_display()}: {self.author}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

