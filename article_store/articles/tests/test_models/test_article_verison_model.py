import pytest

from articles.models import (
    PREVIEW,
    READY,
    ArticleVersion,
)


@pytest.mark.django_db
def test_can_create_article_version(article_version: ArticleVersion):
    assert article_version
    assert article_version.version == 1
    assert article_version.status == PREVIEW


@pytest.mark.django_db
def test_can_change_status(article_version: ArticleVersion):
    article_version.status = READY
    article_version.save()
    assert article_version.status == READY
