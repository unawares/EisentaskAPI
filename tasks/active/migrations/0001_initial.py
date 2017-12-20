# Generated by Django 2.0 on 2017-12-20 15:40

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('progress', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('activities', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('interruptions', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='active_task', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]