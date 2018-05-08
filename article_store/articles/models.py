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
    content = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=ARTICLE_STATUSES, default=UNPUBLISHED)
    # TODO version

    def __str__(self):
        return f'{self.id}'
