<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use Symfony\Component\Translation\TranslatorInterface;
use UnexpectedValueException;
use const Libero\Journal\LIBERO;

final class ListConverter implements ViewConverter
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

        $prefix = $object->getAttribute('prefix')->toText() ?? 'none';

        $element = 'ul';
        $attributes = '';
        switch ($prefix) {
            case 'none':
                $attributes = ' style="list-style-type: none"';
                break;
            case 'alpha-lower':
                $element = 'ol';
                $attributes = ' style="list-style-type: lower-alpha"';
                break;
            case 'alpha-upper':
                $element = 'ol';
                $attributes = ' style="list-style-type: upper-alpha"';
                break;
            case 'bullet':
                break;
            case 'number':
                $element = 'ol';
                $attributes = ' style="list-style-type: decimal"';
                break;
            case 'roman-lower':
                $element = 'ol';
                $attributes = ' style="list-style-type: lower-roman"';
                break;
            case 'roman-upper':
                $element = 'ol';
                $attributes = ' style="list-style-type: upper-roman"';
                break;
            default:
                throw new UnexpectedValueException("Unknown prefix {$prefix}");
        }

        $items = '';
        foreach ($object->find('libero:item') as $item) {
            $content = '';
            $childContext = $context;

            $attributes = '';
            if ($object->getAttribute('lang') && $object->getAttribute('lang')->toText() !== $childContext['lang']) {
                $childContext['lang'] = $object->getAttribute('lang')->toText();
                $dir = $this->translator->trans('direction', [], null, $childContext['lang']);

                $attributes .= " lang=\"{$context['lang']}\"";
                $attributes .= " dir=\"{$dir}\"";
            }
            foreach ($item as $child) {

                $content .= $this->converter->convert($child, $childContext);
            }
            $items .= "<li{$attributes}>{$content}</li>";
        }

        return <<<EOT
<{$element}{$attributes}>
{$items}
</{$element}>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'list' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
