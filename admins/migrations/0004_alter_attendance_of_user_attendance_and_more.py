# Generated by Django 4.0.4 on 2022-05-13 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_alter_attendance_of_user_attendance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance_of_user',
            name='attendance',
            field=models.IntegerField(choices=[(2, 'Late'), (0, 'Absent'), (1, 'Present')], default=0),
        ),
        migrations.AlterField(
            model_name='request_feedback',
            name='approval',
            field=models.IntegerField(choices=[(1, 'Accept'), (2, 'Pending'), (0, 'Reject')], default=2),
        ),
    ]
