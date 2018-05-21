import pytest

from django.test.client import Client

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)

ARTICLES_URL = '/articles'  # TODO refactor using this const!


class TestCreateArticleVersion:

    @pytest.mark.django_db
    def test_can_create_article_version(self, admin_client: Client, article: Article):
        response = admin_client.post(f'{ARTICLES_URL}/{article.id}',
                                     data='', content_type='application/xml')
        assert response.status_code == 201
        assert ArticleVersion.objects.count() == 1

    @pytest.mark.django_db
    def test_will_not_accept_invalid_article_id_format(self, admin_client: Client):
        invalid_id = '[foo](bar)**'
        response = admin_client.post(f'{ARTICLES_URL}/{invalid_id}',
                                     data='', content_type='application/xml')
        assert response.status_code == 406

    @pytest.mark.django_db
    def test_can_create_article_version_with_content(self, admin_client: Client,
                                                     article: Article,
                                                     content_xml_data: str):
        response = admin_client.post(f'{ARTICLES_URL}/{article.id}',
                                     data=content_xml_data,
                                     content_type='application/xml')
        assert response.status_code == 201
        assert ArticleVersion.objects.count() == 1
        assert Content.objects.count() == 1


class TestUpdateArticleVersion:

    @pytest.mark.django_db
    def test_can_update_article_version_with_content(self, admin_client: Client,
                                                     article: Article,
                                                     article_version_1: ArticleVersion,
                                                     content_en_front: Content,
                                                     content_xml_data: str):
        response = admin_client.put(f'{ARTICLES_URL}/{article.id}/{article_version_1.version}',
                                    data=content_xml_data,
                                    content_type='application/xml')
        assert response.status_code == 201
        assert ArticleVersion.objects.count() == 1
        assert Content.objects.count() == 1


class TestDeleteArticles:

    @pytest.mark.django_db
    def test_can_delete_article_version(self,
                                        admin_client: Client, article: Article,
                                        article_version_1: ArticleVersion,
                                        content_en_front: Content):
        url = f'/articles/{article.id}/{article_version_1.version}'
        response = admin_client.delete(url)
        assert response.status_code == 202
        assert Article.objects.count() == 1
        assert ArticleVersion.objects.count() == 0
        assert Content.objects.count() == 0

    @pytest.mark.django_db
    def test_it_deletes_version_and_greater_versions(self,
                                                     admin_client: Client, article: Article,
                                                     article_version_1: ArticleVersion,
                                                     article_version_2: ArticleVersion,
                                                     article_version_3: ArticleVersion,
                                                     content_en_front: Content):
        assert ArticleVersion.objects.count() == 3

        url = f'/articles/{article.id}/{article_version_2.version}'
        response = admin_client.delete(url)
        assert response.status_code == 202
        assert Article.objects.count() == 1
        assert ArticleVersion.objects.count() == 1
        assert Content.objects.count() == 1

    @pytest.mark.django_db
    def test_can_delete_article(self,
                                admin_client: Client, article: Article,
                                article_version_1: ArticleVersion,
                                content_en_front: Content):

        url = f'/articles/{article.id}'
        response = admin_client.delete(url)
        assert response.status_code == 202
        assert Article.objects.count() == 0
        assert ArticleVersion.objects.count() == 0
        assert Content.objects.count() == 0


class TestArticleList:

    @pytest.mark.django_db
    def test_can_get_article_list_xml(self,
                                      admin_client: Client,
                                      article: Article,
                                      article_version_1: ArticleVersion,
                                      content_es_front: Content):

        response = admin_client.get('/articles')
        assert response.status_code == 200
        assert response.content.decode('utf-8') == f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n' \
                                                   f'<libero:articles xmlns:libero="http://libero.pub">' \
                                                   f'<libero:article>{article.id}</libero:article>' \
                                                   f'</libero:articles>'

    @pytest.mark.django_db
    def test_can_get_empty_article_list_xml(self, admin_client: Client):
        response = admin_client.get('/articles')
        assert response.status_code == 200
        assert response.content.decode('utf-8') == f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n' \
                                                   f'<libero:articles xmlns:libero="http://libero.pub"/>'


class TestArticleErrors:

    @pytest.mark.django_db
    def test_can_handle_article_not_existing(self, admin_client: Client):
        url = '/articles/cc1250b5-0855-4fc2-906f-a6a77e4c90f5/latest'
        response = admin_client.get(url)
        assert response.status_code == 406
        assert 'Article matching query does not exist' in response.content.decode('utf-8')

    @pytest.mark.django_db
    def test_can_handle_no_article_version_present(self,
                                                   admin_client: Client,
                                                   article: Article):
        url = f'/articles/{article.id}/latest'
        response = admin_client.get(url)
        assert response.status_code == 406
        assert 'Content does not exist' in response.content.decode('utf-8')

    @pytest.mark.django_db
    def test_can_handle_no_article_version_content_present(self,
                                                           admin_client: Client,
                                                           article: Article,
                                                           article_version_1: ArticleVersion):
        url = f'/articles/{article.id}/latest'
        response = admin_client.get(url)
        assert response.status_code == 406
        assert 'Content does not exist' in response.content.decode('utf-8')


class TestArticleContent:

    @pytest.mark.django_db
    def test_can_get_article_content(self,
                                     admin_client: Client,
                                     article: Article,
                                     article_version_1: ArticleVersion,
                                     content_en_front: Content,
                                     article_0065_en_front_xml: str):
        url = f'/articles/{article.id}/{article_version_1.version}/{content_en_front.name}'
        response = admin_client.get(url)
        assert response.status_code == 200
        xml_payload = response.content.decode('utf-8')
        assert xml_payload == article_0065_en_front_xml

    @pytest.mark.django_db
    def test_can_get_content_using_latest_keyword_for_version(self,
                                                              admin_client: Client,
                                                              article: Article,
                                                              article_version_1: ArticleVersion,
                                                              content_en_front: Content,
                                                              article_0065_en_front_xml: str):

        url = f'/articles/{article.id}/latest/{content_en_front.name}'
        response = admin_client.get(url)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == article_0065_en_front_xml

    @pytest.mark.django_db
    def test_can_get_spanish_article_content(self,
                                             admin_client: Client,
                                             article: Article,
                                             article_version_1: ArticleVersion,
                                             content_es_front: Content,
                                             article_0065_es_front_xml: str):

        url = f'/articles/{article.id}/{article_version_1.version}/{content_es_front.name}'
        response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE='es')
        assert response.status_code == 200
        assert response.content.decode('utf-8') == article_0065_es_front_xml

    @pytest.mark.django_db
    def test_can_get_portuguese_article_content(self,
                                                admin_client: Client,
                                                article: Article,
                                                article_version_1: ArticleVersion,
                                                content_pt_front: Content,
                                                article_0065_pt_front_xml: str):

        url = f'/articles/{article.id}/{article_version_1.version}/{content_pt_front.name}'
        response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE='pt')
        assert response.status_code == 200
        assert response.content.decode('utf-8') == article_0065_pt_front_xml

    @pytest.mark.django_db
    def test_can_get_fallback_article_content(self,
                                              admin_client: Client,
                                              article: Article,
                                              article_version_1: ArticleVersion,
                                              content_es_front: Content,
                                              article_0065_es_front_xml: str):

        url = f'/articles/{article.id}/{article_version_1.version}/{content_es_front.name}'
        response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE='foo')
        assert response.status_code == 200
        assert response.content.decode('utf-8') == article_0065_es_front_xml

    @pytest.mark.django_db
    def test_can_get_article_content_without_giving_part_name(self,
                                                              admin_client: Client,
                                                              article: Article,
                                                              article_version_1: ArticleVersion,
                                                              content_es_front: Content,
                                                              article_0065_es_front_xml: str):

        url = f'/articles/{article.id}/latest'
        response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE='es')
        assert response.status_code == 200
        assert response.content.decode('utf-8') == article_0065_es_front_xml
