from django.urls import path, include

from rest_framework import routers

from workflow.api import (
    ActivityViewSet,
    WorkflowViewSet,
)

router_v1 = routers.DefaultRouter()

router_v1.register('activities', ActivityViewSet, base_name='activity')
router_v1.register('workflows', WorkflowViewSet, base_name='workflow')


urlpatterns = [
    path('api/v1/', include((router_v1.urls, 'api_v1'))),  # namespace='api_v1'
]
