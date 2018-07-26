<?php

namespace Libero\Dom;

trait XmlAsString
{
    abstract public function toXml() : string;

    final public function __toString() : string
    {
        return $this->toXml();
    }
}
