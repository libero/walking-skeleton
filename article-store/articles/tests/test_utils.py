import pytest

from articles.utils import (
    parse_accept_language_header,
    DEFAULT_LANGUAGE,
)


@pytest.mark.parametrize('header_value, expected', [
    ('en-US,en;q=0.9', 'en'),
    ('en', 'en'),
    ('es', 'es'),
    ('pt', 'pt'),
    ('', DEFAULT_LANGUAGE),
    (None, DEFAULT_LANGUAGE),
])
def test_can_parse_accept_language_header(header_value, expected):
    assert parse_accept_language_header(header_value) == expected
