# Generated by Django 3.2.7 on 2021-11-20 03:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcomment',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='timeStamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
