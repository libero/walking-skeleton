<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;

final class ImageConverter implements ViewConverter
{
    private $converter;

    public function __construct(ViewConverter $converter)
    {
        $this->converter = $converter;
    }

    /**
     * @param Element $object
     */
    public function convert($object, array $context = []) : string
    {
        $image = "<img src=\"{$object->get('libero:source')->toText()}\">";

        $caption = '';
        if ($object->get('libero:title')) {
            $caption .= '<figcaption>';
            foreach ($object->get('libero:title') as $child) {
                $caption .= $this->converter->convert($child, $context);
            }
            $caption .= '</figcaption>';
        }

        return <<<EOT
<figure>
{$image}
{$caption}
</figure>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'image' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
