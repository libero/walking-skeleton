<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use Symfony\Component\Translation\TranslatorInterface;
use const Libero\Journal\LIBERO;

final class SectionConverter implements ViewConverter
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
        $context['level'] = ($context['level'] ?? 1) + 1;

        $attributes = '';
        if ($id = $object->getAttribute('id')) {
            $attributes .= " id=\"{$id->toText()}\"";
        }
        if ($object->getAttribute('lang') && $object->getAttribute('lang')->toText() !== $context['lang']) {
            $context['lang'] = $object->getAttribute('lang')->toText();
            $dir = $this->translator->trans('direction', [], null, $context['lang']);

            $attributes .= " lang=\"{$context['lang']}\"";
            $attributes .= " dir=\"{$dir}\"";
        }

        $titleElement = $object->get('libero:title');
        $titleContext = $context;
        $titleAttributes = '';
        if ($titleElement->getAttribute('lang') && $titleElement->getAttribute('lang')->toText() !== $titleContext['lang']) {
            $titleContext['lang'] = $titleElement->getAttribute('lang')->toText();
            $dir = $this->translator->trans('direction', [], null, $titleContext['lang']);

            $attributes .= " lang=\"{$titleContext['lang']}\"";
            $attributes .= " dir=\"{$dir}\"";
        }

        $title = '';
        foreach ($titleElement as $child) {
            $title .= $this->converter->convert($child, $titleContext);
        }

        $body = '';
        foreach ($object->get('libero:content') as $i => $child) {
            $body .= $this->converter->convert($child, $context);
        }

        return <<<EOT
<section{$attributes}>
   <h{$context['level']}{$titleAttributes}>{$title}</h{$context['level']}>
{$body}
</section>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'section' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
