<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;

final class YouTubeConverter implements ViewConverter
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
        $src = "https://www.youtube.com/embed/{$object->get('libero:id')->toText()}";

        return <<<EOT
<iframe src="{$src}" allowfullscreen></iframe>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'youtube' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
