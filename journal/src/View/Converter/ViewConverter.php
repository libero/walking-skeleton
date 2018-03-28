<?php

namespace Libero\Journal\View\Converter;

use Libero\Dom\Node;
use Libero\Templating\View;

interface ViewConverter
{
    public function convert($object, array $context = []) : string;

    public function supports($object, array $context = []) : bool;
}
