import uuid

from django.db import models


PUBLISHED = 'Published'
UNPUBLISHED = 'Unpublished'

ARTICLE_STATUSES = (
    (PUBLISHED, 'Published'),
    (UNPUBLISHED, 'Unpublished'),
)


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.id}'


class ArticleVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, related_name='versions', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ARTICLE_STATUSES, default=UNPUBLISHED)
    version = models.IntegerField()

    # TODO needs check on version number unique, e.g. can't save x2 version 1's

    def __str__(self):
        return f'Article: {self.article_id}, Version {self.version}'


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article_version = models.ForeignKey(ArticleVersion, related_name='content_items', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    name = models.CharField(max_length=250)  # TODO has to be unique per version ??
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

