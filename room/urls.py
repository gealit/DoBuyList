from django.urls import path

from room.views import RoomCreateView, RoomsListView, RoomUpdateView, participants_delete, participants_add, user_add, \
    RoomDeleteView, RoomsSearchListView, RoomEnter, RoomTasksListView, RoomDetailView, RoomTaskCreateView, \
    RoomTaskUpdateView, RoomTaskDeleteView

urlpatterns = [
    path('rooms/', RoomsListView.as_view(), name='rooms'),
    path('room-create/', RoomCreateView.as_view(), name='room-create'),
    path('room-update/<int:id>/', RoomUpdateView.as_view(), name='room-update'),
    path('room-user-delete/<int:id>/<int:pk>/', participants_delete, name='room-user-delete'),
    path('room-user-add/<int:id>/', participants_add, name='room-user-add'),
    path('user-add/<int:id>/<int:pk>/', user_add, name='user-add'),
    path('room-delete/<int:id>/', RoomDeleteView.as_view(), name='room-delete'),
    path('rooms-search/', RoomsSearchListView.as_view(), name='rooms-search'),
    path('rooms-enter/<int:id>/', RoomEnter.as_view(), name='room-enter'),
    path('rooms/<int:id>/', RoomTasksListView.as_view(), name='room'),
    path('rooms/<int:id>/room-detail/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:id>/room-task-create/', RoomTaskCreateView.as_view(), name='room-task-create'),
    path('rooms/<int:id>/room-task-update/<int:pk>/', RoomTaskUpdateView.as_view(), name='room-task-update'),
    path('rooms/<int:id>/room-task-delete/<int:pk>/', RoomTaskDeleteView.as_view(), name='room-task-delete'),
]
