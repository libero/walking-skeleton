import uuid

from django.core.validators import RegexValidator
from django.db import models


PREVIEW = 'preview'
PUBLISHED = 'published'
READY = 'ready'

ARTICLE_STATUSES = (
    (PREVIEW, 'preview'),
    (PUBLISHED, 'Published'),
    (READY, 'ready'),
)


class Article(models.Model):
    id = models.CharField(primary_key=True, max_length=250,
                          validators=[RegexValidator(regex=r'^[A-Za-z0-9\-._]+$')])

    default_version = 0

    def __str__(self):
        return f'{self.id}'

    @property
    def latest_version(self) -> int:
        """Finds the latest associated `ArticleVersion.version`.

        :return: int
        """
        versions = self.versions.all()

        if versions:
            return max([version.version for version in versions ])

        return self.default_version

    @property
    def next_version(self) -> int:
        """Finds the next version from the associated `ArticleVersion.version`.

        :return: int
        """
        return self.latest_version + 1


class ArticleVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, related_name='versions', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ARTICLE_STATUSES, default=PREVIEW)
    version = models.IntegerField(default=1)

    # TODO needs check on version number unique, e.g. can't save x2 version 1's

    def __str__(self):
        return f'Article: {self.article_id}, Version {self.version}'


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article_version = models.ForeignKey(ArticleVersion, related_name='content_items', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    name = models.CharField(max_length=250)  # TODO has to be unique per version ??
    model = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

