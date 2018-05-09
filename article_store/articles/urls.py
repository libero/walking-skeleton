from django.urls import path, include

from rest_framework import routers

from articles.api import (
    ArticleViewSet,
    ArticleContentAPIView,
)


router_v1 = routers.DefaultRouter()

router_v1.register('articles', ArticleViewSet, base_name='article')


urlpatterns = [
    path('api/v1/', include((router_v1.urls, 'api_v1'))),
    # TODO article ids list
    path('<str:article_id>/<str:version>/<str:part>', ArticleContentAPIView.as_view(), name='article-content'),
]
