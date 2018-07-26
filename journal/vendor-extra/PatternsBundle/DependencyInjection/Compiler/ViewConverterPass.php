<?php

namespace Libero\PatternsBundle\DependencyInjection\Compiler;

use Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\DependencyInjection\Reference;
use function Functional\each;

final class ViewConverterPass implements CompilerPassInterface
{
    public function process(ContainerBuilder $container) : void
    {
        $definition = $container->findDefinition('libero.views.view_converter.registry');

        $taggedServices = $container->findTaggedServiceIds('libero.views.view_converter');

        each(array_keys($taggedServices), function (string $id) use ($definition) : void {
            $definition->addMethodCall('add', [new Reference($id)]);
        });
    }
}
