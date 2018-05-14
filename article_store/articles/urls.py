from django.urls import path, include

from rest_framework import routers

from articles.api import (
    ArticleViewSet,
    ArticleContentAPIView,
    ArticleListAPIView,
)


router_v1 = routers.DefaultRouter()

router_v1.register('articles', ArticleViewSet, base_name='article')


urlpatterns = [
    path('api/v1/', include((router_v1.urls, 'api_v1'))),
    path('<str:article_id>/<str:version>', ArticleContentAPIView.as_view(), name='article-content-no-part'),
    path('<str:article_id>/<str:version>/<str:part>', ArticleContentAPIView.as_view(), name='article-content'),
    path('', ArticleListAPIView.as_view(), name='article-list'),
]
