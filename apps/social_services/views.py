from django.views.generic import ListView

from users.models import Mentor


class MentorsView(ListView):
    template_name = 'social_services/mentors.html'
    queryset = Mentor.objects.all()
