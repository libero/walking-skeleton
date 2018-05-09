from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)
from articles.serializers import (
    ArticleSerializer,
    ContentSerializer,
)

from articles.utils import parse_accept_language_header


class ArticleViewSet(viewsets.ModelViewSet):
    model = Article
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleContentAPIView(APIView):
    renderer_classes = (XMLRenderer,)

    latest = 'latest'

    def get(self, request: Request, article_id: str, version: str, part: str) -> HttpResponse:
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

        except AttributeError as err:
            return Response({'error': f'Content does not exist - {err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ObjectDoesNotExist as err:
            return Response({'error': f'{err}'}, status=status.HTTP_406_NOT_ACCEPTABLE)
