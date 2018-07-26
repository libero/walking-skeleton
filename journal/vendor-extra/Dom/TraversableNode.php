<?php

namespace Libero\Dom;

use ArrayAccess;
use Countable;
use Traversable;

interface TraversableNode extends Node, ArrayAccess, Countable, Traversable
{
    public function find(string $xpath) : NodeList;

    public function get(string $xpath) : ?Node;
}
