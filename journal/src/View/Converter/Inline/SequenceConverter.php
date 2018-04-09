<?php

namespace Libero\Journal\View\Converter\Inline;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\ELIFE;

final class SequenceConverter implements ViewConverter
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
        $text = '';
        foreach ($object as $child) {
            $text .= $this->converter->convert($child, $context);
        }

        return <<<EOT
<span style="word-wrap: break-word; word-break: break-all;">{$text}</span>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'sequence' === $object->getName() && ELIFE === $object->getNamespace();
    }
}
