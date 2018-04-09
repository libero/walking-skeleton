<?php

namespace Libero\Journal;

use Libero\Journal\Dom\Node;
use Libero\Journal\View\Converter\ViewConverter;
use function Functional\map;

const ELIFE = 'http://elifesciences.org';
const LIBERO = 'http://libero.pub';
const MATHML = 'http://www.w3.org/1998/Math/MathML';

function will_convert_all(ViewConverter $converter, array $context = []) : callable
{
    return function (iterable $nodes) use ($converter, $context) : iterable {
        return map($nodes, will_convert($converter, $context));
    };
}

function will_convert(ViewConverter $converter, array $context = []) : callable
{
    return function (Node $node) use ($converter, $context) : string {
        return $converter->convert($node, $context);
    };
}
