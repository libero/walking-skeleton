import pytest

from articles.models import (
    PREVIEW,
    READY,
    ArticleVersion,
)


@pytest.mark.django_db
def test_can_create_article_version(article_version_1: ArticleVersion):
    assert article_version_1
    assert article_version_1.version == 1
    assert article_version_1.status == PREVIEW


@pytest.mark.django_db
def test_can_change_status(article_version_1: ArticleVersion):
    article_version_1.status = READY
    article_version_1.save()
    assert article_version_1.status == READY
