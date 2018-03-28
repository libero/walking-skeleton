<?php

namespace Libero\Journal\Controller;

use GuzzleHttp\ClientInterface;
use Libero\Journal\Dom\Document;
use Libero\Journal\View\Converter\ViewConverter;
use Psr\Http\Message\ResponseInterface;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;
use function extract;
use function GuzzleHttp\Promise\all;
use function Libero\Journal\will_convert_all;

final class ArticleController
{
    private $twig;
    private $apiClient;
    private $converter;

    public function __construct(Environment $twig, ClientInterface $apiClient, ViewConverter $converter)
    {
        $this->twig = $twig;
        $this->apiClient = $apiClient;
        $this->converter = $converter;
    }

    public function __invoke(Request $request, string $id) : Response
    {
        $article = (all([
            'front' => $this->apiClient->requestAsync('GET', "articles/{$id}/latest/front", ['headers' => ['Accept-Language' => $request->getLocale()]]),
            'body' => $this->apiClient->requestAsync('GET', "articles/{$id}/latest/body", ['headers' => ['Accept-Language' => $request->getLocale()]])->otherwise(function () { return null; }),
        ]))
            ->then(function (array $parts) : array {
                return array_map([$this, 'toDocument'], $parts);
            })
            ->then(function (array $parts) : array {
                /** @var Document $front */
                /** @var Document|null $body */
                extract($parts);

                $front = $front->get('libero:front');
                if ($body) {
                    $body = $body->get('libero:body');
                }

                $context = [
                    'front' => [
                        'id' => $front->get('libero:id')->toText(),
                        'doi' => $front->get('libero:doi') ? $front->get('libero:doi')->toText() : null,
                        'title' => $front->get('libero:title')->toText(),
                        'language' => $front->getAttribute('lang')->toText(),
                        'abstract' => [],
                        'digest' => [],
                    ],
                    'body' => [],
                ];

                if ($abstract = $front->get('libero:abstract')) {
                    $text = '';
                    foreach ($abstract as $child) {
                        $text .= $this->converter->convert($child, $context);
                    }

                    $context['front']['abstract'] += [
                        'id' => $abstract->getAttribute('id')->toText(),
                        'doi' => $abstract->getAttribute('doi') ? $abstract->getAttribute('doi')->toText() : null,
                        'text' => implode('', will_convert_all($this->converter, ['lang' => $context['front']['language']])($abstract)),
                    ];
                }

                if ($digest = $front->get('elife:digest')) {
                    $text = '';
                    foreach ($digest as $child) {
                        $text .= $this->converter->convert($child, $context);
                    }

                    $context['front']['digest'] += [
                        'id' => $digest->getAttribute('id')->toText(),
                        'doi' => $digest->getAttribute('doi') ? $digest->getAttribute('doi')->toText() : null,
                        'text' => implode('', will_convert_all($this->converter, ['lang' => $context['front']['language']])($digest)),
                    ];
                }

                if ($body) {
                    $context['body'] += [
                        'text' => implode('', will_convert_all($this->converter, ['lang' => $body->getAttribute('lang')->toText()])($body)),
                        'language' => $body->getAttribute('lang')->toText(),
                    ];
                }

                return $context;
            });

        $context = $article->wait();

        return new Response($this->twig->render('article.html.twig', $context));
    }

    public function toDocument(ResponseInterface $response) : Document
    {
        return new Document((string) $response->getBody(), 'libero');
    }
}
