# Generated by Django 3.2.3 on 2021-05-22 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='username',
            new_name='user',
        ),
    ]
