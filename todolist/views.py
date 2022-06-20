from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import ListView, FormView


class HomeView(ListView):
    model = User
    template_name = 'todolist/home.html'


class LoginPage(LoginView):
    template_name = 'todolist/login.html'
    redirect_authenticated_user = True
    next_page = 'home'


class RegisterPage(FormView):
    template_name = 'todolist/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage, self).get(*args, **kwargs)

