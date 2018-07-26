<?php

namespace Libero\Journal\Views\ViewConverter\Blocks;

use Libero\Dom\Element;
use Libero\Dom\Node;
use Libero\PatternsBundle\Views\ViewConverter\LangAttributes;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use Symfony\Component\Translation\TranslatorInterface;
use function array_filter;
use function Functional\map;
use const Libero\PatternsBundle\LIBERO;

final class eLifeFrontContentHeaderConverter implements ViewConverter
{
    use LangAttributes;

    private $converter;
    private $translator;

    public function __construct(ViewConverter $converter, TranslatorInterface $translator)
    {
        $this->converter = $converter;
        $this->translator = $translator;
    }

    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        if (!$object instanceof Element || '@LiberoPatterns/patterns/content-header.html.twig' !== $template || 'front' !== $object->getName() || LIBERO !== $object->getNamespace()) {
            return null;
        }

        $context['level'] = ($context['level'] ?? 1) + 1;

        return new View(
            $template, array_filter(
                [
                    'digest' => $this->digest($object, $context),
                ]
            )
        );
    }

    private function digest(Element $object, array $context = []) : ?array
    {
        $digestElement = $object->get('elife:digest');

        if (!$digestElement instanceof Element) {
            return null;
        }

        return [
            'attributes' => [
                'id' => $digestElement->getAttribute('id')->toText(),
            ],
            'doi' => $digestElement->getAttribute('doi') ? $digestElement->getAttribute('doi')->toText() : null,
            'title' => [
                'level' => $context['level'],
                'text' => [new View('@LiberoPatterns/patterns/text.html.twig', ['text' => $this->translator->trans('app.digest')])],
            ],
            'body' => [
                'attributes' => $this->addLangAttribute(
                    $digestElement,
                    $context,
                    [
                        'id' => $digestElement->getAttribute('id')->toText(),
                    ]
                ),
                'text' => array_filter(
                    map(
                        $digestElement,
                        function (Element $element) use ($context) : ?View {
                            return $this->converter->convert($element, null, $context);
                        }
                    )
                ),
            ],
        ];
    }
}
