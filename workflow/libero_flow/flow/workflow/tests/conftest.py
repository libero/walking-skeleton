import pytest

from workflow.models import Activity, Workflow


@pytest.fixture
@pytest.mark.django_db
def workflow():
    return Workflow.objects.create(name='FooWorkflow', config={"foo": "bar"})


@pytest.fixture
@pytest.mark.django_db
def activity(workflow):
    return Activity.objects.create(name='FooActivity', config={"foo": "bar"},
                                   workflow=workflow)
