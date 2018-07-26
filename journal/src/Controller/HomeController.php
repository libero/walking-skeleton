<?php

namespace Libero\Journal\Controller;

use GuzzleHttp\Promise\PromiseInterface;
use Libero\ApiClient\ArticlesClient;
use Libero\ApiClient\XmlResponse;
use Libero\Dom\Element;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Translation\TranslatorInterface;
use Twig\Environment;
use function Functional\map;
use function GuzzleHttp\Promise\all;
use function Libero\PatternsBundle\locale_direction;

final class HomeController
{
    private $articlesClient;
    private $converter;
    private $translator;
    private $twig;

    public function __construct(ArticlesClient $articlesClient, Environment $twig, ViewConverter $converter, TranslatorInterface $translator)
    {
        $this->articlesClient = $articlesClient;
        $this->twig = $twig;
        $this->converter = $converter;
        $this->translator = $translator;
    }

    public function __invoke(Request $request) : Response
    {
        $articles = $this->articlesClient->list()
            ->then(
                function (XmlResponse $list) use ($request) : PromiseInterface {
                    return all(
                        map(
                            $list->getDocument()->find('libero:articles/libero:article'),
                            function (Element $article) use ($request) : PromiseInterface {
                                return $this->articlesClient->part($article->toText(), null, 'front', ['Accept-Language' => $request->getLocale()]);
                            }
                        )
                    );
                }
            );

        $articles = $articles->wait();

        $mainContext = ['lang' => $request->getLocale(), 'dir' => locale_direction($request->getLocale())];

        $context = [
            'title' => $this->translator->trans('app.home'),
            'top' => [
                new View('@LiberoPatterns/patterns/content-header.html.twig', ['title' => ['text' => [$this->translator->trans('app.articles')]]]),
            ],
            'main' => array_filter(
                map(
                    $articles,
                    function (XmlResponse $article) use ($mainContext) : ?View {
                        $front = $article->getDocument()->getRootElement();

                        $frontContext = $mainContext + ['root' => $front];

                        return $this->converter->convert($front, '@LiberoPatterns/patterns/teaser.html.twig', $frontContext);
                    }
                )
            ),
        ];

        return new Response($this->twig->render('@LiberoPatterns/layouts/one-col.html.twig', $context));
    }
}
