<?php
use Interop\Queue\PsrConnectionFactory;
use Interop\Amqp\AmqpTopic;
use Interop\Amqp\AmqpQueue;
use Interop\Amqp\Impl\AmqpBind;
use Enqueue\AmqpLib\AmqpConnectionFactory;

require_once 'vendor/autoload.php';

$connectionFactory = new AmqpConnectionFactory('amqp:');
/** @var PsrConnectionFactory $connectionFactory **/
$psrContext = $connectionFactory->createContext();

$articlesTopic = $psrContext->createTopic('articles');
$articlesTopic->setType(AmqpTopic::TYPE_FANOUT);
$articlesTopic->setFlags(AmqpTopic::FLAG_DURABLE);
$psrContext->declareTopic($articlesTopic);

$dashboardQueue = $psrContext->createQueue('dashboard');
$dashboardQueue->addFlag(AmqpQueue::FLAG_DURABLE);
$psrContext->declareQueue($dashboardQueue);

$psrContext->bind(new AmqpBind($articlesTopic, $dashboardQueue));


