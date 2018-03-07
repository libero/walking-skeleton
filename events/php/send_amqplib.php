<?php
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;
require_once 'vendor/autoload.php';

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();
$channel->set_ack_handler(
    function (AMQPMessage $message) {
        echo "Message acked with content " . $message->body . PHP_EOL;
    }
);

$channel->confirm_select();
/*
    name: $exchange
    type: fanout
    passive: false // don't check if an exchange with the same name exists
    durable: false // the exchange won't survive server restarts
    auto_delete: true //the exchange will be deleted once the channel is closed.
*/
//$channel->exchange_declare($exchange, 'fanout', false, false, true);
$msg = new AMQPMessage((string) time());
$channel->basic_publish($msg, 'articles');
$channel->wait_for_pending_acks();
$channel->close();
$connection->close();
