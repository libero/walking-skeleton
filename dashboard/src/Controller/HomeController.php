<?php

namespace Libero\Dashboard\Controller;

use Doctrine\Common\Persistence\ObjectManager;
use Libero\Dashboard\Entity\Event;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;

final class HomeController
{
    private $doctrine;
    private $twig;

    public function __construct(Environment $twig, ObjectManager $doctrine)
    {
        $this->twig = $twig;
        $this->doctrine = $doctrine;
    }

    public function __invoke(Request $request) : Response
    {
        $events = $this->doctrine->getRepository(Event::class)->findAll();

        return new Response($this->twig->render('home.html.twig', ['events' => $events]));
    }
}
