import pytest

from articles.models import Content


@pytest.mark.django_db
def test_can_create_content(content_en_front: Content, article_0065_en_front_xml: str):
    assert content_en_front
    assert content_en_front.language == 'en'
    assert content_en_front.name == 'front'
    assert content_en_front.text == article_0065_en_front_xml
