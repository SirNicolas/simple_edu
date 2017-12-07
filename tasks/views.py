from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponseRedirect, JsonResponse

from .models import Task
from .forms import UploadFileForm
from .utils import check_code


class TaskCreateView(FormView):
    form_class = UploadFileForm
    template_name = 'tasks/task_new.html'
    success_url = reverse_lazy('tasks:list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('tasks:list'))
        else:
            return self.form_invalid(form)


class TaskListView(ListView):
    model = Task

    def post(self, request, *args, **kwargs):
        result = ''
        task_id = request.POST['task_id']
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            task = None
        if task:
            result = check_code(task.file)
        return JsonResponse({'status': 'ok', 'text': result})