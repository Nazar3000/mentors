# Generated by Django 2.1 on 2018-09-03 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0010_auto_20180830_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default='content'),
            preserve_default=False,
        ),
    ]