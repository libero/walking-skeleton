<?php

namespace Libero\PatternsBundle\Views\ViewConverter\Blocks;

use Libero\Dom\Element;
use Libero\Dom\Node;
use Libero\PatternsBundle\Views\ViewConverter\LangAttributes;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use Symfony\Component\Translation\TranslatorInterface;
use function Functional\map;
use const Libero\PatternsBundle\LIBERO;

final class AbstractSectionConverter implements ViewConverter
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
        if (!$object instanceof Element || '@LiberoPatterns/patterns/section.html.twig' !== $template || 'abstract' !== $object->getName() || LIBERO !== $object->getNamespace()) {
            return null;
        }

        $context['level'] = $context['level'] ?? 1;

        return new View(
            '@LiberoPatterns/patterns/section.html.twig', array_filter(
                [
                    'attributes' => [
                        'id' => $object->getAttribute('id')->toText(),
                    ],
                    'doi' => $object->getAttribute('doi') ? $object->getAttribute('doi')->toText() : null,
                    'title' => [
                        'level' => $context['level'],
                        'text' => [new View('@LiberoPatterns/patterns/text.html.twig', ['text' => $this->translator->trans('app.abstract')])],
                    ],
                    'body' => [
                        'attributes' => $this->addLangAttribute($object, $context),
                        'text' => array_filter(
                            map(
                                $object,
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
}
