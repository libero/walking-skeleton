<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use Symfony\Component\Translation\TranslatorInterface;
use const Libero\Journal\LIBERO;

final class AsideConverter implements ViewConverter
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

        $labelElement = $object->get('libero:label');
        if ($labelElement) {
            $labelContext = $context;
            $labelAttributes = '';
            if ($labelElement->getAttribute('lang') && $labelElement->getAttribute('lang')->toText() !== $labelContext['lang']) {
                $labelContext['lang'] = $object->getAttribute('lang')->toText();
                $dir = $this->translator->trans('direction', [], null, $labelContext['lang']);

                $labelAttributes .= " lang=\"{$labelContext['lang']}\"";
                $labelAttributes .= " dir=\"{$dir}\"";
            }

            $label = '';
            foreach ($labelElement as $child) {
                $label .= $this->converter->convert($child, $labelContext);
            }
            $label = "<h{$labelContext['level']}{$labelAttributes}>{$label}</h{$labelContext['level']}>";
        } else {
            $label = '';
        }

        $titleElement = $object->get('libero:title');
        if ($titleElement) {
            $titleContext = $context;
            $titleAttributes = '';
            if ($titleElement->getAttribute('lang') && $titleElement->getAttribute('lang')->toText() !== $titleContext['lang']) {
                $titleContext['lang'] = $object->getAttribute('lang')->toText();
                $dir = $this->translator->trans('direction', [], null, $titleContext['lang']);

                $titleAttributes .= " lang=\"{$titleContext['lang']}\"";
                $titleAttributes .= " dir=\"{$dir}\"";
            }

            $title = '';
            foreach ($titleElement as $child) {
                $title .= $this->converter->convert($child, $titleContext);
            }
            $title = "<h{$titleContext['level']}{$titleAttributes}>{$title}</h{$titleContext['level']}>";
        } else {
            $title = '';
        }

        $captionElement = $object->get('libero:caption');
        if ($captionElement) {
            $caption = '';
            foreach ($captionElement as $child) {
                $caption .= $this->converter->convert($child, $context);
            }
            $caption = "<div>{$caption}</div>";
        } else {
            $caption = '';
        }

        $attributionElement = $object->get('libero:attribution');
        if ($attributionElement) {
            $attribution = '';
            foreach ($attributionElement as $child) {
                $attribution .= $this->converter->convert($child, $context);
            }
            $attribution = "<div>{$attribution}</div>";
        } else {
            $attribution = '';
        }

        $body = '';
        foreach ($object->get('libero:content') as $i => $child) {
            $body .= $this->converter->convert($child, $context);
        }

        $doiAttribute = $object->getAttribute('doi');
        if ($doiAttribute) {
            $doi = "<p>doi:{$doiAttribute->toText()}</p>";
        } else {
            $doi = '';
        }

        return <<<EOT
<aside style="border: 1px solid black; margin: 1em; padding: 1em;"{$attributes}>
<header>
{$label}
{$title}
{$caption}
</header>
{$body}
<footer>
{$attribution}
{$doi}
</footer>
</section>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'aside' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
