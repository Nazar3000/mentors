# Generated by Django 2.1.1 on 2018-12-05 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_services', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PublicOrganizationMasterKey',
            new_name='PublicServiceMasterKey',
        ),
        migrations.RenameModel(
            old_name='PublicOrganizationVideo',
            new_name='PublicServiceVideo',
        ),
    ]