<?php

namespace Libero\ApiClient;

use GuzzleHttp\Promise\PromiseInterface;
use Psr\Http\Message\RequestInterface;

interface XmlClient
{
    public function send(RequestInterface $request) : PromiseInterface;
}
