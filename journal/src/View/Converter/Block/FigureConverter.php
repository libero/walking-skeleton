<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;

final class FigureConverter implements ViewConverter
{
    private $converter;

    public function __construct(ViewConverter $converter)
    {
        $this->converter = $converter;
    }

    /**
     * @param Element $object
     */
    public function convert($object, array $context = []) : string
    {
        return '<p>[Figure]</p>';
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'figure' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
