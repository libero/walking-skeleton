import uuid

from django.db import models


CANCELLED = 'Cancelled'
FINISHED = 'Finished'
IN_PROGRESS = 'In Progress'
PENDING = 'Pending'
PERMANENT_FAILURE = 'PermanentFailure'
SUCCEEDED = 'Succeeded'
TEMPORARY_FAILURE = 'TemporaryFailure'

ACTIVITY_STATUSES = (
    (IN_PROGRESS, 'In Progress'),
    (PENDING, 'Pending'),
    (PERMANENT_FAILURE, 'Permanent Failure'),
    (SUCCEEDED, 'Succeeded'),
    (TEMPORARY_FAILURE, 'Temporary Failure'),
)

WORKFLOW_STATUSES = (
    (CANCELLED, 'Cancelled'),
    (IN_PROGRESS, 'In Progress'),
    (PENDING, 'Pending'),
    (FINISHED, 'Finished'),
)


class Workflow(models.Model):
    instance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=50, choices=WORKFLOW_STATUSES, default=PENDING)
    start_timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}: {self.instance_id}'


class Activity(models.Model):
    instance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    required = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=ACTIVITY_STATUSES, default=PENDING)
    workflow = models.ForeignKey(Workflow, related_name='activity', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f'{self.name}: {self.instance_id} - workflow: {self.workflow.instance_id}'


# TODO Event
# workflow: FK
# id
# timestamp
# type

