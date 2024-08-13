from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
        


class CustomPasswordResetForm(PasswordResetForm): # das hier wäre z.b. die zusätzlichen validierungs möglichkeiten wen man das aktiviert. hier wird das protokoll angepasst damit der nicht die standart methode von django nimmt
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            self.send_reset_email(user, request)

    def send_reset_email(self, user, request):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        subject = "Password reset on 127.0.0.1:8000"
        from_email = 'webmaster@localhost'
        to_email = user.email

        text_content = "Click the link below to reset your password."
        html_content = render_to_string('password_reset_email.html', {
            'protocol': request.scheme,
            'domain': request.get_host(),
            'uid': uid,
            'token': token,
            'user': user,
            'site_name': get_current_site(request).name,
        })

        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()