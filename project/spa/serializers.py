from rest_framework import serializers
from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializer for Project model """

    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'color', 'created', 'task_count', )
        read_only_fields = ('id', 'author', 'created', )

    @staticmethod
    def get_task_count(project):
        """
        :param project: self.object
        :return: integer
        """
        return project.task_set.count()


class TaskSerializer(serializers.ModelSerializer):
    """ Serializer for Task model """

    project_id = serializers.IntegerField(write_only=True)
    project = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'content', 'created', 'final_date', 'done', 'priority', 'project_id', 'project', )
        read_only_fields = ('project', 'project_id', )

    @staticmethod
    def get_project(task):
        return {
            'id': task.project.id,
            'name': task.project.name,
            'color': task.project.color,
        }
