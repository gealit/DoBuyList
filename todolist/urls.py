from django.urls import path

from todolist.views import TaskDetailView, TasksListView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('tasks/', TasksListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
]
