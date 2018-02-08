from django.conf.urls import url

from .views import TaskListView, TaskCreateView, CheckCodeView, TestCodeView

app_name = "tasks"

urlpatterns = [
    url(r'^$', TaskListView.as_view(), name='list'),
    url(r'^new$', TaskCreateView.as_view(), name='new'),
    url(r'^check$', CheckCodeView.as_view(), name='check'),
    url(r'^test', TestCodeView.as_view(), name='test'),
]
