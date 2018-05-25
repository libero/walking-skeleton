from typing import Any, Tuple

from django.conf import settings
from rest_framework_xml.parsers import XMLParser
import defusedxml.ElementTree as etree

from xml.etree.ElementTree import register_namespace


def register_namespaces(name_spaces: Tuple[Tuple[str, str]]) -> None:
    """Register `n` number of xml namespaces

    :param name_spaces: Tuple
    :return:
    """
    for name_space in name_spaces:
        register_namespace(*name_space)


class ArticleXMLParser(XMLParser):
    content_element = 'content'
    media_type = 'application/xml'
    register_namespaces(settings.XML_NAMESPACES)

    def _xml_convert(self, element: 'etree.Element') -> Any:
        """Convert the xml `element` into the corresponding python object.

        If an `element.tag` matches the `content_element` all child elements
        will be converted into a single str.

        :param element: class: `etree.Element`
        :return: Any
        """
        if element.tag in self.content_element:
            content_str = self._nested_xml_to_string(element)
            return content_str

        children = list(element)

        if len(children) == 0:
            return self._type_convert(element.text)
        else:
            if children[0].tag == "list-item":
                data = []
                for child in children:
                    data.append(self._xml_convert(child))
            else:
                data = {}
                for child in children:
                    data[child.tag] = self._xml_convert(child)

            return data

    @staticmethod
    def _nested_xml_to_string(element: 'etree.Element') -> str:
        """Will take all child elements of `element` and convert
        them to a single str.

        :param element: class: `etree.Element`
        :return: str
        """
        children = [child for child in element]
        return etree.tostring(children[0]).decode('utf-8')


if __name__ == '__main__':
    pass
