import pytest

from articles.models import Content


@pytest.mark.django_db
def test_can_create_content(content: Content, article_00666_front_xml: str):
    assert content
    assert content.language == 'en'
    assert content.name == 'front'
    assert content.text == article_00666_front_xml
