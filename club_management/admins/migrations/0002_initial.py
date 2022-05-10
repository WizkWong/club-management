# Generated by Django 4.0.4 on 2022-05-10 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_chat_pending_user_task_assigned_user_request'),
        ('admins', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('detail', models.TextField(null=True)),
                ('deadline', models.DateTimeField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request_feedback',
            fields=[
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user_request')),
                ('approval', models.IntegerField(choices=[(2, 'Pending'), (0, 'Reject'), (1, 'Accept')], default=2, max_length=1)),
                ('feedback', models.TextField(default=None, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance_of_user',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.event'),
        ),
        migrations.AddField(
            model_name='attendance_of_user',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='attendance_of_user',
            unique_together={('event', 'user')},
        ),
    ]
