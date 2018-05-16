from django.core.exceptions import ValidationError
import pytest

from articles.models import (
    Article,
    ArticleVersion,
)


@pytest.mark.django_db
def test_can_create_article(article: Article):
    assert article
    assert article.id


@pytest.mark.django_db
def test_can_get_latest_version(article: Article,
                                article_version_2: ArticleVersion,
                                article_version_3: ArticleVersion):
    assert article.latest_version == 3


@pytest.mark.django_db
def test_will_not_accept_invalid_id_format():
    with pytest.raises(ValidationError):
        Article.objects.create(id='[foo](bar)**')
