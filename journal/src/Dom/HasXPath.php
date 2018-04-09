<?php

namespace Libero\Journal\Dom;

use DOMNode;
use DOMXPath;

trait HasXPath
{
    abstract protected function getXPath() : DOMXPath;

    abstract protected function getXPathContext() : DOMNode;
}
