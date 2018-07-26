<?php

namespace Libero\Views\ViewConverter;

use Libero\Dom\Node;
use Libero\Views\View;
use Libero\Views\ViewConverter;

final class ViewConverterRegistry implements ViewConverter
{
    private $registry = [];

    public function add(ViewConverter $registry)
    {
        $this->registry[] = $registry;
    }

    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        $view = null;

        foreach ($this->registry as $converter) {
            $converted = $converter->convert($object, $template, $context);

            if (!$view instanceof View) {
                $view = $converted;
            } elseif ($converted instanceof View) {
                $view = $view->withArguments($converted->getArguments())->withTemplate($converted->getTemplate());
            }
        }

        if (null === $view && null === $template) {
            return new View('@LiberoPatterns/patterns/text.html.twig', ['text' => "{$object->toText()}"]);
        }

        return $view;
    }
}
