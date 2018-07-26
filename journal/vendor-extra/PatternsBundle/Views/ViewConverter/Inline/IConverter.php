<?php

namespace Libero\PatternsBundle\Views\ViewConverter\Inline;

use Libero\Dom\Element;
use Libero\Dom\Node;
use Libero\PatternsBundle\Views\ViewConverter\LangAttributes;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use function Functional\map;
use const Libero\PatternsBundle\LIBERO;

final class IConverter implements ViewConverter
{
    use LangAttributes;

    private $converter;

    public function __construct(ViewConverter $converter)
    {
        $this->converter = $converter;
    }

    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        if (!$object instanceof Element || 'i' !== $object->getName() || LIBERO !== $object->getNamespace()) {
            return null;
        }

        return new View(
            '@LiberoPatterns/patterns/italic.html.twig', [
                'attributes' => $this->addLangAttribute($object, $context),
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
