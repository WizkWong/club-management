# Generated by Django 4.0.4 on 2022-05-13 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_task_assigned_task_task_assigned_user_chat_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_request',
            name='title',
            field=models.CharField(default='Request 1', max_length=100),
            preserve_default=False,
        ),
    ]
