# Generated by Django 4.0.4 on 2022-06-08 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_request_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='user',
        ),
        migrations.DeleteModel(
            name='Pending_user',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
    ]
