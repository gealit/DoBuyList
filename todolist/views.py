from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib import messages

from todolist.forms import RegisterForm
from todolist.models import Account, AccountManager, Task, Room, RoomTask
from todolist.token import account_activation_token


class HomeView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'todolist/home.html'


class LoginPage(LoginView):
    template_name = 'todolist/login.html'
    redirect_authenticated_user = True
    next_page = 'home'


class RegisterPage(FormView):
    template_name = 'todolist/register.html'
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
                message = render_to_string('todolist/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject=subject, message=message)
                return HttpResponse('please check your email for account activation')
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
        return redirect('login')
    else:
        return render(request, 'todolist/activation_invalid.html')


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todolist/tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(done=False).count()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todolist/task.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'info', 'done']
    template_name = 'todolist/task-create.html'
    form_class = None
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'info', 'done']
    form_class = None
    template_name = 'todolist/task-update.html'
    success_url = reverse_lazy('tasks')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todolist/task-delete.html'
    success_url = reverse_lazy('tasks')


class RoomsListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'todolist/rooms.html'
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = context['rooms'].filter(participants=self.request.user)
        context['count'] = context['rooms'].count()
        return context


class RoomsSearchListView(LoginRequiredMixin, ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'todolist/rooms-search.html'


class RoomTasksListView(LoginRequiredMixin, ListView):
    model = RoomTask
    context_object_name = 'roomtasks'
    template_name = 'todolist/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roomtasks'] = context['roomtasks'].filter(room__participants=self.request.user)
        return context

