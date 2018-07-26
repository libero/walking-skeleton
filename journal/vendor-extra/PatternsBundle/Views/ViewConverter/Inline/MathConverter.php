<?php

namespace Libero\PatternsBundle\Views\ViewConverter\Inline;

use Libero\Dom\Element;
use Libero\Dom\Node;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use function str_replace;
use const Libero\PatternsBundle\MATHML;

final class MathConverter implements ViewConverter
{
    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        if (!$object instanceof Element || 'math' !== $object->getName() || MATHML !== $object->getNamespace()) {
            return null;
        }

        return new View(
            '@LiberoPatterns/patterns/math.html.twig', [
                'math' => str_replace('mml:', '', $object->toXml()),
            ]
        );
    }
}
