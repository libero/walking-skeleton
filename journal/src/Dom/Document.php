<?php

namespace Libero\Journal\Dom;

use DOMDocument;
use DOMNode;
use DOMXPath;
use IteratorAggregate;
use Libero\Journal\Dom\Exception\InvalidDom;
use function restore_error_handler;
use function set_error_handler;
use function strpos;

final class Document implements IteratorAggregate, TraversableNode
{
    use FindsThroughXPath;
    use ReadOnlyArrayAccess;

    private $document;
    private $namespaces = [];
    private $xPath;

    public function __construct(string $xml, string $defaultNamespace)
    {
        $this->document = new DOMDocument();
        $this->document->preserveWhiteSpace = false;

        set_error_handler(function (int $errno, string $errstr) : bool {
            if (E_WARNING === $errno && false !== strpos($errstr, 'DOMDocument::loadXML()')) {
                throw new InvalidDom($errstr);
            }

            return false;
        });
        $this->document->loadXML($xml);
        restore_error_handler();

        $this->xPath = new DOMXPath($this->document);

        foreach ($this->xPath->query('namespace::*') as $namespace) {
            if (!empty($namespace->prefix)) {
                if ('xml' !== $namespace->prefix && 'http://www.w3.org/XML/1998/namespace' !== $namespace->nodeValue) {
                    $this->namespaces[$namespace->prefix] = $namespace->nodeValue;
                }
            } else {
                if (empty($this->namespaces[$defaultNamespace])) {
                    $this->namespaces[$defaultNamespace] = $this->document->documentElement->getAttribute('xmlns');
                }
            }
        }

        foreach ($this->namespaces as $prefix => $uri) {
            $this->xPath->registerNamespace($prefix, $uri);
        }
    }

    public function getPath() : string
    {
        return $this->document->getNodePath();
    }

    public function toText() : string
    {
        return $this->document->nodeValue;
    }

    public function toXml() : string
    {
        return $this->document->saveXml();
    }

    protected function getXPath() : DOMXPath
    {
        return $this->xPath;
    }

    protected function getXPathContext() : DOMNode
    {
        return $this->document;
    }
}
