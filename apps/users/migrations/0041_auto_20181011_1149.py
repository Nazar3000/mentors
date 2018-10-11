# Generated by Django 2.1.1 on 2018-10-11 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_auto_20181011_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='status',
            field=models.CharField(choices=[('PASSED_INFO_MEETING', 'Пройшов інфо-зустріч'), ('PASSED_TRAINING', 'Пройшов тренінг'), ('REJECTED_TO_BE_MENTOR', 'Відмовився бути наставником'), ('PASSED_INTERVIEW_WITH_PSYCHOLOGIST', 'Пройшов співбесіду з психологом'), ('SELECTED_FOR_MENTOREE', 'Підібраний для вихованця'), ('ACTIVE_INTERACTION', 'Активна взаємодія'), ('PAIR_DISBANDED', 'Пара розформована')], max_length=64),
        ),
    ]
