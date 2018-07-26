<?php

namespace Libero\Dom;

interface Node
{
    public function getPath() : string;

    public function toText() : string;

    public function toXml() : string;

    public function __toString() : string;
}
