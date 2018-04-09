<?php

namespace Libero\Journal\View\Converter;

use Libero\Journal\Dom\Element;
use RuntimeException;

final class ViewConverterRegistry implements ViewConverter
{
    private $registry = [];

    public function add(ViewConverter $registry)
    {
        $this->registry[] = $registry;
    }

    public function convert($object, array $context = []) : string
    {
        return $this->findModelConverter($object, $context)->convert($object, $context);
    }

    public function supports($object, array $context = []) : bool
    {
        try {
            $this->findModelConverter($object, $context);
        } catch (RuntimeException $e) {
            return false;
        }

        return true;
    }

    private function findModelConverter($object, array $context) : ViewConverter
    {
        $modelConverters = [];

        foreach ($this->registry as $modelConverter) {
            if ($modelConverter->supports($object, $context)) {
                $modelConverters[] = $modelConverter;
            }
        }

        $for = get_class($object);
        if ($object instanceof Element) {
            $for .= " {$object->getFullName()}";
        }

        if (empty($modelConverters)) {
            throw new RuntimeException("Can't find model converter for {$for} with ".var_export($context, true));
        } elseif (count($modelConverters) > 1) {
            throw new RuntimeException("Can't find single model converter for {$for} with ".var_export($context, true));
        }

        return $modelConverters[0];
    }
}
