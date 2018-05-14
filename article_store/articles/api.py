from lxml.etree import (
    Element,
    SubElement,
    tostring,
)
from django.db.models import QuerySet
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)
from articles.serializers import ArticleSerializer

from articles.utils import parse_accept_language_header


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


class ArticleViewSet(viewsets.ModelViewSet):
    model = Article
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # parser_classes = (XMLParser,)
    # renderer_classes = (XMLRenderer,)


class ArticleListAPIView(APIView):

    def get(self, request: Request) -> HttpResponse:
        """Return xml article list.

        example return value:

        <?xml version='1.0' encoding='utf-8'?>
        <libero:articles xmlns:libero="http://libero.pub">
            <libero:article>cc1250b5-0855-4fc2-906f-a6a77e4c90f9</libero:article>
        </libero:articles>
        
        :param request: 
        :return: 
        """
        xml = article_list_xml_generator(articles=Article.objects.all())

        return HttpResponse(tostring(xml, encoding='utf-8', xml_declaration=True),
                            status=status.HTTP_200_OK, content_type="application/xml")


class ArticleContentAPIView(APIView):
    renderer_classes = (XMLRenderer,)

    default_part_name = 'front'
    latest = 'latest'

    def delete(self, request: Request, article_id: str, version: str = '') -> HttpResponse:
        """Delete an `Article`

        :param request: class: `Request`
        :param article_id: str
        :param version: str
        :return: class: `HttpResponse`
        """
        try:
            article = Article.objects.get(id=article_id)

            if not version:
                article.delete()
            else:
                if version == self.latest:
                    version = article.latest_version

                article_versions = ArticleVersion.objects.filter(article_id=article_id)

                for article_version in article_versions:
                    if article_version.version >= int(version):
                        article_version.delete()

            return HttpResponse(status=status.HTTP_204_NO_CONTENT, content_type="application/xml")

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
                version = article.latest_version

            article_version = ArticleVersion.objects.filter(article_id=article_id).filter(version=version).first()

            content_items = Content.objects\
                .filter(article_version=article_version.id)\
                .filter(name=part)

            # see if given language has an entry
            if content_items.filter(language=language).count():
                content = content_items.filter(language=language).first()
            else:
                # if not found try and return first fallback
                content = content_items.first()

            return HttpResponse(content.text, status=status.HTTP_200_OK, content_type="application/xml")

        except ValidationError as err:
            return Response({'error': f'Invalid article ID - {err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AttributeError as err:
            return Response({'error': f'Content does not exist - {err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ObjectDoesNotExist as err:
            return Response({'error': f'{err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)
