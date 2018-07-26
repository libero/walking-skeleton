<?php

namespace Libero\PatternsBundle\Views\ViewConverter;

use Libero\Dom\Element;
use function Libero\PatternsBundle\locale_direction;

trait LangAttributes
{
    final private function addLangAttribute(Element $element, array &$context, array $attributes = []) : array
    {
        $lang = $element->getAttribute('lang');

        if (!$lang && isset($context['root'])) {
            $lang = $context['root']->getAttribute('lang');
        } else {
            return $attributes;
        }

        if ($lang->toText() === ($context['lang'] ?? null)) {
            return $attributes;
        }

        $context['lang'] = $lang->toText();
        $attributes['lang'] = $context['lang'];

        $dir = locale_direction($context['lang']);

        if (($context['dir'] ?? null) !== $dir) {
            $context['dir'] = $dir;
            $attributes['dir'] = $dir;
        }

        return $attributes;
    }
}
