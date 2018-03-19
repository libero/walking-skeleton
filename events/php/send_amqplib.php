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
$msg = new AMQPMessage((string) time(), [
    'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
]);
$channel->basic_publish($msg, 'articles');
$channel->wait_for_pending_acks();
$channel->close();
$connection->close();
