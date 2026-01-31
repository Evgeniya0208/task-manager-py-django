from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
    )

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.get_full_name() or self.get_username()


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:project-detail", args=[str(self.id)])


class Team(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="teams",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        blank=True,
    )

    class Meta:
        unique_together = ("project", "name")
        ordering = ["project__name", "name"]

    def get_absolute_url(self):
        return reverse("catalog:team-detail", args=[str(self.id)])


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class TaskStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):

    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name="tasks",
    )

    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.PROTECT,
        related_name="tasks",
    )
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.assignee_id and self.project_id:
            ok = Team.objects.filter(
                project_id=self.project_id, members__id=self.assignee_id
            ).exists()
            if not ok:
                raise ValidationError(
                    {"assignee": "Assignee must be a member of a team in this project."}
                )

    def get_absolute_url(self):
        return reverse("catalog:task-detail", args=[str(self.id)])
