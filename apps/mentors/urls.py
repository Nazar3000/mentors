from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'mentors'

urlpatterns = [
    path('register/', views.SignUpStep0View.as_view(), name='signup_step0'),
    path('register-step1/', views.SignUpStep1View.as_view(), name='signup_step1'),
    path('register-step2/', views.SignUpStep2View.as_view(), name='signup_step2'),
    path('register-step3/', views.SignUpStep3View.as_view(), name='signup_step3'),
    path('roadmap/', login_required(views.Roadmap.as_view()), name='mentor_roadmap'),
    path('password_reset/', views.MentorPasswordResetView.as_view(), name='password_reset'),
    path('roadmap/step1/', login_required(views.RoadmapStep1.as_view()), name='mentor_roadmap_step1'),
    path('roadmap/step2/', login_required(views.RoadmapStep2.as_view()), name='mentor_roadmap_step2'),
    path('roadmap/step3/', login_required(views.RoadmapStep3.as_view()), name='mentor_roadmap_step3'),
    path('office/', login_required(views.MentorOfficeView.as_view()), name='mentor_office'),
    path('videos/', login_required(views.MentorSchoolVideoListView.as_view()), name='school_videos'),
    path('videos/<int:pk>/', login_required(views.MentorSchoolVideoDetailView.as_view()), name='school_video'),
    path('mentoree/', login_required(views.MentoreeDetailView.as_view()), name='mentoree_detail'),
    path('posts/', login_required(views.PostListView.as_view()), name='posts'),
    path('posts/send-comment/', login_required(views.send_post_comment), name='send_comment'),
    path('meetings/', login_required(views.MeetingListView.as_view()), name='meetings_list'),
    path('settings/', login_required(views.MentorSettingsView.as_view()), name='mentor_settings'),
    path('contacts/', login_required(views.UsefulContactsView.as_view()), name='useful_contacts'),
    path('proforientation/', login_required(views.ProforientationView.as_view()), name='proforientation'),
    path('question/', login_required(views.QuestionView.as_view()), name='question'),

    path('prefooter/report-ssc/', login_required(views.SscReportView.as_view()), name='ssc_report'),
    path('prefooter/assess-ssc/', login_required(views.SscAssessView.as_view()), name='ssc_assess'),
    path('posts/like-post/', login_required(views.like_news_item), name='like_post'),
    path('next-tip/', login_required(views.get_next_tip), name='next_tip'),
    path('notifications/', login_required(views.get_notifications), name='notifications'),
    path('mia_list/', login_required(views.get_mia_list), name='mia_list'),
    path('questionnaire-pdf/<uuid:pk>/', views.QuestionnairePdf.as_view(), name='questionnaire_pdf'),
    path('questionnaire-pdf-print/<uuid:pk>/',
         views.QuestionnairePdf.as_view(filename=None),
         name='questionnaire_pdf_print'),
]
