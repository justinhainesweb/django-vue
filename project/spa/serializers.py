from rest_framework import serializers
from .models import Project, Task, Like


class ProjectSerializer(serializers.ModelSerializer):

    is_my = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'color', 'task_count', )
        read_only_fields = ('id', 'created_at', 'author', 'created', )

    @staticmethod
    def get_task_count(project):
        """
        :param project: self.object
        :return: integer
        """
        return project.task_set.count()


class TaskSerializer(serializers.ModelSerializer):

    project_id = serializers.IntegerField(write_only=True)
    project = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'content', 'final_date', 'done', 'priority', 'project_id',
                  'project', 'like_count', 'liked', 'shared', 'is_my', )
        read_only_fields = ('id', 'created_at', 'project', 'project_id', 'like_count', 'liked', 'shared', 'is_my', )

    def get_is_my(self, task):
        """
        :param task:
        :return: true is it's my task
        """
        return True if task.user == self.context['request'].user else False

    def get_liked(self, task):
        """
        :param task:
        :return:
        """
        try:
            liked = task.like_set.get(user=self.context['request'].user)
            return liked.id
        except Like.DoesNotExist:
            return False

    @staticmethod
    def get_like_count(task):
        """
        :param task: self.object
        :return: integer
        """
        return task.like_set.count()

    @staticmethod
    def get_project(task):
        return {
            'id': task.project.id,
            'name': task.project.name,
            'color': task.project.color,
        }


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'task', )
        read_only_fields = ('user', 'task', )
