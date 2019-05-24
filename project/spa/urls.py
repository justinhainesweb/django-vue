from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .viewset import ProjectViewSet, TaskViewSet, LikeViewSet


router = DefaultRouter()
router.register(r'project', ProjectViewSet, base_name='Project')
router.register(r'task', TaskViewSet, base_name='Task')
router.register(r'like', LikeViewSet, base_name='Like')


urlpatterns = [
    path('', TemplateView.as_view(template_name='spa/main.html'), name='spa'),
    re_path(r'^(login|register|home)$', TemplateView.as_view(template_name='spa/main.html'), name='spa'),
    path('api/v1/', include(router.urls), name='APIv1')
]
