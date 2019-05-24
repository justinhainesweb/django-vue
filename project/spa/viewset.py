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

        tasks = Task.objects.select_related('project').filter(
            project__in=self.queryset.only('id'),
            final_date__range=[
                timezone.now(), timezone.now() + timedelta(days=30)
            ]).prefetch_related('like_set').order_by('priority').order_by('-done', 'final_date')

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

    queryset = Task.objects.select_related('project').prefetch_related('like_set').all()
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
        author = self.request.user
        paginate_queryset = self.paginate_queryset(self.queryset)

        filter_state = self.request.query_params.get('filter_state', None)
        filter_period = self.request.query_params.get('filter_period', None)
        project_id = int(self.request.query_params.get('project_id', 0))

        if project_id:
            paginate_queryset = paginate_queryset.filter(project_id=project_id)
        else:
            paginate_queryset = paginate_queryset.filter(project__author=author)

        if filter_state == 'completed':
            paginate_queryset = paginate_queryset.filter(done=True)
        elif filter_state == 'active':
            paginate_queryset = paginate_queryset.filter(done=False)

        if filter_period == 'today':
            paginate_queryset = paginate_queryset.filter(final_date__range=[date.today(), date.today() + timedelta(1)])
        elif filter_period == 'last_week':
            paginate_queryset = paginate_queryset.filter(final_date__range=[date.today(), date.today() + timedelta(7)])

        paginate_queryset = paginate_queryset.order_by('final_date').order_by('priority')

        task_serializer = TaskSerializer(paginate_queryset, many=True, context={'request': request})
        return self.get_paginated_response(task_serializer.data)
