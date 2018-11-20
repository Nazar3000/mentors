# Generated by Django 2.1.1 on 2018-11-12 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('mentors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proforientation',
            name='related_mentor',
            field=models.ManyToManyField(to='users.Mentor'),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Mentor'),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='mentors.Post'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='users.Mentor'),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(to='users.Mentor'),
        ),
        migrations.AddField(
            model_name='mentorsocialservicecenterdata',
            name='mentor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='social_service_center_data', to='users.Mentor'),
        ),
        migrations.AddField(
            model_name='mentorquestionnairejob',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentors.MentorQuestionnaire'),
        ),
        migrations.AddField(
            model_name='mentorquestionnairefamilymember',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentors.MentorQuestionnaire'),
        ),
        migrations.AddField(
            model_name='mentorquestionnaireeducation',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentors.MentorQuestionnaire'),
        ),
        migrations.AddField(
            model_name='mentorquestionnairechildrenworkexperience',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentors.MentorQuestionnaire'),
        ),
        migrations.AddField(
            model_name='mentorquestionnaire',
            name='mentor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire', to='users.Mentor'),
        ),
        migrations.AddField(
            model_name='mentoree',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Organization'),
        ),
        migrations.AddField(
            model_name='meetingimage',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentors.Meeting'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='performer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='users.Mentor'),
        ),
    ]