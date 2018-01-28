# Generated by Django 2.0 on 2018-01-28 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grouptask',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='grouptask',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
    ]
