import pytest


@pytest.mark.django_db
def test_can_create_article(article):
    assert article
    assert article.id
    assert article.status == 'Unpublished'
    assert article.content
    # assert article.version == 1
