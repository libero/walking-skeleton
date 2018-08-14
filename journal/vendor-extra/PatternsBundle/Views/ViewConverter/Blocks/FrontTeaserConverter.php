<?php

namespace Libero\PatternsBundle\Views\ViewConverter\Blocks;

use Libero\Dom\Element;
use Libero\Dom\Node;
use Libero\PatternsBundle\Views\ViewConverter\LangAttributes;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use Symfony\Component\Routing\RouterInterface;
use function Functional\map;
use const Libero\PatternsBundle\LIBERO;

final class FrontTeaserConverter implements ViewConverter
{
    use LangAttributes;

    private $converter;
    private $router;

    public function __construct(ViewConverter $converter, RouterInterface $router)
    {
        $this->converter = $converter;
        $this->router = $router;
    }

    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        if (!$object instanceof Element || '@LiberoPatterns/patterns/teaser.html.twig' !== $template || 'front' !== $object->getName() || LIBERO !== $object->getNamespace()) {
            return null;
        }

        $context['level'] = $context['level'] ?? 1;

        return new View(
            $template, array_filter(
                [
                    'title' => $this->title($object, $context),
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
            'attributes' => $this->addLangAttribute($titleElement, $context) + ['href' => $this->router->generate('article', ['id' => $context['root']->get('libero:id')->toText()])],
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
