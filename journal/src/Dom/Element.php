<?php

namespace Libero\Journal\Dom;

use function array_pop;
use DOMElement;
use DOMNode;
use DOMXPath;
use function explode;
use IteratorAggregate;

final class Element implements IteratorAggregate, TraversableNode
{
    use FindsThroughXPath;
    use ReadOnlyArrayAccess;

    private $xPath;
    private $domElement;

    /**
     * @internal
     */
    public function __construct(DOMXPath $xPath, DOMElement $domElement)
    {
        $this->xPath = $xPath;
        $this->domElement = $domElement;
    }

    public function getName() : string
    {
        $parts = explode(':', $this->domElement->tagName, 2);

        return array_pop($parts);
    }

    public function getNamespace() : string
    {
        return $this->domElement->namespaceURI;
    }

    public function getFullName() : string
    {
        return "{{$this->getNamespace()}}{$this->getName()}";
    }

    public function getAttribute(string $name, string $namespace = null) : ?Attribute
    {
        if (!$namespace) {
            $attribute = $this->domElement->attributes->getNamedItem($name);
        } else {
            $attribute = $this->domElement->attributes->getNamedItemNS($namespace, $name);
        }

        if (!$attribute) {
            return null;
        }

        return $this->convert($attribute);
    }

    public function getPath() : string
    {
        return $this->domElement->getNodePath();
    }

    public function toText() : string
    {
        return $this->domElement->nodeValue;
    }

    public function toXml() : string
    {
        return $this->domElement->ownerDocument->saveXML($this->domElement);
    }

    protected function getXPath() : DOMXPath
    {
        return $this->xPath;
    }

    protected function getXPathContext() : DOMNode
    {
        return $this->domElement;
    }
}
