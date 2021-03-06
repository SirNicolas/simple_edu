import inspect
from enum import Enum
from django.db import models


class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


class StatusEnum(ChoiceEnum):
    not_tested = 0
    tested = 1
    on_review = 2
    done = 3


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(null=True)
    status = models.CharField(max_length=1, choices=StatusEnum.choices(),
                              default=StatusEnum.not_tested.value)


class TestCase(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(blank=True, null=True)
    task = models.ForeignKey(
        Task, verbose_name='Тесты для задач', related_name='cases',
        on_delete=models.CASCADE)

    def get_input_items(self):
        return self.items.filter(is_input=True)

    def get_output_items(self):
        return self.items.filter(is_input=False)


class TestInOut(models.Model):
    value = models.CharField(max_length=255)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE,
                                  verbose_name='Входные/выходные данные',
                                  related_name='items')
    is_input = models.BooleanField(default=True)
