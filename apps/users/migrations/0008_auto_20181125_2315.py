# Generated by Django 2.1.1 on 2018-11-25 21:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20181121_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialservicecenter',
            name='phone_numbers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=None),
        ),
    ]
