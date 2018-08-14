<?php

namespace Libero\Views;

use Libero\Dom\Node;

interface ViewConverter
{
    public function convert(Node $object, ?string $template, array $context = []) : ?View;
}
