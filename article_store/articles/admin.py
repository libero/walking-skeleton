from django.contrib import admin

from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):

    list_filter = (
        'id',
        'status'
    )

    list_display = (
        'id',
        'status',
        'content',
    )

    list_display_links = ['id']


admin.site.register(Article, ArticleAdmin)
