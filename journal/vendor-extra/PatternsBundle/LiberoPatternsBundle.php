<?php

namespace Libero\PatternsBundle;

use Libero\PatternsBundle\DependencyInjection\Compiler\ViewConverterPass;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\HttpKernel\Bundle\Bundle;

final class LiberoPatternsBundle extends Bundle
{
    public function build(ContainerBuilder $container) : void
    {
        $container->addCompilerPass(new ViewConverterPass());
    }
}
