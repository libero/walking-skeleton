<?php

namespace Libero\Journal\Views\ViewConverter\Inline;

use Libero\Dom\Element;
use Libero\Dom\Node;
use Libero\PatternsBundle\Views\ViewConverter\LangAttributes;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use function Functional\map;
use const Libero\Journal\ELIFE;

final class ColorConverter implements ViewConverter
{
    use LangAttributes;

    private $converter;

    public function __construct(ViewConverter $converter)
    {
        $this->converter = $converter;
    }

    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        if (!$object instanceof Element || 'color' !== $object->getName() || ELIFE !== $object->getNamespace()) {
            return null;
        }

        return new View(
            '@LiberoPatterns/patterns/span.html.twig', [
                'attributes' => $this->addLangAttribute($object, $context, ['style' => "color: {$object->getAttribute('color')->toText()}"]),
                'text' => array_filter(
                    map(
                        $object,
                        function (Node $node) use ($context) : ?View {
                            return $this->converter->convert($node, null, $context);
                        }
                    )
                ),
            ]
        );
    }
}
