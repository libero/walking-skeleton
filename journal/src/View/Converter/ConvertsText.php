<?php

namespace Libero\Journal\View\Converter;

use Libero\Journal\Dom\Node;
use Libero\Journal\Dom\TraversableNode;
use function Functional\invoke;

trait ConvertsText
{
    private function convertText(Node $object, array $context = []) : string
    {
        $context['lang'] = $context['lang'] ?? null;

        if (!$object instanceof TraversableNode) {
            return $object->toXml();
        }

        return implode('', invoke($object, 'toXml'));
    }
}
