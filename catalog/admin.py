from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import Position, TaskStatus, Worker, Project, Team, TaskType


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display + (
        "position",
        "teams_list",
    )
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)

    def teams_list(self, obj):
        return ", ".join(team.name for team in obj.teams.all())

    teams_list.short_description = "Teams"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "project",
        "members_list",
    ]

    def members_list(self, obj):
        return ", ".join(user.username for user in obj.members.all())

    members_list.short_description = "Members"


admin.site.register(Project)
admin.site.register(Position)
admin.site.register(TaskStatus)
admin.site.register(TaskType)
