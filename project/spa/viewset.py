from datetime import date, timedelta
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        author = self.request.user

        projects = Project.objects.filter(author=author).order_by('-name')
        project_serializer = ProjectSerializer(projects, many=True)

        tasks = Task.objects.filter(project__author=author, done=False, final_date__range=[
                date.today(), date.today() + timedelta(1)  # today
            ]).order_by('priority').order_by('-done', 'final_date')[:100]

        task_serializer = TaskSerializer(tasks, many=True)

        return Response({
            'projects': project_serializer.data,
            'tasks': task_serializer.data,
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

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_class = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        author = self.request.user
        queryset = Task.objects.all()

        filter_state = self.request.query_params.get('filter_state', None)
        filter_period = self.request.query_params.get('filter_period', None)
        project_id = int(self.request.query_params.get('project_id', 0))

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        else:
            queryset = queryset.filter(project__author=author)

        if filter_state == 'completed':
            queryset = queryset.filter(done=True)
        elif filter_state == 'active':
            queryset = queryset.filter(done=False)

        if filter_period == 'today':
            queryset = queryset.filter(final_date__range=[date.today(), date.today() + timedelta(1)])
        elif filter_period == 'last_week':
            queryset = queryset.filter(final_date__range=[date.today(), date.today() + timedelta(7)])

        queryset = queryset.order_by('final_date').order_by('priority')

        task_serializer = TaskSerializer(queryset, many=True)
        return Response(task_serializer.data)
