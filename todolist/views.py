from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todolist.models import Task


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todolist/tasks.html'
    context_object_name = 'tasks'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_count'] = context['tasks'].filter(done=False).count()
        return context

    def get_queryset(self):
        queryset = super(TasksListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todolist/task.html'
    raise_exception = True

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(TaskDetailView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(TaskDetailView, self).get_queryset()
        return queryset.filter(user=self.request.user).select_related('user')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'info', 'done']
    template_name = 'todolist/task-create.html'
    form_class = None
    success_url = reverse_lazy('tasks')
    raise_exception = True

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'info', 'done']
    form_class = None
    template_name = 'todolist/task-update.html'
    success_url = reverse_lazy('tasks')
    raise_exception = True

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(TaskUpdateView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(TaskUpdateView, self).get_queryset()
        return queryset.filter(user=self.request.user).select_related('user')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todolist/task-delete.html'
    success_url = reverse_lazy('tasks')
    raise_exception = True

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(TaskDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(TaskDeleteView, self).get_queryset()
        return queryset.filter(user=self.request.user).select_related('user')
