import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


CANCELLED = 'Cancelled'
FAILED = 'Failed'
FINISHED = 'Finished'
IN_PROGRESS = 'In Progress'
PENDING = 'Pending'
PERMANENT_FAILURE = 'Permanent Failure'
SCHEDULED = 'Scheduled'
SUCCEEDED = 'Succeeded'
TEMPORARY_FAILURE = 'Temporary Failure'

ACTIVITY_STATUSES = (
    (IN_PROGRESS, 'In Progress'),
    (PENDING, 'Pending'),
    (PERMANENT_FAILURE, 'Permanent Failure'),
    (SCHEDULED, 'Scheduled'),
    (SUCCEEDED, 'Succeeded'),
    (TEMPORARY_FAILURE, 'Temporary Failure'),
)

WORKFLOW_STATUSES = (
    (CANCELLED, 'Cancelled'),
    (IN_PROGRESS, 'In Progress'),
    (PENDING, 'Pending'),
    (FAILED, 'Failed'),
    (FINISHED, 'Finished'),
)


class Workflow(models.Model):
    instance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=50, choices=WORKFLOW_STATUSES, default=PENDING)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    start_timestamp = models.DateTimeField(null=True, blank=True)
    end_timestamp = models.DateTimeField(null=True, blank=True)
    input_data = JSONField(null=True, blank=True)
    config = JSONField(null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.name}: {self.instance_id}'


class Activity(models.Model):
    instance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    independent = models.BooleanField(default=False)
    required = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=ACTIVITY_STATUSES, default=PENDING)
    workflow = models.ForeignKey(Workflow, related_name='activities', on_delete=models.CASCADE)
    config = JSONField(null=True, blank=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f'{self.name}: {self.instance_id} - workflow: {self.workflow.instance_id}'


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    type = models.CharField(max_length=250)
    workflow = models.ForeignKey(Workflow, related_name='events', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'{self.id}: {self.type}'


@receiver(post_save, sender=Workflow)
def set_workflow_start_timestamp(sender, instance, created, **kwargs):
    if instance.status == IN_PROGRESS and not instance.start_timestamp:
        instance.start_timestamp = timezone.now()
        instance.save()


@receiver(post_save, sender=Workflow)
def set_workflow_end_timestamp(sender, instance, created, **kwargs):
    if instance.status == FINISHED and not instance.end_timestamp:
        instance.end_timestamp = timezone.now()
        instance.save()
