from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Project, Task, Like
from .serializers import ProjectSerializer, TaskSerializer, LikeSerializer
from .pagination import DefaultResultSetPagination


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = DefaultResultSetPagination

    def list(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        self.queryset = self.queryset.filter(Q(author=self.request.user) | Q(shared=True))
        project_serializer = ProjectSerializer(self.queryset, many=True, context={'request': request})

        tasks = Task.objects.select_related('project').filter(project__in=self.queryset.only('id')).\
            prefetch_related('like_set').order_by('-done', 'final_date')

        task_serializer = TaskSerializer(self.paginate_queryset(tasks), many=True, context={'request': request})

        return Response({
            'projects': project_serializer.data,
            'tasks': self.paginator.get_paginated_data(task_serializer.data),
        })

    def perform_create(self, serializer):
        """
        :param serializer:
        :return:
        """
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        project_id = self.request.data.get('id', 0)
        exists = Project.objects.filter(author=self.request.user, id=project_id).exists()

        # if I am the creator
        if exists:
            serializer = TaskSerializer(
                instance=self.get_object(),
                context={'request': request},
                data={
                    'content': self.request.data.get('content'),
                    'name': self.request.data.get('name')
                }
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        project = self.get_object()
        incomplete_tasks_count = project.task_set.filter(done=False).count()

        if not incomplete_tasks_count:
            self.perform_destroy(project)
            message = 'The project has been deleted'
        else:
            message = 'There are incomplete tasks'

        return Response(data={
            'message': message,
            'incomplete_tasks_count': incomplete_tasks_count
        }, )


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.select_related('project').prefetch_related('like_set').all().order_by('-final_date')
    serializer_class = TaskSerializer
    authentication_class = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = DefaultResultSetPagination

    def list(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        filter_state = self.request.query_params.get('filter_state', None)
        filter_period = self.request.query_params.get('filter_period', None)
        project_id = int(self.request.query_params.get('project_id', 0))

        if project_id:
            self.queryset = self.queryset.filter(project_id=project_id)
        else:
            project_qs = Project.objects.filter(Q(author=self.request.user) | Q(shared=True)).only('id')
            self.queryset = self.queryset.filter(project__in=project_qs)

        if filter_state == 'completed':
            self.queryset = self.queryset.filter(done=True)
        elif filter_state == 'active':
            self.queryset = self.queryset.filter(done=False)

        if filter_period == 'today':
            self.queryset = self.queryset.filter(final_date__range=[timezone.now(), timezone.now() + timedelta(1)])
        elif filter_period == 'last_week':
            self.queryset = self.queryset.filter(final_date__range=[timezone.now(), timezone.now() + timedelta(7)])

        self.queryset = self.queryset.order_by('-done', 'final_date')

        paginate_queryset = self.paginate_queryset(self.queryset)
        task_serializer = TaskSerializer(paginate_queryset, many=True, context={'request': request})

        return self.get_paginated_response(task_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        task = self.get_object()
        task_id = task.id

        self.perform_destroy(task)

        return Response(data={'id': task_id}, )


class LikeViewSet(viewsets.ModelViewSet):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        like_id = 0
        task_id = self.request.data.get('task_id', 0)
        exists = Like.objects.filter(user=self.request.user, task_id=task_id).exists()

        if not exists:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            like_id = self.perform_create(serializer)

        return Response(data={
            'like_id': like_id
        }, )

    def perform_create(self, serializer):
        """
        :param serializer:
        :return:
        """
        return serializer.save(
            user=self.request.user,
            task_id=self.request.data.get('task_id', 0)
        ).id

    def perform_destroy(self, instance):
        """
        :param instance:
        :return:
        """
        instance.delete()
