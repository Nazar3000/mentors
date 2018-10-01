# Generated by Django 2.1.1 on 2018-10-01 07:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0037_proforientation_related_mentor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorlicencekey',
            name='key',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex='\\d{3}[a-zA-z]{3}')]),
        ),
    ]