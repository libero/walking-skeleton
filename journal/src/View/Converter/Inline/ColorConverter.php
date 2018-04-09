<?php

namespace Libero\Journal\View\Converter\Inline;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\ELIFE;

final class ColorConverter implements ViewConverter
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
        $color = $object->getAttribute('color')->toText();

        $text = '';
        foreach ($object as $child) {
            $text .= $this->converter->convert($child, $context);
        }

        return <<<EOT
<span style="color: {$color}">{$text}</span>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'color' === $object->getName() && ELIFE === $object->getNamespace();
    }
}
