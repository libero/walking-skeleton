<?php

namespace Libero\PatternsBundle\Views\ViewConverter\Blocks;

use Libero\Dom\Element;
use Libero\Dom\Node;
use Libero\PatternsBundle\Views\ViewConverter\LangAttributes;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use function array_filter;
use function Functional\map;
use const Libero\PatternsBundle\LIBERO;

final class SectionConverter implements ViewConverter
{
    use LangAttributes;

    private $converter;

    public function __construct(ViewConverter $converter)
    {
        $this->converter = $converter;
    }

    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        if (!$object instanceof Element || 'section' !== $object->getName() || LIBERO !== $object->getNamespace()) {
            return null;
        }

        $context['level'] = ($context['level'] ?? 1) + 1;

        return new View(
            '@LiberoPatterns/patterns/section.html.twig', array_filter(
                [
                    'attributes' => $this->addLangAttribute(
                        $object,
                        $context,
                        $object->getAttribute('id') ? [
                            'id' => $object->getAttribute('id')->toText(),
                        ] : []
                    ),
                    'title' => $this->title($object, $context),
                    'body' => [
                        'text' => array_filter(
                            map(
                                $object->get('libero:content') ?? [],
                                function (Element $element) use ($context) : ?View {
                                    return $this->converter->convert($element, null, $context);
                                }
                            )
                        ),
                    ],
                ]
            )
        );
    }

    private function title(Element $object, array $context = []) : ?array
    {
        $titleElement = $object->get('libero:title');

        if (!$titleElement instanceof Element) {
            return null;
        }

        return [
            'attributes' => $this->addLangAttribute($titleElement, $context),
            'level' => $context['level'],
            'text' => array_filter(
                map(
                    $titleElement,
                    function (Node $node) use ($context) : ?View {
                        return $this->converter->convert($node, null, $context);
                    }
                )
            ),
        ];
    }
}
