# Generated by Django 2.1.1 on 2018-12-07 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20181205_1752'),
        ('mentors', '0010_auto_20181129_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Mentor')),
            ],
        ),
    ]
