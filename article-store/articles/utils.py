from django.utils.translation.trans_real import parse_accept_lang_header


DEFAULT_LANGUAGE = 'en'


def parse_accept_language_header(lang_str: str) -> str:
    """Obtain two char language string from header value.
    If value is already a two char string that will be returned.

    example usage:

    >>> parse_accept_language_header('en-US,en;q=0.9')
    'en'

    >>> parse_accept_language_header('es')
    'es'

    :param lang_str: str
    :return: str
    """
    try:
        return parse_accept_lang_header(lang_str)[-1][0]
    except (AttributeError, IndexError):
        return DEFAULT_LANGUAGE

