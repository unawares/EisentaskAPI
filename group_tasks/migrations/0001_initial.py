# Generated by Django 2.0 on 2018-01-26 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(choices=[(1, 'GOALS'), (2, 'PROGRESS'), (3, 'ACTIVITIES'), (4, 'INTERRUPTIONS')])),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_tasks', to='groups.Group')),
            ],
        ),
        migrations.CreateModel(
            name='SharedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_tasks', to=settings.AUTH_USER_MODEL)),
                ('dislikes', models.ManyToManyField(related_name='dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('previous', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group_tasks.SharedTask')),
            ],
        ),
        migrations.AddField(
            model_name='grouptask',
            name='shared_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_tasks', to='group_tasks.SharedTask'),
        ),
    ]