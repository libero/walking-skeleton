import re
import uuid

from django.core.validators import RegexValidator
from django.db import models


PREVIEW = 'preview'
PUBLISHED = 'published'
READY = 'ready'

ARTICLE_VERSION_STATUSES = (
    (PREVIEW, 'preview'),
    (PUBLISHED, 'published'),
    (READY, 'ready'),
)

ARTICLE_ID_FORMAT = r'^[A-Za-z0-9\-._]+$'


class Article(models.Model):
    id = models.CharField(primary_key=True, max_length=250,
                          validators=[RegexValidator(regex=ARTICLE_ID_FORMAT)])

    article_id_format = ARTICLE_ID_FORMAT
    default_version_count = 0

    def __str__(self):
        return f'{self.id}'

    @property
    def version_count(self) -> int:
        """Count the associated `ArticleVersion.version`.

        :return: int
        """
        versions = self.versions.all()

        if versions:
            return versions.count()

        return self.default_version_count

    @property
    def next_version(self) -> int:
        """Finds the next version from the associated `ArticleVersion.version`.

        :return: int
        """
        return self.version_count + 1

    @classmethod
    def id_is_valid(cls, article_id) -> bool:
        """Check if a `str` value is valid against `article_id_format`

        :param article_id: str
        :return: bool
        """
        return True if re.match(cls.article_id_format, article_id) else False


class ArticleVersion(models.Model):
    article = models.ForeignKey(Article, related_name='versions', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ARTICLE_VERSION_STATUSES, default=PREVIEW)
    version = models.IntegerField(default=1)

    # TODO needs check on version number unique, e.g. can't save x2 version 1's

    def __str__(self):
        return f'Article: {self.article_id}, Version {self.version}'


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    article_version = models.ForeignKey(ArticleVersion, related_name='content_items', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    name = models.CharField(max_length=250)  # TODO has to be unique per version ??
    model = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

