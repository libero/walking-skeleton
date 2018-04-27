from rest_framework import serializers

from workflow.models import (
    Activity,
    Event,
    Workflow,
)


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class WorkflowSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = (
            "instance_id",
            "name",
            "status",
            "created",
            "start_timestamp",
            "end_timestamp",
            "config",
            "input_data",
            "activities",
            "events",
        )


class WorkflowStarterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    input_data = serializers.JSONField(required=False)

    class Meta:
        model = None

    def create(self, instance, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
