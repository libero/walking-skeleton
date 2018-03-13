<?php
use Interop\Queue\PsrConnectionFactory;
use Interop\Amqp\AmqpMessage;
use Enqueue\AmqpLib\AmqpConnectionFactory;

require_once 'vendor/autoload.php';

$connectionFactory = new AmqpConnectionFactory('amqp:');
/** @var PsrConnectionFactory $connectionFactory **/
$psrContext = $connectionFactory->createContext();

// TODO: set wrong name
$destination = $psrContext->createTopic('articles');

$message = $psrContext->createMessage(json_encode([
    'myid' => time(),
]));
$message->setDeliveryMode(AmqpMessage::DELIVERY_MODE_PERSISTENT);
echo $message->getBody(), PHP_EOL;

$psrContext->createProducer()->send($destination, $message);
