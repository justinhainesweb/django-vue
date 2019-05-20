from django.db import models
from django.utils import timezone
from django.conf import settings


class Project(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, help_text="Enter project name")
    color = models.CharField(max_length=8, default="fff")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """
        :return:
        """
        return self.name


class Task(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    final_date = models.DateTimeField(default=timezone.now)
    priority = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Task of project'
        verbose_name_plural = 'Tasks of project'
        ordering = ['-final_date']

    def __str__(self):
        """
        :return:
        """
        return self.content[:50] + '...'


class Like(models.Model):

    post = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
