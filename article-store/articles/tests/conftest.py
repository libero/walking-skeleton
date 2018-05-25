from pathlib import Path

from django.test.client import Client
import pytest
from rest_framework.test import APIClient

from articles.tests.fixtures import FIXTURES_DIR
from articles.models import (
    Article,
    ArticleVersion,
    Content,
)


def parse_fixture_file(file_name: str) -> str:
    return Path.joinpath(FIXTURES_DIR, file_name).read_text()


@pytest.fixture
@pytest.mark.django_db
def admin_rest_client(admin_user: Client) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
@pytest.mark.django_db
def article() -> Article:
    return Article.objects.create(id='cc1250b5-0855-4fc2-906f-a6a77e4c90f5')


@pytest.fixture(scope='session')
def article_0065_en_front_xml() -> str:
    return parse_fixture_file('0065_en_front.xml')


@pytest.fixture(scope='session')
def article_0065_en_front_payload_xml() -> str:
    return parse_fixture_file('0065_en_front_payload.xml')


@pytest.fixture(scope='session')
def article_0065_es_front_xml() -> str:
    return parse_fixture_file('0065_es_front.xml')


@pytest.fixture(scope='session')
def article_0065_es_front_payload_xml() -> str:
    return parse_fixture_file('0065_es_front_payload.xml')


@pytest.fixture(scope='session')
def article_0065_pt_front_xml() -> str:
    return parse_fixture_file('0065_pt_front.xml')


@pytest.fixture(scope='session')
def article_0065_pt_front_payload_xml() -> str:
    return parse_fixture_file('0065_pt_front_payload.xml')


@pytest.fixture
@pytest.mark.django_db
def article_version_1(article: Article) -> ArticleVersion:
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
def content_en_front(article_version_1: ArticleVersion,
                     article_0065_en_front_payload_xml: str) -> Content:
    return Content.objects.create(article_version=article_version_1,
                                  language='en',
                                  name='front',
                                  model='http://localhost:8081/schemas/scielo/article/front.rng',
                                  content=article_0065_en_front_payload_xml)


@pytest.fixture
@pytest.mark.django_db
def content_es_front(article_version_1: ArticleVersion,
                     article_0065_es_front_payload_xml: str) -> Content:
    return Content.objects.create(article_version=article_version_1,
                                  language='es',
                                  name='front',
                                  model='http://localhost:8081/schemas/scielo/article/front.rng',
                                  content=article_0065_es_front_payload_xml)


@pytest.fixture
@pytest.mark.django_db
def content_pt_front(article_version_1: ArticleVersion,
                     article_0065_pt_front_payload_xml: str) -> Content:
    return Content.objects.create(article_version=article_version_1,
                                  language='pt',
                                  name='front',
                                  model='http://localhost:8081/schemas/scielo/article/front.rng',
                                  content=article_0065_pt_front_payload_xml)


@pytest.fixture
def content_xml_data() -> str:
    return '''
    <root>
        <content-list>
            <list-item>
                <language>en</language>
                <name>front</name>
                <model>http://localhost:8081/schemas/scielo/article/body.rng</model>
                <content>
                    <front xmlns="http://libero.pub" xmlns:scielo="http://scielo.org" xml:lang="en">
                        <id>0065-1737-azm-31-03-0367</id>
                        <title>Damage evaluation of (Lepidoptera: Tortricidae) (Heinrich),
                            structural parameters and natural regeneration in Pinus nelsonii (Shaw) and
                            P. cembroides ( Zucc.) in Miquihuana, Tamaulipas</title>
                    </front>
                </content>
            </list-item>
        </content-list>
    </root>'''
