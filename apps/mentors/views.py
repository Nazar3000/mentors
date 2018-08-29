from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView

from users.models import Mentor
from .forms import SignUpStep0Form, SignUpStep1Form, SignUpStep3Form


class SignUpStep0View(FormView):
    template_name = 'mentors/signup_step0.html'
    form_class = SignUpStep0Form
    success_url = reverse_lazy('mentors:signup_step1')

    def form_valid(self, form):
        self.request.session['mentor_data'] = form.cleaned_data
        return HttpResponseRedirect(self.get_success_url())


class SignUpStep1View(FormView):
    template_name = 'mentors/signup_step1.html'
    form_class = SignUpStep1Form
    success_url = reverse_lazy('mentors:signup_step2')

    def get_initial(self):
        initial = super().get_initial()
        if 'mentor_data' in self.request.session.keys():
            print(self.request.session['mentor_data']['email'])
            initial['email'] = self.request.session['mentor_data']['email']
        return initial

    def form_valid(self, form):
        user = form.save()
        if 'mentor_data' in self.request.session.keys():
            mentor = Mentor(**self.request.session['mentor_data'])
            mentor.user = user
            mentor.save()
        else:
            return redirect('mentors:signup_step0')
        return HttpResponseRedirect(self.get_success_url())


class SignUpStep2View(TemplateView):
    template_name = 'mentors/signup_step2.html'


class SignUpStep3View(FormView):
    # TODO: complete this view
    template_name = 'mentors/signup_step3.html'
    form_class = SignUpStep3Form
    success_url = '/'


class MentorRoadmap(TemplateView):
    template_name = 'mentors/mentor_roadmap.html'


class MentorOfficeView(DetailView):
    # TODO: complete this view
    template_name = 'mentors/mentor_office.html'
    model = Mentor
