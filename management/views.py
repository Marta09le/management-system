from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic

from apps.accounts.forms import UserLoginForm


class StartView(generic.TemplateView):
    template_name = 'start.html'


class ChooseWhoView(generic.TemplateView):
    template_name = 'choose_who.html'

