from django.db import models
from .utils import ChoiceEnum


class StatusEnum(ChoiceEnum):
    not_tested = 0
    tested = 1
    on_review = 2
    done = 3


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField()
    status = models.CharField(max_length=1, choices=StatusEnum.choices(),
                              default=StatusEnum.not_tested)


class TestCase(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField()
    task = models.ForeignKey(
        Task, verbose_name='Тесты для задач', related_name='cases',
        on_delete=models.CASCADE)
