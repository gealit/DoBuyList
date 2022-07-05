from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from account.models import Account
from todolist.forms import RoomEnterForm
from todolist.models import Task, Room, RoomTask


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todolist/tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['tasks'].filter(done=False).count()
        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


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

    def get_queryset(self):
        return Room.objects.filter(participants=self.request.user)


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ['name', 'info', 'password']
    form_class = None
    template_name = 'todolist/room-create.html'
    success_url = '/rooms'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        info = form.cleaned_data['info']
        password = form.cleaned_data['password']
        instance = Room.objects.create(name=name, info=info, password=password)
        instance.participants.add(self.request.user)
        return HttpResponseRedirect(self.success_url)


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    fields = ['name', 'info', 'password']
    form_class = None
    template_name = 'todolist/room-update.html'
    success_url = reverse_lazy('rooms')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        print(self.request)
        return super(RoomUpdateView, self).form_valid(form)


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'todolist/room-delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('rooms')


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'todolist/room-detail.html'
    pk_url_kwarg = 'id'


def participants_delete(request, id, pk):
    room = Room.objects.get(id=id)
    user = Account.objects.get(pk=pk)
    room.participants.remove(user)
    return redirect(f'/rooms/{id}/room-detail')


def participants_add(request, id):
    room = Room.objects.get(id=id)
    users = Account.objects.all()
    context = {'room': room, 'users': users}
    return render(request, 'todolist/room-user-add.html', context)


def user_add(request, id, pk):
    room = Room.objects.get(id=id)
    user = Account.objects.get(pk=pk)
    room.participants.add(user)
    return redirect(f'/rooms/{id}/room-detail')


class RoomsSearchListView(LoginRequiredMixin, ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'todolist/rooms-search.html'


class RoomEnter(FormView):
    model = Room
    template_name = 'todolist/room-enter.html'
    form_class = RoomEnterForm
    success_url = reverse_lazy('rooms-search')

    def form_valid(self, form):
        id = self.request.resolver_match.kwargs['id']
        room = Room.objects.get(pk=id)
        if room.password != form.clean_password():
            messages.error(self.request, 'wrong password')
            return redirect(f'/rooms-enter/{id}')
        else:
            room.participants.add(self.request.user)
        return super(RoomEnter, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = Room.objects.get(pk=self.request.resolver_match.kwargs['id'])
        return context


class RoomTasksListView(LoginRequiredMixin, ListView):
    model = Room
    context_object_name = 'room_tasks'
    template_name = 'todolist/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = Room.objects.get(id=self.room_id)
        return context

    def get_queryset(self):
        self.room_id = self.request.resolver_match.kwargs['id']
        return RoomTask.objects.filter(room=self.room_id)


class RoomTaskCreateView(LoginRequiredMixin, CreateView):
    model = RoomTask
    template_name = 'todolist/room-task-create.html'
    fields = ['title', 'info', 'done']
    form_class = None

    def form_valid(self, form):
        room_id = self.request.resolver_match.kwargs['id']
        print(Room.objects.get(id=room_id))
        form.instance.room = Room.objects.get(id=room_id)
        form.instance.user = self.request.user
        return super(RoomTaskCreateView, self).form_valid(form)

    def get_success_url(self):
        room_id = self.request.resolver_match.kwargs['id']
        self.success_url = f'/rooms/{room_id}/'
        return self.success_url


class RoomTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = RoomTask
    fields = ['title', 'info', 'done']
    form_class = None
    template_name = 'todolist/room-task-update.html'

    def get_success_url(self):
        room_id = self.request.resolver_match.kwargs['id']
        self.success_url = f'/rooms/{room_id}/'
        return self.success_url

    def get_queryset(self):
        print(self.request.resolver_match.kwargs)
        return RoomTask.objects.filter(pk=self.request.resolver_match.kwargs['pk'])
