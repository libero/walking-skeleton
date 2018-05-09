from pathlib import Path


from django.test.client import Client
import pytest
from rest_framework.test import APIClient

from articles.fixtures import FIXTURES_DIR
from articles.models import (
    Article,
    ArticleVersion,
    Content,
)


@pytest.fixture
@pytest.mark.django_db
def admin_rest_client(admin_user: Client) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
@pytest.mark.django_db
def article() -> Article:
    return Article.objects.create()


@pytest.fixture(scope='session')
def article_00666_front_xml() -> str:
    return Path.joinpath(FIXTURES_DIR, 'front.xml').read_text()


@pytest.fixture
@pytest.mark.django_db
def article_version(article: Article) -> ArticleVersion:
    return ArticleVersion.objects.create(article=article, version=1)


@pytest.fixture
@pytest.mark.django_db
def article_version_2(article: Article) -> ArticleVersion:
    return ArticleVersion.objects.create(article=article, version=2)


@pytest.fixture
@pytest.mark.django_db
def article_version_3(article: Article) -> ArticleVersion:
    return ArticleVersion.objects.create(article=article, version=3)


@pytest.fixture
@pytest.mark.django_db
def content(article_version: ArticleVersion,
            article_00666_front_xml: str) -> Content:
    return Content.objects.create(article_version=article_version,
                                  language='en',
                                  name='front',
                                  text=article_00666_front_xml)
