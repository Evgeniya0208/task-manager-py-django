from django.urls import path

from catalog.views import (
    index,
    ProjectListView,
    TeamListView,
    TaskListView,
    ProjectDetailView,
    TaskDetailView,
    TeamDetailView,
    ProjectCreateView,
    TeamCreateView,
    TaskCreateView,
    TeamUpdateView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("projects/<int:pk>", ProjectDetailView.as_view(), name="project-detail"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("teams/<int:pk>", TeamDetailView.as_view(), name="team-detail"),
    path("projects/create", ProjectCreateView.as_view(), name="project-create"),
    path("teams/create", TeamCreateView.as_view(), name="team-create"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path("teams/<int:pk>/update", TeamUpdateView.as_view(), name="team-update"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"),
]

app_name = "catalog"
