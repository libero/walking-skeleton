<?php
use PhpAmqpLib\Connection\AMQPStreamConnection;
require_once 'vendor/autoload.php';
$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();
$channel->queue_declare('dashboard', $passive = false, $durable = true, $exclusive = false, $autoDelete = false);
$channel->exchange_declare('articles', 'fanout', $passive = false, $durable = true, $autoDelete = false);
$channel->queue_bind('dashboard', 'articles');
