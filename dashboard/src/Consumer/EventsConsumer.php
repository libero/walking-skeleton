<?php

namespace Libero\Dashboard\Consumer;

use Doctrine\Common\Persistence\ManagerRegistry;
use Doctrine\Common\Persistence\ObjectManager;
use Doctrine\ORM\EntityManagerInterface;
use Libero\Dashboard\Entity\Event;
use OldSound\RabbitMqBundle\RabbitMq\ConsumerInterface;
use PhpAmqpLib\Message\AMQPMessage;
use Throwable;

final class EventsConsumer implements ConsumerInterface
{
    private $doctrine;

    public function __construct(ManagerRegistry $doctrine)
    {
        $this->doctrine = $doctrine;
    }

    public function execute(AMQPMessage $message) : int
    {
        try {
            $this->doExecute($message);
        } catch (Throwable $e) { // Naive, but the process terminates otherwise.
            return ConsumerInterface::MSG_REJECT;
        }

        return ConsumerInterface::MSG_ACK;
    }

    private function doExecute(AMQPMessage $message) : void
    {
        $event = new Event($message->body);

        $manager = $this->getManager();

        $manager->persist($event);
        $manager->flush();
        $manager->detach($event);
    }

    private function getManager() : ObjectManager
    {
        $manager = $this->doctrine->getManager();

        if ($manager instanceof EntityManagerInterface && !$manager->isOpen()) {
            $manager = $this->doctrine->resetManager();
        }

        return $manager;
    }
}
