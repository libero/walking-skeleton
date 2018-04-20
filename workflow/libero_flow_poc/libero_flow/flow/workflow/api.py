import json

from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from workflow.utils import start_workflow

from workflow.models import (
    Activity,
    Event,
    Workflow,
)
from workflow.serializers import (
    ActivitySerializer,
    EventSerializer,
    WorkflowSerializer,
    WorkflowStarterSerializer,
)


class ActivityViewSet(viewsets.ModelViewSet):
    model = Activity
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class EventViewSet(viewsets.ModelViewSet):
    model = Event
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    model = Workflow
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer


class WorkflowStarterViewSet(viewsets.ViewSet):

    @staticmethod
    def create(request, *args, **kwargs):
        workflow_name = request.data.get('name', None)
        input_data = json.dumps(request.data.get('input_data', {}))

        serializer = WorkflowStarterSerializer(data={'name': workflow_name, "input_data": input_data})

        try:
            if serializer.is_valid(raise_exception=True):
                start_workflow(name=serializer.data['name'],
                               input_data=json.loads(serializer.data['input_data']))

                return Response({"message": "Start Workflow request sent"}, status=status.HTTP_200_OK)

        except ValidationError as err:
            return Response({"message": f"{err.detail}"}, status=status.HTTP_400_BAD_REQUEST)
