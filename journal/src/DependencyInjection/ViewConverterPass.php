<?php

namespace Libero\Journal\DependencyInjection;

use Libero\Journal\View\Converter\ViewConverterRegistry;
use Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\DependencyInjection\Reference;
use function Functional\each;

final class ViewConverterPass implements CompilerPassInterface
{
    public function process(ContainerBuilder $container) : void
    {
        $definition = $container->findDefinition(ViewConverterRegistry::class);

        $taggedServices = $container->findTaggedServiceIds('view_model.converter');

        each(array_keys($taggedServices), function (string $id) use ($definition) : void {
            $definition->addMethodCall('add', [new Reference($id)]);
        });
    }
}
