# Generated by Django 2.1.1 on 2018-11-18 21:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20181118_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicservice',
            name='licence',
            field=models.CharField(blank=True, max_length=7, validators=[django.core.validators.RegexValidator(regex='[A-Z]{4}\\s{1}\\d{2}')]),
        ),
    ]
