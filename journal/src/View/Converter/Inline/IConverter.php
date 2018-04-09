<?php

namespace Libero\Journal\View\Converter\Inline;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;

final class IConverter implements ViewConverter
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
        $context['lang'] = $context['lang'] ?? null;

        $attributes = '';
        if ($object->getAttribute('lang') ?? $context['lang'] !== $context['lang']) {
            $attributes .= " lang=\"{$object->getAttribute('lang')->toText()}\"";
            $context['lang'] = $object->getAttribute('lang')->toText();
        }

        $text = '';
        foreach ($object as $child) {
            $text .= $this->converter->convert($child, $context);
        }

        return <<<EOT
<i{$attributes}>{$text}</i>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'i' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
