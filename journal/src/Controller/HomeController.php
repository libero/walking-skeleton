<?php

namespace Libero\Journal\Controller;

use GuzzleHttp\ClientInterface;
use GuzzleHttp\Promise\PromiseInterface;
use Libero\Journal\Dom\Document;
use Libero\Journal\Dom\Element;
use Psr\Http\Message\ResponseInterface;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;
use function Functional\compose;
use function Functional\invoker;
use function GuzzleHttp\Promise\all;

final class HomeController
{
    private $twig;
    private $apiClient;

    public function __construct(Environment $twig, ClientInterface $apiClient)
    {
        $this->twig = $twig;
        $this->apiClient = $apiClient;
    }

    public function __invoke(Request $request) : Response
    {
        $articles = $this->apiClient->requestAsync('GET', 'articles')
            ->then([$this, 'toDocument'])
            ->then(function (Document $articles) use ($request) : PromiseInterface {
                $promises = [];
                foreach ($articles->find('libero:articles/libero:article') as $article) {
                    $promises[] = $this->apiClient->requestAsync('GET', "articles/{$article->toText()}/latest", ['headers' => ['Accept-Language' => $request->getLocale()]]);
                }

                return all($promises);
            })
            ->then(function (array $articles) : array {
                return array_map(compose([$this, 'toDocument'], invoker('get', ['libero:front'])), $articles);
            })
            ->then(function (array $articles) : array {
                return array_map(function (Element $article) : array {
                    return [
                        'id' => $article->get('libero:id')->toText(),
                        'title' => $article->get('libero:title')->toText(),
                        'language' => $article->getAttribute('lang')->toText(),
                    ];
                }, $articles);
            });

        $articles = $articles->wait();

        return new Response($this->twig->render('home.html.twig', ['articles' => $articles]));
    }

    public function toDocument(ResponseInterface $response) : Document
    {
        return new Document((string) $response->getBody(), 'libero');
    }
}
