# Generated by Django 2.0 on 2018-01-27 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20180127_0815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='creator',
            new_name='admin',
        ),
    ]