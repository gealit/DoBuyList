from django.contrib.auth.views import LogoutView
from django.urls import path

from todolist.views import HomeView, LoginPage, RegisterPage, activate, TaskDetailView, TasksListView, TaskCreateView, \
    TaskUpdateView, TaskDeleteView, RoomsListView, RoomsSearchListView, RoomTasksListView, RoomTaskCreateView, \
    RoomDetailView, RoomTaskUpdateView, RoomCreateView, RoomDeleteView, RoomUpdateView, participants_delete, \
    participants_add, user_add

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('tasks/', TasksListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('rooms/', RoomsListView.as_view(), name='rooms'),
    path('room-create/', RoomCreateView.as_view(), name='room-create'),
    path('room-update/<int:id>/', RoomUpdateView.as_view(), name='room-update'),
    path('room-user-delete/<int:id>/<int:pk>/', participants_delete, name='room-user-delete'),
    path('room-user-add/<int:id>/', participants_add, name='room-user-add'),
    path('user-add/<int:id>/<int:pk>/', user_add, name='user-add'),
    path('room-delete/<int:id>/', RoomDeleteView.as_view(), name='room-delete'),
    path('rooms-search/', RoomsSearchListView.as_view(), name='rooms-search'),
    path('rooms/<int:id>/', RoomTasksListView.as_view(), name='room'),
    path('rooms/<int:id>/room-detail/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:id>/room-task-create/', RoomTaskCreateView.as_view(), name='room-task-create'),
    path('rooms/<int:id>/room-task-update/<int:pk>/', RoomTaskUpdateView.as_view(), name='room-task-update'),
]
