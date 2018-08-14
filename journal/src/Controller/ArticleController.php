<?php

namespace Libero\Journal\Controller;

use Libero\ApiClient\ArticlesClient;
use Libero\Dom\Element;
use Libero\Views\View;
use Libero\Views\ViewConverter;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;
use function Functional\const_function;
use function Functional\map;
use function GuzzleHttp\Promise\all;
use function Libero\PatternsBundle\locale_direction;

final class ArticleController
{
    private $twig;
    private $articlesClient;
    private $converter;

    public function __construct(ArticlesClient $articlesClient, Environment $twig, ViewConverter $converter)
    {
        $this->articlesClient = $articlesClient;
        $this->twig = $twig;
        $this->converter = $converter;
    }

    public function __invoke(Request $request, string $id) : Response
    {
        $article = all(
            [
                'front' => $this->articlesClient->part($id, null, 'front', ['Accept-Language' => $request->getLocale()]),
                'body' => $this->articlesClient->part($id, null, 'body', ['Accept-Language' => $request->getLocale()])->otherwise(const_function(null)),
            ]
        )
            ->then(
                function (array $parts) use ($request) : array {
                    /** @var Element $front */
                    $front = $parts['front']->getDocument()->get('libero:front');
                    /** @var Element|null $body */
                    $body = $parts['body'] ? $parts['body']->getDocument()->get('libero:body') : null;

                    $context = [
                        'title' => $front->get('libero:title')->toText(),
                        'top' => [],
                        'main' => [],
                        'bottom' => [],
                    ];

                    $mainContext = ['lang' => $request->getLocale(), 'dir' => locale_direction($request->getLocale())];

                    $frontContext = $mainContext + ['root' => $front];

                    $context['top'][] = $this->converter->convert($front, '@LiberoPatterns/patterns/content-header.html.twig', $frontContext);

                    if ($abstract = $front->get('libero:abstract')) {
                        $context['top'][] = $this->converter->convert($abstract, '@LiberoPatterns/patterns/section.html.twig', $frontContext + ['level' => 2]);
                    }

                    if ($body instanceof Element) {
                        $bodyContext = $mainContext + ['root' => $body];

                        $context['main'] = $context['main'] + array_filter(
                                map(
                                    $body,
                                    function (Element $element) use ($bodyContext) : ?View {
                                        return $this->converter->convert($element, null, $bodyContext);
                                    }
                                )
                            );
                    }

                    return $context;
                }
            );

        $context = $article->wait();

        return new Response($this->twig->render('article.html.twig', $context));
    }
}
