# Generated by Django 2.0 on 2018-02-08 04:04

from django.db import migrations, models
import django.db.models.deletion
import tasks.models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('3', 'done'), ('0', 'not_tested'), ('2', 'on_review'), ('1', 'tested')], default=tasks.models.StatusEnum(0), max_length=1),
        ),
        migrations.AddField(
            model_name='testcase',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='tasks.Task', verbose_name='Тесты для задач'),
        ),
    ]
