<?php

namespace Libero\Journal\View\Converter\Inline;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use Symfony\Component\Translation\TranslatorInterface;
use const Libero\Journal\LIBERO;

final class IConverter implements ViewConverter
{
    private $converter;
    private $translator;

    public function __construct(ViewConverter $converter, TranslatorInterface $translator)
    {
        $this->converter = $converter;
        $this->translator = $translator;
    }

    /**
     * @param Element $object
     */
    public function convert($object, array $context = []) : string
    {
        $context['lang'] = $context['lang'] ?? null;

        $attributes = '';
        if ($object->getAttribute('lang') && $object->getAttribute('lang')->toText() !== $context['lang']) {
            $context['lang'] = $object->getAttribute('lang')->toText();
            $dir = $this->translator->trans('direction', [], null, $context['lang']);

            $attributes .= " lang=\"{$context['lang']}\"";
            $attributes .= " dir=\"{$dir}\"";
        }

        $text = '';
        foreach ($object as $child) {
            $text .= $this->converter->convert($child, $context);
        }

        return <<<EOT
<i{$attributes}>{$text}</i>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'i' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
