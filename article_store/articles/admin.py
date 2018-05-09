from django.contrib import admin

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)


class ArticleAdmin(admin.ModelAdmin):

    list_filter = (
        'id',
    )

    list_display = (
        'id',
    )

    list_display_links = ['id']


class ContentAdmin(admin.ModelAdmin):

    list_filter = (
        'id',
    )

    list_display = (
        'id',
        'article_version',
        'language',
        'name',
    )

    list_display_links = ['id']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleVersion)
admin.site.register(Content, ContentAdmin   )
