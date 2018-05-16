from django.urls import path, include

from rest_framework import routers

from articles.api import (
    ArticleViewSet,
    ArticleXMLAPIView,
    ArticleListAPIView,
)


router_v1 = routers.DefaultRouter()
router_v1.register('articles', ArticleViewSet, base_name='article')


urlpatterns = [
    path('api/v1/', include((router_v1.urls, 'api_v1'))),
    path('<str:article_id>', ArticleXMLAPIView.as_view(), name='article-xml'),
    path('<str:article_id>/<str:version>', ArticleXMLAPIView.as_view(), name='article-version'),
    path('<str:article_id>/<str:version>/<str:part>', ArticleXMLAPIView.as_view(), name='article-content'),
    path('', ArticleListAPIView.as_view(), name='article-list'),
]
