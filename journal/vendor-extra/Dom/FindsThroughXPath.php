<?php

namespace Libero\Dom;

use Libero\Dom\Exception\NodeNotFound;
use RuntimeException;
use Traversable;

trait FindsThroughXPath
{
    use CreatesNodes;

    final public function find(string $xpath) : NodeList
    {
        $result = $this->getXPath()->query($xpath, $this->getXPathContext()); // TODO add evaluate()

        if (!$result) {
            throw new RuntimeException('XPath done gone not worked');
        }

        return new NodeList(...$this->convertAll($result));

    }

    final public function get(string $xpath) : ?Node
    {
        $result = @$this->getXPath()->query("{$xpath}[1]", $this->getXPathContext()); // TODO fix error handling and find a better way to get the first item quickly

        if (!$result || !$result->item(0)) {
            return null;
        }

        return $this->convert($result->item(0));
    }

    final public function getIterator() : Traversable
    {
        return $this->getChildren();
    }

    final public function offsetExists($offset)
    {
        return $this->getChildren()->offsetExists($offset);
    }

    final public function offsetGet($offset)
    {
        return $this->getChildren()->offsetGet($offset);
    }

    final public function count()
    {
        return $this->getChildren()->count();
    }

    final private function getChildren() : NodeList
    {
        return $this->find('child::node()');
    }
}
