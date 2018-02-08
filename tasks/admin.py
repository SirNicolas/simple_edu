from django.contrib import admin
from .models import TestCase, Task, TestInOut

admin.site.register(TestCase)
admin.site.register(Task)
admin.site.register(TestInOut)
