<?php

namespace Libero\Journal\View\Converter\Block;

use Libero\Journal\Dom\Element;
use Libero\Journal\View\Converter\ViewConverter;
use const Libero\Journal\LIBERO;

final class CodeConverter implements ViewConverter
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
        $text = '';
        foreach ($object as $child) {
            $text .= $this->converter->convert($child, $context);
        }

        if ('preserve' === $object->getAttribute('space')->toText() ?? 'default') {
            return <<<EOT
<pre><code>{$text}</code></pre>
EOT;
        }

        return <<<EOT
<code>{$text}</code>
EOT;
    }

    public function supports($object, array $context = []) : bool
    {
        return $object instanceof Element && 'code' === $object->getName() && LIBERO === $object->getNamespace();
    }
}
