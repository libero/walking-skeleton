<?php

namespace Libero\Journal\Dom;

use DOMAttr;
use DOMComment;
use DOMElement;
use DOMNode;
use DOMNodeList;
use DOMText;
use LogicException;
use function array_map;
use function get_class;

trait CreatesNodes
{
    use HasXPath;

    private function convertAll(DOMNodeList $domNodeList) : NodeList
    {
        return new NodeList(...array_filter(array_map([$this, 'convert'], iterator_to_array($domNodeList))));
    }

    private function convert(DOMNode $domNode) : ?Node
    {
        switch (true) {
            case $domNode instanceof DOMAttr:
                return new Attribute($this->getXPath(), $domNode);
            case $domNode instanceof DOMComment:
                return null;
            case $domNode instanceof DOMElement:
                return new Element($this->getXPath(), $domNode);
            case $domNode instanceof DOMText:
                return new Text($this->getXPath(), $domNode);
        }

        throw new LogicException('Unknown type \''.get_class($domNode).'\'');
    }
}
