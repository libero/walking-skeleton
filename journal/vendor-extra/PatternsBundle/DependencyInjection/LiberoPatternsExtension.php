<?php

namespace Libero\PatternsBundle\DependencyInjection;

use Libero\Views\ViewConverter;
use Symfony\Component\Config\FileLocator;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\DependencyInjection\Loader\XmlFileLoader;
use Symfony\Component\HttpKernel\DependencyInjection\Extension;

final class LiberoPatternsExtension extends Extension
{
    public function load(array $configs, ContainerBuilder $container) : void
    {
        $loader = new XmlFileLoader($container, new FileLocator(__DIR__.'/../Resources/config'));

        $loader->load('twig.xml');
        $loader->load('view_converters.xml');

        $container->registerForAutoconfiguration(ViewConverter::class)->addTag('libero.views.view_converter');
    }
}
