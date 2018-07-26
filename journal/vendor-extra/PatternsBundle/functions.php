<?php

namespace Libero\PatternsBundle;

use Punic\Misc;

function locale_direction(string $locale) : string
{
    return 'right-to-left' === Misc::getCharacterOrder($locale) ? 'rtl' : 'ltr';
}
