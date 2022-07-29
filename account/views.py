from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView

from account.forms import RegisterForm
from account.models import Account
from account.token import account_activation_token


class HomeView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'account/home.html'


class LoginPage(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    next_page = 'home'


class RegisterPage(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password2'])
        user.save()
        messages.success(self.request, 'Welcome to the application!')
        if user is not None:
            if not user.is_active:
                current_site = get_current_site(self.request)
                subject = 'Account activating'
                message = render_to_string('account/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject=subject, message=message)
                return HttpResponse('<h1>Please check your email for account activation</h1>')
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage, self).get(*args, **kwargs)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login', permanent=True)
    else:
        return render(request, 'account/activation_invalid.html')
