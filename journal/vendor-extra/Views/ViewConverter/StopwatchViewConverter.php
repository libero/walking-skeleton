<?php

namespace Libero\Views\ViewConverter;

use Libero\Dom\Element;
use Libero\Dom\Node;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use Symfony\Component\Stopwatch\Stopwatch;

final class StopwatchViewConverter implements ViewConverter
{
    private $stopwatch;
    private $viewConverter;

    public function __construct(Stopwatch $stopwatch, ViewConverter $viewConverter)
    {
        $this->stopwatch = $stopwatch;
        $this->viewConverter = $viewConverter;
    }

    public function convert(Node $object, ?string $template, array $context = []) : ?View
    {
        if ($object instanceof Element) {
            if ($template) {
                $message = "converting {$object->getFullName()} to {$template}";
            } else {
                $message = "converting {$object->getFullName()}";
            }
        } else {
            $message = 'converting '.get_class($object);
        }

        $e = $this->stopwatch->start($message, 'view_converter');

        $view = $this->viewConverter->convert($object, $template, $context);

        $e->stop();

        return $view;
    }
}
