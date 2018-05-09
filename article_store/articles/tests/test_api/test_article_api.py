import pytest

from django.test.client import Client

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)


@pytest.mark.django_db
def test_can_get_article_content(admin_client: Client,
                                 article: Article,
                                 article_version_1: ArticleVersion,
                                 content_en_front: Content,
                                 article_0065_en_front_xml: str):

    url = f'/articles/{article.id}/{article_version_1.version}/{content_en_front.name}'
    response = admin_client.get(url)
    assert response.status_code == 200
    assert response.content.decode('utf-8') == article_0065_en_front_xml


@pytest.mark.django_db
def test_can_get_content_using_latest_keyword_for_version(admin_client: Client,
                                                          article: Article,
                                                          article_version_1: ArticleVersion,
                                                          content_en_front: Content,
                                                          article_0065_en_front_xml: str):

    url = f'/articles/{article.id}/latest/{content_en_front.name}'
    response = admin_client.get(url)
    assert response.status_code == 200
    assert response.content.decode('utf-8') == article_0065_en_front_xml


@pytest.mark.django_db
def test_can_get_spanish_article_content(admin_client: Client,
                                         article: Article,
                                         article_version_1: ArticleVersion,
                                         content_es_front: Content,
                                         article_0065_es_front_xml: str):

    url = f'/articles/{article.id}/{article_version_1.version}/{content_es_front.name}'
    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE='es')
    assert response.status_code == 200
    assert response.content.decode('utf-8') == article_0065_es_front_xml


@pytest.mark.django_db
def test_can_get_portuguese_article_content(admin_client: Client,
                                            article: Article,
                                            article_version_1: ArticleVersion,
                                            content_pt_front: Content,
                                            article_0065_pt_front_xml: str):

    url = f'/articles/{article.id}/{article_version_1.version}/{content_pt_front.name}'
    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE='pt')
    assert response.status_code == 200
    assert response.content.decode('utf-8') == article_0065_pt_front_xml


@pytest.mark.django_db
def test_can_get_fallback_article_content(admin_client: Client,
                                          article: Article,
                                          article_version_1: ArticleVersion,
                                          content_es_front: Content,
                                          article_0065_es_front_xml: str):

    url = f'/articles/{article.id}/{article_version_1.version}/{content_es_front.name}'
    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE='foo')
    assert response.status_code == 200
    assert response.content.decode('utf-8') == article_0065_es_front_xml
