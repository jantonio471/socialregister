# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Submit

from django import forms

from socialregister.users.models import User


class BaseRegisterForm(object):

    def clean(self):
        if 'password' not in self.cleaned_data:
            raise forms.ValidationError("Enter a password.")
        elif 'confirm_password' not in self.cleaned_data:
            raise forms.ValidationError("Enter your password (again)")
        elif (
            self.cleaned_data['confirm_password'] !=
            self.cleaned_data['password']
             ):
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data


class CompleteDataForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            message = """
                <p class='errorlist'>Hay un usuario registrado con este correo
                <a href="/users/logout/">Ingresa con otra cuenta</a></p>
            """
            raise forms.ValidationError(message)
        return email


class SetPasswordForm(BaseRegisterForm, forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['password']
        widgets = {'password': forms.PasswordInput()}


class RegisterForm(BaseRegisterForm, forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email", "username", "password"]
        widgets = {'password': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                        href="{% url "home" %}">Cancel</a> """),
                Submit('save', 'Guardar'),
            )
        )
