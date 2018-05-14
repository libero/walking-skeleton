import pytest

from django.test.client import Client

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)


@pytest.mark.django_db
def test_can_delete_article(admin_client: Client, article: Article,
                            article_version_1: ArticleVersion,
                            content_en_front: Content):

    url = f'/articles/{article.id}'
    response = admin_client.delete(url)
    assert response.status_code == 204
    assert Article.objects.count() == 0
    assert ArticleVersion.objects.count() == 0
    assert Content.objects.count() == 0


@pytest.mark.django_db
def test_can_delete_article_version(admin_client: Client, article: Article,
                                    article_version_1: ArticleVersion,
                                    content_en_front: Content):
    url = f'/articles/{article.id}/{article_version_1.version}'
    response = admin_client.delete(url)
    assert response.status_code == 204
    assert Article.objects.count() == 1
    assert ArticleVersion.objects.count() == 0
    assert Content.objects.count() == 0


@pytest.mark.django_db
def test_it_deletes_version_and_greater_versions(admin_client: Client, article: Article,
                                                 article_version_1: ArticleVersion,
                                                 article_version_2: ArticleVersion,
                                                 article_version_3: ArticleVersion,
                                                 content_en_front: Content):

    assert ArticleVersion.objects.count() == 3

    url = f'/articles/{article.id}/{article_version_2.version}'
    response = admin_client.delete(url)
    assert response.status_code == 204
    assert Article.objects.count() == 1
    assert ArticleVersion.objects.count() == 1
    assert Content.objects.count() == 1


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


@pytest.mark.django_db
def test_can_get_article_content_without_giving_part_name(admin_client: Client,
                                                          article: Article,
                                                          article_version_1: ArticleVersion,
                                                          content_es_front: Content,
                                                          article_0065_es_front_xml: str):

    url = f'/articles/{article.id}/latest'
    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE='es')
    assert response.status_code == 200
    assert response.content.decode('utf-8') == article_0065_es_front_xml


@pytest.mark.django_db
def test_can_get_article_list_xml(admin_client: Client,
                                  article: Article,
                                  article_version_1: ArticleVersion,
                                  content_es_front: Content):

    response = admin_client.get('/articles/')
    assert response.status_code == 200
    assert response.content.decode('utf-8') == f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n' \
                                               f'<libero:articles xmlns:libero="http://libero.pub">' \
                                               f'<libero:article>{article.id}</libero:article>' \
                                               f'</libero:articles>'


@pytest.mark.django_db
def test_can_get_empty_article_list_xml(admin_client: Client):

    response = admin_client.get('/articles/')
    assert response.status_code == 200
    assert response.content.decode('utf-8') == f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n' \
                                               f'<libero:articles xmlns:libero="http://libero.pub"/>'


@pytest.mark.django_db
def test_can_handle_article_not_existing(admin_client: Client):
    url = '/articles/foobar-article/latest'
    response = admin_client.get(url)
    assert response.status_code == 406
    assert 'Invalid article ID' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_can_handle_no_article_version_present(admin_client: Client, article: Article):
    url = f'/articles/{article.id}/latest'
    response = admin_client.get(url)
    assert response.status_code == 406
    assert 'Content does not exist' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_can_handle_no_article_version_content_present(admin_client: Client,
                                                       article: Article,
                                                       article_version_1: ArticleVersion):
    url = f'/articles/{article.id}/latest'
    response = admin_client.get(url)
    assert response.status_code == 406
    assert 'Content does not exist' in response.content.decode('utf-8')
