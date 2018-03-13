<?php
use Interop\Queue\PsrConnectionFactory;
use Enqueue\AmqpLib\AmqpConnectionFactory;

require_once 'vendor/autoload.php';

$connectionFactory = new AmqpConnectionFactory('amqp:');
/** @var PsrConnectionFactory $connectionFactory **/
$psrContext = $connectionFactory->createContext();

$source = $psrContext->createQueue('dashboard');

$consumer = $psrContext->createConsumer($source);

$message = $consumer->receive();
echo $message->getBody(), PHP_EOL;
$consumer->acknowledge($message);
