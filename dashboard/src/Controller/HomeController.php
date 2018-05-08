<?php

namespace Libero\Dashboard\Controller;

use Doctrine\Common\Persistence\ObjectManager;
use Libero\Dashboard\Entity\Event;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;
use function array_reduce;

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
        $types = array_reduce(
            $this->doctrine->getRepository(Event::class)
                ->findBy([], ['aggregate.name' => 'ASC', 'aggregate.identifier' => 'ASC', 'dateTime' => 'ASC']),
            function (array $carry, Event $event) {
                $carry[$event->getAggregate()->getName()][$event->getAggregate()->getIdentifier()][] = $event;

                return $carry;
            },
            []
        );

        return new Response($this->twig->render('home.html.twig', ['types' => $types]));
    }
}
