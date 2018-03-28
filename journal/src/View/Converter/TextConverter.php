<?php

namespace Libero\Journal\View\Converter;

use Libero\Journal\Dom\Text;

final class TextConverter implements ViewConverter
{
    /**
     * @param Text $object
     */
    public function convert($object, array $context = []) : string
    {
        return $object->toXml();
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Text;
    }
}
