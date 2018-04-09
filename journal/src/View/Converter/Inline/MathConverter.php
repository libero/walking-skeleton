<?php

namespace Libero\Journal\View\Converter\Inline;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\MATHML;

final class MathConverter implements ViewConverter
{
    /**
     * @param Element $object
     */
    public function convert($object, array $context = []) : string
    {
        return str_replace('mml:', '', $object->toXml());
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'math' === $object->getName() && MATHML === $object->getNamespace();
    }
}
