<?php

namespace Libero\Journal\Dom;

use DOMAttr;
use DOMXPath;

final class Attribute implements Node
{
    private $xPath;
    private $domAttr;

    /**
     * @internal
     */
    public function __construct(DOMXPath $xPath, DOMAttr $domAttr)
    {
        $this->xPath = $xPath;
        $this->domAttr = $domAttr;
    }

    public function getPath() : string
    {
        return $this->domAttr->getNodePath();
    }

    public function toText() : string
    {
        return $this->domAttr->nodeValue;
    }

    public function toXml() : string
    {
        return $this->domAttr->ownerDocument->saveXML($this->domAttr);
    }
}
