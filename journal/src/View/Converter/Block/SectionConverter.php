<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;

final class SectionConverter implements ViewConverter
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
        $context['level'] = ($context['level'] ?? 1) + 1;

        $titleElement = $object->get('libero:title');
        $titleContext = $context;
        $titleAttributes = '';
        if ($titleElement->getAttribute('lang') ?? $titleContext['lang'] !== $titleContext['lang']) {
            $titleAttributes .= " lang=\"{$object->getAttribute('lang')}\"";
            $childContext['lang'] = $object->getAttribute('lang');
        }

        $title = '';
        foreach ($titleElement as $child) {
            $title .= $this->converter->convert($child, $context);
        }

        $attributes = '';
        if ($id = $object->getAttribute('id')) {
            $attributes .= " id=\"{$id->toText()}\"";
        }
        if ($object->getAttribute('lang') ?? $context['lang'] !== $context['lang']) {
            $attributes .= " lang=\"{$object->getAttribute('lang')}\"";
        }

        $body = '';
        foreach ($object->get('libero:content') as $i => $child) {
            $body .= $this->converter->convert($child, $context);
        }

        return <<<EOT
<section{$attributes}>
   <h{$context['level']}{$titleAttributes}>{$title}</h{$context['level']}>
{$body}
</section>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'section' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
