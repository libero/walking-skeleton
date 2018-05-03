<?php

namespace Libero\Dashboard\Consumer;

use OldSound\RabbitMqBundle\RabbitMq\ConsumerInterface;
use PhpAmqpLib\Message\AMQPMessage;

final class EventsConsumer implements ConsumerInterface
{
    public function execute(AMQPMessage $message) : int
    {
        echo $message->body, PHP_EOL;

        return ConsumerInterface::MSG_ACK;
    }
}
