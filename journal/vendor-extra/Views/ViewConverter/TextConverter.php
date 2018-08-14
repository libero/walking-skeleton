<?php

namespace Libero\Views\ViewConverter;

use Libero\Dom\Node;
use Libero\Dom\Text;
use Libero\Views\View;
use Libero\Views\ViewConverter;

final class TextConverter implements ViewConverter
{
    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        if (!$object instanceof Text) {
            return null;
        }

        return new View('@LiberoPatterns/patterns/text.html.twig', ['text' => $object->toText()]);
    }
}
