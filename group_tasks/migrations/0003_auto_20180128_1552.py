# Generated by Django 2.0 on 2018-01-28 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group_tasks', '0002_auto_20180128_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedtask',
            name='previous',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='group_tasks.SharedTask'),
        ),
    ]
