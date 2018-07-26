<?php

namespace Libero\ApiClient;

use GuzzleHttp\Promise\PromiseInterface;
use GuzzleHttp\Psr7\Request;

final class ArticlesClient
{
    private $client;

    public function __construct(XmlClient $client)
    {
        $this->client = $client;
    }

    public function list(array $headers = []) : PromiseInterface
    {
        return $this->request('GET', 'articles', $headers);
    }

    public function part(string $id, ?int $version, string $part = 'front', array $headers = []) : PromiseInterface
    {
        if (!is_int($version)) {
            $version = 'latest';
        }

        return $this->request('GET', "articles/{$id}/versions/{$version}/{$part}", $headers);
    }

    private function request(string $method, string $uri, array $headers = [], ?string $body = null) : PromiseInterface
    {
        return $this->client->send(new Request($method, $uri, $headers, $body));
    }
}
