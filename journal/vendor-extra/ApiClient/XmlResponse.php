<?php

namespace Libero\ApiClient;

use InvalidArgumentException;
use Libero\Dom\Document;
use Libero\Dom\Exception\InvalidDom;
use Psr\Http\Message\ResponseInterface;
use Symfony\Component\Stopwatch\Stopwatch;

final class XmlResponse
{
    private $document;
    private $response;

    public function __construct(Stopwatch $stopwatch, ResponseInterface $response)
    {
        $this->response = $response;

        try {
            $this->document = new Document($stopwatch, (string)$response->getBody(), 'libero');
        } catch (InvalidDom $e) {
            throw new InvalidArgumentException('Invalid XML', 0, $e);
        }
    }

    public function getDocument() : Document
    {
        return $this->document;
    }

    public function getResponse() : ResponseInterface
    {
        return $this->response;
    }
}
