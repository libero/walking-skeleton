from rest_framework import serializers

from articles.models import (
    Article,
    ArticleVersion,
    Content,
)


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = (
            'id',
            'name',
            'language',
            'text',
        )


class ArticleVersionSerializer(serializers.ModelSerializer):
    content_items = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = ArticleVersion
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    versions = ArticleVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
