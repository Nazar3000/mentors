# Generated by Django 2.1.1 on 2018-11-25 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_services', '0005_basesocialservicecenter_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basesocialservicecenter',
            name='service',
        ),
    ]