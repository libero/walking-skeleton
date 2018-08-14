<?php

namespace Libero\Dom;

use DOMText;
use DOMXPath;

final class Text implements Node
{
    use XmlAsString;

    private $xPath;
    private $domText;

    /**
     * @internal
     */
    public function __construct(DOMXPath $xPath, DOMText $domText)
    {
        $this->xPath = $xPath;
        $this->domText = $domText;
    }

    public function getPath() : string
    {
        return $this->domText->getNodePath();
    }

    public function toText() : string
    {
        return $this->domText->nodeValue;
    }

    public function toXml() : string
    {
        return $this->domText->ownerDocument->saveXML($this->domText);
    }
}
