from django.forms import ModelForm

from .models import Task


class UploadFileForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'file']
