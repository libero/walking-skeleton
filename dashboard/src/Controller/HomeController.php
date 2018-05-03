<?php

namespace Libero\Dashboard\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;

final class HomeController
{
    private $twig;

    public function __construct(Environment $twig)
    {
        $this->twig = $twig;
    }

    public function __invoke(Request $request) : Response
    {
        return new Response($this->twig->render('home.html.twig'));
    }
}
