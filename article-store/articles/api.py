from lxml.etree import (
    Element,
    SubElement,
    tostring,
)
from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer

from articles.airflow_adapter import start_article_dag
from articles.xml_parser import ArticleXMLParser

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)
from articles.serializers import (
    ArticleSerializer,
    ArticleVersionSerializer,
)

from articles.utils import parse_accept_language_header
from events.utils import message_publisher


class ArticleViewSet(viewsets.ModelViewSet):
    model = Article
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleVersionViewSet(viewsets.ModelViewSet):
    model = ArticleVersion
    queryset = ArticleVersion.objects.all()
    serializer_class = ArticleVersionSerializer


def article_list_xml_generator(articles: 'QuerySet[Article]') -> Element:
    """Generate an xml representation of all `Article` objects.

    :param articles: QuerySet[Article]
    :return: class: `Element`
    """
    name_space = {'libero': 'http://libero.pub'}

    root = Element('{%s}articles' % name_space['libero'], nsmap=name_space)

    for article in articles:
        child = SubElement(root, '{%s}article' % name_space['libero'])
        child.text = str(article.id)

    return root


class ArticleItemAPIView(APIView):
    parser_classes = (ArticleXMLParser,)
    renderer_classes = (XMLRenderer,)

    default_part_name = 'front'
    latest = 'latest'
    style_element = '<?xml version="1.0" ?>\n'

    def post(self, request: Request, article_id: str) -> HttpResponse:
        """Create an `ArticleVersion`.

        :param request: class: `Request`
        :param article_id: str
        :return: class: `HttpResponse`
        """
        if not article_id or not Article.id_is_valid(article_id):
            return Response({'error': 'Please provide a valid article id'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        run_id = request.META.get(settings.RUN_ID_HEADER)

        with transaction.atomic():
            article, created = Article.objects.get_or_create(id=article_id)

            with message_publisher('article.version.post', run_id=run_id):
                article_version = ArticleVersion.objects.create(version=article.next_version,
                                                                article=article)

                for content_item in request.data.get('content-list', []):
                    Content.objects.create(article_version=article_version, **content_item)

                serializer = ArticleVersionSerializer(article_version)

        if settings.AIRFLOW_ACTIVE:
            start_article_dag(run_id=run_id,
                              article_id=article_id,
                              article_version=article_version.version,
                              article_version_id=article_version.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request: Request, article_id: str, version: str) -> HttpResponse:
        """Update an `ArticleVersion`

        :param request:
        :param article_id:
        :param version:
        :return: class: `HttpResponse`
        """
        if article_id and version:
            run_id = request.META.get(settings.RUN_ID_HEADER)

            with transaction.atomic():
                with message_publisher('article.version.put', run_id):
                    article_version = ArticleVersion.objects.get(version=version, article_id=article_id)
                    old_content = Content.objects.filter(article_version=article_version)
                    old_content.delete()

                    if request.data:
                        for content_item in request.data.get('content-list', []):
                            Content.objects.create(article_version=article_version, **content_item)

                    serializer = ArticleVersionSerializer(article_version)

            if settings.AIRFLOW_ACTIVE and not request.META.get(settings.AIRFLOW_REQUEST_HEADER):
                start_article_dag(run_id=run_id,
                                  article_id=article_id,
                                  article_version=article_version.version,
                                  article_version_id=article_version.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Please provide a valid article id and version number'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request: Request, article_id: str, version: str = '') -> HttpResponse:
        """Delete an `Article` or a all versions including and > a specified `ArticleVersion`

        :param request: class: `Request`
        :param article_id: str
        :param version: str
        :return: class: `HttpResponse`
        """
        try:
            article = Article.objects.get(id=article_id)

            if not version:
                with message_publisher('article.delete', request.META.get(settings.RUN_ID_HEADER)):
                    article.delete()
            else:
                if version == self.latest:
                    version = article.version_count

                with message_publisher('article.version.delete', request.META.get(settings.RUN_ID_HEADER)):
                    article_versions = ArticleVersion.objects.filter(article_id=article_id)

                    for article_version in article_versions:
                        if article_version.version >= int(version):
                            article_version.delete()

            return HttpResponse(status=status.HTTP_202_ACCEPTED, content_type="application/xml")

        except ValidationError as err:
            return Response({'error': f'Invalid article ID - {err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ObjectDoesNotExist as err:
            return Response({'error': f'{err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get(self, request: Request, article_id: str, version: str, part: str = default_part_name) -> HttpResponse:
        """Get article content based on version, language and content name.

        :param request: `Request`
        :param article_id: str
        :param version: str
        :param part: str
        :return: class: `HttpResponse`
        """
        language = parse_accept_language_header(request.META.get('HTTP_ACCEPT_LANGUAGE'))

        try:
            article = Article.objects.get(id=article_id)

            if version == self.latest:
                version = article.version_count

            article_version = ArticleVersion.objects\
                .filter(article_id=article_id)\
                .filter(version=version).first()

            content_items = Content.objects\
                .filter(article_version=article_version.id)\
                .filter(name=part)

            # see if given language has an entry
            if content_items.filter(language=language).count():
                content_item = content_items.filter(language=language).first()
            else:
                # if not, try and return first fallback
                content_item = content_items.first()

            payload = self.style_element + f'<?xml-model href="{content_item.model}"?>\n\n' + content_item.content

            return HttpResponse(payload, status=status.HTTP_200_OK, content_type="application/xml")

        except ValidationError as err:
            return Response({'error': f'Invalid article ID - {err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AttributeError as err:
            return Response({'error': f'Content does not exist - {err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ObjectDoesNotExist as err:
            return Response({'error': f'{err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ArticleListAPIView(APIView):
    parser_classes = (ArticleXMLParser,)
    renderer_classes = (XMLRenderer,)

    @staticmethod
    def get(request: Request) -> HttpResponse:
        """Return xml article list.

        example return value:

        <?xml version='1.0' encoding='utf-8'?>
        <libero:articles xmlns:libero="http://libero.pub">
            <libero:article>cc1250b5-0855-4fc2-906f-a6a77e4c90f9</libero:article>
        </libero:articles>

        :param request: class: `Request`
        :return: class: `HttpResponse`
        """
        xml = article_list_xml_generator(articles=Article.objects.all())

        return HttpResponse(tostring(xml, encoding='utf-8', xml_declaration=True),
                            status=status.HTTP_200_OK, content_type="application/xml")
