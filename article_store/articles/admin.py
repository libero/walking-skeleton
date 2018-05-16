from django.contrib import admin

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)


class ArticleVersionInline(admin.StackedInline):
    model = ArticleVersion
    show_change_link = True
    extra = 0


class ContentInline(admin.StackedInline):
    model = Content
    show_change_link = True
    extra = 0


class ArticleAdmin(admin.ModelAdmin):

    list_filter = ['id']
    list_display = ['id']
    list_display_links = ['id']
    inlines = [ArticleVersionInline]


class ArticleVersionAdmin(admin.ModelAdmin):
    list_filter = (
        'id',
        'version',
        'status',
    )
    list_display = (
        'id',
        'article_id',
        'version',
        'status',
    )
    list_display_links = ['id']
    inlines = [ContentInline]


class ContentAdmin(admin.ModelAdmin):

    list_filter = ['id']
    list_display = (
        'id',
        'article_version',
        'language',
        'name',
    )
    list_display_links = ['id']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleVersion, ArticleVersionAdmin)
admin.site.register(Content, ContentAdmin)
