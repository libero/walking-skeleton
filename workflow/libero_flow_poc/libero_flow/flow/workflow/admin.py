from django.contrib import admin

from .models import (
    Activity,
    Event,
    Workflow,
)


class ActivityAdmin(admin.ModelAdmin):

    list_filter = (
        'instance_id',
        'name',
        'status'
    )

    list_display = (
        'instance_id',
        'name',
        'status',
        'required',
        'workflow'
    )

    list_display_links = ['instance_id']


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0


class EventAdmin(admin.ModelAdmin):

    list_filter = (
        'id',
        'type',
        'created'
    )

    list_display = (
        'id',
        'type',
        'created',
    )

    list_display_links = ['id']


class WorkflowAdmin(admin.ModelAdmin):

    inlines = [
        ActivityInline,
    ]

    list_filter = (
        'end_timestamp',
        'instance_id',
        'name',
        'status',
        'start_timestamp',
    )

    list_display = (
        'instance_id',
        'name',
        'status',
        'start_timestamp',
        'end_timestamp',
    )

    list_display_links = ['instance_id']


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Workflow, WorkflowAdmin)
