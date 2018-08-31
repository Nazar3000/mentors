# Generated by Django 2.1 on 2018-08-31 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0014_auto_20180830_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorSchoolVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('video', models.FileField(upload_to='govern_users/mentor_school_videos')),
                ('watched_by', models.ManyToManyField(to='users.Mentor')),
            ],
        ),
        migrations.CreateModel(
            name='MentorTip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('content', models.TextField()),
            ],
        ),
    ]
