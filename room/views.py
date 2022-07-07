from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView

from account.models import Account
from room.forms import RoomEnterForm
from room.models import Room, RoomTask


class RoomsListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'room/rooms.html'
    context_object_name = 'rooms'
    raise_exception = True

    def get_queryset(self):
        return Room.objects.filter(participants=self.request.user)


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ['name', 'info', 'password']
    form_class = None
    template_name = 'room/room-create.html'
    success_url = '/rooms'
    raise_exception = True

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
    template_name = 'room/room-update.html'
    success_url = reverse_lazy('rooms')
    pk_url_kwarg = 'id'
    raise_exception = True

    def get_queryset(self):
        room_id = self.request.resolver_match.kwargs['id']
        return Room.objects.filter(id=room_id).prefetch_related('participants')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(RoomUpdateView, self).get_object()
        if not self.request.user in obj.participants.all():
            raise Http404
        return obj


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'room/room-delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('rooms')
    raise_exception = True


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'room/room-detail.html'
    pk_url_kwarg = 'id'
    raise_exception = True


def participants_delete(request, id, pk):
    room = Room.objects.get(id=id)
    if request.user in room.participants.all():
        user = Account.objects.get(pk=pk)
        room.participants.remove(user)
    return redirect(f'/rooms/{id}/room-detail')


def participants_add(request, id):
    room = Room.objects.get(id=id)
    if not request.user in room.participants.all():
        return redirect(f'/rooms-enter/{id}/')
    participants = room.participants.all()
    users = Account.objects.all()
    context = {'room': room, 'users': users, 'participants': participants}
    return render(request, 'room/room-user-add.html', context)


def user_add(request, id, pk):
    room = Room.objects.get(id=id)
    if request.user in room.participants.all():
        user = Account.objects.get(pk=pk)
        room.participants.add(user)
    return redirect(f'/rooms/{id}/room-detail')


class RoomsSearchListView(LoginRequiredMixin, ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'room/rooms-search.html'
    raise_exception = True

    def get_queryset(self):
        return Room.objects.all().prefetch_related('participants')


class RoomEnter(LoginRequiredMixin, FormView):
    model = Room
    template_name = 'room/room-enter.html'
    form_class = RoomEnterForm
    raise_exception = True

    def form_valid(self, form):
        room_id = self.request.resolver_match.kwargs['id']
        room = Room.objects.get(pk=room_id)
        if room.password != form.clean_password():
            messages.error(self.request, 'wrong password')
            return redirect(f'/rooms-enter/{room_id}')
        else:
            room.participants.add(self.request.user)
        return super(RoomEnter, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = Room.objects.get(pk=self.request.resolver_match.kwargs['id'])
        return context

    def get_success_url(self):
        return f'/rooms/{self.room_id}'


class RoomTasksListView(LoginRequiredMixin, ListView):
    model = RoomTask
    context_object_name = 'room_tasks'
    template_name = 'room/room.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = Room.objects.get(id=self.room_id)
        return context

    def get_queryset(self):
        self.room_id = self.request.resolver_match.kwargs['id']
        return RoomTask.objects.filter(room=self.room_id)


class RoomTaskCreateView(LoginRequiredMixin, CreateView):
    model = RoomTask
    template_name = 'room/room-task-create.html'
    fields = ['title', 'info', 'done']
    form_class = None
    raise_exception = True

    def form_valid(self, form):
        room_id = self.request.resolver_match.kwargs['id']
        form.instance.room = Room.objects.get(id=room_id)
        form.instance.user = self.request.user
        return super(RoomTaskCreateView, self).form_valid(form)

    def get_success_url(self):
        room_id = self.request.resolver_match.kwargs['id']
        self.success_url = f'/rooms/{room_id}/'
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = self.request.resolver_match.kwargs['id']
        context['room'] = Room.objects.get(id=room_id)
        return context


class RoomTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = RoomTask
    fields = ['title', 'info', 'done']
    form_class = None
    template_name = 'room/room-task-update.html'
    raise_exception = True

    def get_success_url(self):
        room_id = self.request.resolver_match.kwargs['id']
        self.success_url = f'/rooms/{room_id}/'
        return self.success_url

    def get_queryset(self):
        return RoomTask.objects.filter(pk=self.request.resolver_match.kwargs['pk'])


class RoomTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = RoomTask
    template_name = 'room/room-task-delete.html'
    raise_exception = True

    def get_success_url(self):
        room_id = self.request.resolver_match.kwargs['id']
        self.success_url = f'/rooms/{room_id}'
        return self.success_url


