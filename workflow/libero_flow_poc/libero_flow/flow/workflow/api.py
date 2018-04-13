from rest_framework import status, viewsets

from workflow.models import (
    Activity,
    Workflow,
)
from workflow.serializers import (
    ActivitySerializer,
    WorkflowSerializer,
)


class ActivityViewSet(viewsets.ModelViewSet):
    model = Activity
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    model = Workflow
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
