<?php

namespace Libero\PatternsBundle\Twig;

use Twig_Extension;
use Twig_SimpleFilter;

final class LocaleDirectionExtension extends Twig_Extension
{
    public function getFilters() : iterable
    {
        return [
            new Twig_SimpleFilter('locale_direction', 'Libero\PatternsBundle\locale_direction'),
        ];
    }

    public function getName() : string
    {
        return 'locale_direction_extension';
    }
}
