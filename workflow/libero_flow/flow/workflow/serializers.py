from rest_framework import serializers

from workflow.models import (
    Activity,
    Workflow,
)


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'


class WorkflowSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = (
            "instance_id",
            "name",
            "status",
            "start_timestamp",
            "end_timestamp",
            "config",
            "activities",
        )
