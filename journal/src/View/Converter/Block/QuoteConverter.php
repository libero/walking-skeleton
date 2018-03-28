<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;

final class QuoteConverter implements ViewConverter
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

        $text = '';
        foreach ($object->get('libero:content') as $child) {
            $text .= $this->converter->convert($child, $context);
        }

        $citeElement = $object->get('libero:cite');
        if ($citeElement) {
            $citeContext = $context;

            $citeAttributes = '';
            if ($citeElement->getAttribute('lang') ?? $citeContext['lang'] !== $citeContext['lang']) {
                $citeAttributes .= " lang=\"{$citeElement->getAttribute('lang')}\"";
                $citeContext['lang'] = $citeElement->getAttribute('lang');
            }
            $cite = '';

            foreach ($citeElement as $child) {
                $cite .= $this->converter->convert($child, $citeContext);
            }
            $cite = "<footer><cite{$citeAttributes}>{$cite}</cite></footer>";
        } else {
            $cite = '';
        }

        return <<<EOT
<blockquote>
{$text}
{$cite}
</blockquote>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'quote' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
