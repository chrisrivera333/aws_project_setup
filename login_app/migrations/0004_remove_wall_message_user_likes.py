# Generated by Django 2.2 on 2021-04-15 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0003_auto_20210414_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wall_message',
            name='user_likes',
        ),
    ]