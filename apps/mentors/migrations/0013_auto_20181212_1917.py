# Generated by Django 2.1.1 on 2018-12-12 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0012_auto_20181212_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorquestionnaire',
            name='home_family_members_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mentorquestionnaire',
            name='home_type',
            field=models.CharField(blank=True, choices=[('APARTMENT', 'квартира'), ('PRIVATE_HOUSE', 'приватний будинок'), ('RENTED', 'орендоване житло')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='mentorquestionnaire',
            name='people_per_room',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='mentorquestionnaire',
            name='pets_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mentorquestionnaire',
            name='room_count',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
    ]