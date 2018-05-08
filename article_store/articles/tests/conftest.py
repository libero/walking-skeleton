from pathlib import Path

import pytest

from articles.fixtures import FIXTURES_DIR
from articles.models import Article


@pytest.fixture
@pytest.mark.django_db
def article(article_00666_front_xml):
    return Article.objects.create(content=article_00666_front_xml)


@pytest.fixture(scope='session')
def article_00666_front_xml():
    return Path.joinpath(FIXTURES_DIR, 'front.xml').read_text()



