from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, FormView, DetailView, ListView
from .forms import SignUpStep0Form, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import SocialServiceVideo, Material, MaterialCategory
from users.models import Mentor
from django.core.files import File

class SignUpFormView(FormView):
    template_name = 'social_service/ssc_register.html'
    form_class = SignUpStep0Form

    def form_valid(self, form):
        form.save()
        return redirect('social_service:video')


class LoginView(FormView):
    template_name = 'social_service/ssc_login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
        else:
            messages.error(self.request, 'Невірний пароль.')
            return redirect('social_service:ssc_login')
        return redirect('/')


class MainPageView(TemplateView):
    template_name = 'social_service/ssc_main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['main_video'] = SocialServiceVideo.objects.filter(page=1).first()
        return context


class VideoMentorView(TemplateView):
    template_name = 'social_service/ssc_video_mentor.html'

    def get_context_data(self, **kwargs):
        context = super(VideoMentorView, self).get_context_data(**kwargs)
        context['mentor_video'] = SocialServiceVideo.objects.filter(page=2).first()
        return context


class MentorCardView(DetailView):
    model = Mentor
    template_name = 'social_service/ssc_mentor_card.html'


class MaterialView(ListView):
    model = Material
    template_name = 'social_service/ssc_material.html'

    def get_context_data(self, **kwargs):
        context = super(MaterialView, self).get_context_data(**kwargs)
        context['categories'] = MaterialCategory.objects.all()
        return context


def download_file(request, material_id):
    material = Material.objects.get(id=material_id)
    filename = material.file.name.split('/')[-1]
    response = HttpResponse(material.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
