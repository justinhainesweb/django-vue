from django.db import models
from django.utils import timezone
from django.conf import settings


def plus_month():
    return timezone.now() + timezone.timedelta(days=30)


class Project(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, help_text="Enter project name")
    color = models.CharField(max_length=8, default="#F7DC6F")
    shared = models.BooleanField(default=False, help_text='Will be hidden for everyone')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-name']

    def __str__(self):
        """
        :return:
        """
        return self.name


class Task(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, blank=True, default='''
        What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    ''')
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    final_date = models.DateTimeField(default=plus_month)
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

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
