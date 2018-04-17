import pytest

from rest_framework.exceptions import ValidationError

from workflow.serializers import WorkflowStarterSerializer


@pytest.mark.parametrize('data',
                         [
                             {"name": "FooBarWorkflow",
                              "input_data": {"timeout": 300}},
                             {"name": "FooBarWorkflow",
                              "input_data": {}},
                         ])
def test_can_validate_workflow_starter_data(data):
    serializer = WorkflowStarterSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.parametrize('data',
                         [
                             {"name": None, "input_data": {"timeout": 300}},
                             {"name": None, "input_data": None},
                             {"input_data": {"timeout": 300}},
                         ])
def test_will_fail_workflow_starter_validation(data):
    serializer = WorkflowStarterSerializer(data=data)

    with pytest.raises(ValidationError):
        assert serializer.is_valid(raise_exception=True)
