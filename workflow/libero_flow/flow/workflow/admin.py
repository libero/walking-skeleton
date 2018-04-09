from django.contrib import admin

from .models import Activity, Workflow


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
admin.site.register(Workflow, WorkflowAdmin)
