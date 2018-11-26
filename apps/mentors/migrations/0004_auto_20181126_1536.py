# Generated by Django 2.1.1 on 2018-11-26 13:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0003_auto_20181114_1813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentorquestionnaire',
            old_name='middle_name',
            new_name='full_name',
        ),
        migrations.AddField(
            model_name='mentorquestionnaire',
            name='actual_address',
            field=models.CharField(default='address', max_length=521),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mentorquestionnaire',
            name='date_of_birth',
            field=models.DateField(default='1980-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mentorquestionnaire',
            name='email',
            field=models.EmailField(default='some@mail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mentorquestionnaire',
            name='phone_number',
            field=models.CharField(default='1', max_length=17, validators=[django.core.validators.RegexValidator(regex='\\+?1?\\d$')]),
            preserve_default=False,
        ),
    ]
