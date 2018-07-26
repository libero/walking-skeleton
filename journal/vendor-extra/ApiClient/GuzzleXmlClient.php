<?php

namespace Libero\ApiClient;

use GuzzleHttp\ClientInterface;
use GuzzleHttp\Promise\PromiseInterface;
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Symfony\Component\Stopwatch\Stopwatch;

final class GuzzleXmlClient implements XmlClient
{
    private $client;
    private $stopwatch;

    public function __construct(Stopwatch $stopwatch, ClientInterface $client)
    {
        $this->client = $client;
        $this->stopwatch = $stopwatch;
    }

    public function send(RequestInterface $request) : PromiseInterface
    {
        return $this->client
            ->sendAsync($request)
            ->then(
                function (ResponseInterface $e) : XmlResponse {
                    return new XmlResponse($this->stopwatch, $e);
                }
            );
    }
}
