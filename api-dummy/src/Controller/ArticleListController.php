<?php

namespace Libero\ApiDummy\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use XMLWriter;
use const GLOB_ONLYDIR;

final class ArticleListController
{
    private $dataPath;

    public function __construct(string $dataPath)
    {
        $this->dataPath = $dataPath;
    }

    public function __invoke(Request $request) : Response
    {
        $articles = array_map('basename', glob("{$this->dataPath}/articles/*", GLOB_ONLYDIR));

        $xml = new XMLWriter();
        $xml->openMemory();
        $xml->startDocument('1.0');
        $xml->startElementNS('libero', 'articles', 'http://libero.pub');
        foreach ($articles as $article) {
            $xml->startElementNS('libero', 'article', null);
            $xml->text($article);
            $xml->endElement();
        }
        $xml->endElement();
        $xml->endDocument();

        return new Response($xml->outputMemory(), Response::HTTP_OK, ['Content-Type' => 'application/xml']);
    }
}
