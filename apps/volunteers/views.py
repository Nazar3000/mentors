from django.views.generic import CreateView

from .forms import VolunteerForm


class VolunteerSignUpView(CreateView):
    # TODO: find what to do with missing password fields
    template_name = 'users/volunteer_signup.html'
    form_class = VolunteerForm
    success_url = '/'
