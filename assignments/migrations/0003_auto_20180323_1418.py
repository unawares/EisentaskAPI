# Generated by Django 2.0 on 2018-03-23 14:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_auto_20180323_1124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ('created', 'updated')},
        ),
        migrations.AddField(
            model_name='assignment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignment',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
