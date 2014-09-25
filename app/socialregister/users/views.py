# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import FormView

from social.apps.django_app.default.models import UserSocialAuth

from socialregister.users.forms import CompleteDataForm, RegisterForm


class UserCompleteData(FormView):
    form_class = CompleteDataForm
    template_name = "users/complete_data.html"

    def form_valid(self, form):
        email = form.data['email']
        self.request.user.email = email
        self.request.user.username = email
        self.request.user.save()
        return redirect('/')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.email:
            return redirect('/')
        return super(UserCompleteData, self).dispatch(*args, **kwargs)


class UserDeleteConection(View):

    def post(self, *args, **kwargs):
        UserSocialAuth.objects.get(
            user_id=self.request.user.id, provider=kwargs['provider']).delete()
        return redirect('/')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDeleteConection, self).dispatch(*args, **kwargs)


class UserLogin(FormView):
    form_class = AuthenticationForm
    template_name = "users/form.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect("/")

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('home')
        return super(UserLogin, self).dispatch(*args, **kwargs)


def user_logout(request):
    return logout(request, next_page="users:login")


class UserRegister(FormView):
    form_class = RegisterForm
    success_url = '/'
    template_name = "users/register.html"

    def form_valid(self, form):
        u = form.save()
        u.username = u.email
        u.set_password(form.cleaned_data['password'])
        u.save()
        return redirect("users:login")

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('home')
        return super(UserRegister, self).dispatch(*args, **kwargs)
