<?php

namespace Libero\Dashboard\Twig;

use Symfony\Component\Intl\Intl;
use Twig_Extension;
use Twig_SimpleFilter;

final class LocaleNameExtension extends Twig_Extension
{
    public function getFilters() : array
    {
        return [
            new Twig_SimpleFilter('locale_name', [$this, 'localeNameFilter']),
        ];
    }

    public function localeNameFilter($locale, $displayLocale = null) : string
    {
        return Intl::getLocaleBundle()->getLocaleName($locale, $displayLocale);
    }

    public function getName() : string
    {
        return 'locale_name_extension';
    }
}
