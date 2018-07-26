<?php

namespace Libero\Dom;

use DOMDocument;
use DOMNode;
use DOMXPath;
use IteratorAggregate;
use Libero\Dom\Exception\InvalidDom;
use Symfony\Component\Stopwatch\Stopwatch;
use function restore_error_handler;
use function set_error_handler;
use function strpos;

final class Document implements IteratorAggregate, TraversableNode
{
    use FindsThroughXPath;
    use ReadOnlyArrayAccess;
    use XmlAsString;

    private $document;
    private $namespaces = [];
    private $xPath;

    public function __construct(Stopwatch $stopwatch, string $xml, string $defaultNamespace)
    {
        $event = $stopwatch->start(self::CLASS, 'xml');

        $this->document = new DOMDocument();
        $this->document->preserveWhiteSpace = false;

        set_error_handler(
            function (int $errno, string $errstr) : bool {
                if (E_WARNING === $errno && false !== strpos($errstr, 'DOMDocument::loadXML()')) {
                    throw new InvalidDom($errstr);
                }

                return false;
            }
        );
        $this->document->loadXML($xml);
        restore_error_handler();

        $document = $this->document;
        $this->xPath = new class($stopwatch, $document) extends DOMXPath
        {
            private $stopwatch;

            public function __construct(Stopwatch $stopwatch, \DOMDocument $doc)
            {
                parent::__construct($doc);
                $this->stopwatch = $stopwatch;
            }

            public function query($expr, ?DOMNode $context = null, $registerNodeNS = null)
            {
                $event = $this->stopwatch->start($expr, 'xpath');

                $return = parent::query($expr, $context, $registerNodeNS);

                $event->stop();

                return $return;
            }
        };

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

        $event->stop();
    }

    public function getPath() : string
    {
        return $this->document->getNodePath();
    }

    public function getRootElement() : Element
    {
        return $this->convert($this->document->documentElement);
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
