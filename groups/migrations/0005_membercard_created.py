# Generated by Django 2.0 on 2018-01-28 09:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_remove_membercard_is_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='membercard',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]