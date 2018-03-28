<?php

namespace Libero\Journal\Dom;

interface Node
{
    public function getPath() : string;

    public function toText() : string;

    public function toXml() : string;
}
