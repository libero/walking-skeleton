<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;
use function str_replace;

final class MathMlConverter implements ViewConverter
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
        $attributes = '';
        if ($id = $object->getAttribute('id')) {
            $attributes .= " id=\"{$id->toText()}\"";
        }

        $label = $object->get('libero:label')->toText() ?? null;

        $body = str_replace('mml:', '', $object->get('mml:math')->toXml());

        return <<<EOT
<div{$attributes}>
{$label}
{$body}
</div>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'mathml' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
