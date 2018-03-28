<?php

namespace Libero\Journal\View\Converter\Inline;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;

final class AConverter implements ViewConverter
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

        $href = $object->getAttribute('href')->toText();

        $attributes = '';
        if ($object->getAttribute('lang') ?? $context['lang'] !== $context['lang']) {
            $attributes .= " lang=\"{$object->getAttribute('lang')}\"";
        }

        $text = '';
        foreach ($object as $child) {
            $text .= $this->converter->convert($child, $context);
        }

        return <<<EOT
<a href="{$href}"{$attributes}>{$text}</a>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'a' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
