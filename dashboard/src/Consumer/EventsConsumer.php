<?php

namespace Libero\Dashboard\Consumer;

use Doctrine\Common\Persistence\ObjectManager;
use Libero\Dashboard\Entity\Event;
use OldSound\RabbitMqBundle\RabbitMq\ConsumerInterface;
use PhpAmqpLib\Message\AMQPMessage;

final class EventsConsumer implements ConsumerInterface
{
    private $doctrine;

    public function __construct(ObjectManager $doctrine)
    {
        $this->doctrine = $doctrine;
    }

    public function execute(AMQPMessage $message) : int
    {
        $event = new Event($message->body);

        $this->doctrine->persist($event);
        $this->doctrine->flush();

        return ConsumerInterface::MSG_ACK;
    }
}
