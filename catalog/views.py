from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Project, Team, Task


def index(request: HttpRequest) -> HttpResponse:
    num_projects = Project.objects.all().count()
    num_teams = Team.objects.all().count()
    num_tasks = Task.objects.all().count()
    context = {
        "num_projects": num_projects,
        "num_teams": num_teams,
        "num_tasks": num_tasks,
    }

    return render(request, "catalog/index.html", context=context)


class ProjectListView(generic.ListView, LoginRequiredMixin):
    model = Project
    # queryset = Project.objects.select_related("team")


class TeamListView(generic.ListView, LoginRequiredMixin):
    model = Team
    # queryset = Team.objects.select_related("user")


class TaskListView(generic.ListView, LoginRequiredMixin):
    model = Task
    paginate_by = 50
    # queryset = Task.objects.select_related("project")


class ProjectDetailView(generic.DetailView, LoginRequiredMixin):
    model = Project


class TeamDetailView(generic.DetailView, LoginRequiredMixin):
    model = Team


class TaskDetailView(generic.DetailView, LoginRequiredMixin):
    model = Task


class ProjectCreateView(generic.CreateView, LoginRequiredMixin):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("catalog:project-list")
    template_name = "catalog/project_form.html"


class TeamCreateView(generic.CreateView, LoginRequiredMixin):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("catalog:team-list")
    template_name = "catalog/team_form.html"


class TaskCreateView(generic.CreateView, LoginRequiredMixin):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("catalog:task-list")
    template_name = "catalog/task_form.html"


class TeamUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Team
    fields = ("name", "members")
    success_url = reverse_lazy("catalog:team-list")
    template_name = "catalog/team_form.html"


class TaskUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Task
    fields = ("name", "description", "status", "assignee", "priority", "due_at", "tags")
    success_url = reverse_lazy("catalog:task-list")
    template_name = "catalog/task_form.html"


class TaskDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = Task
    template_name = "catalog/task_confirm_delete.html"
