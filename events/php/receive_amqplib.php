<?php
use PhpAmqpLib\Message\AMQPMessage;
use PhpAmqpLib\Connection\AMQPStreamConnection;
require_once 'vendor/autoload.php';
$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();

$exit = false;
$signalHandler = function() use ($channel, &$exit) {
    $channel->basic_cancel(null, false, true);
    $exit = true;
};
pcntl_signal(SIGTERM, $signalHandler);
pcntl_signal(SIGINT, $signalHandler);
pcntl_signal(SIGQUIT, $signalHandler);

$channel->basic_consume('dashboard', null, false, false, false, false, function(AMQPMessage $message) use ($channel) {
    echo $message->body, PHP_EOL;
    $channel->basic_ack($message->delivery_info['delivery_tag']);
});

while (!$exit) {
    echo "Waiting for new message", PHP_EOL;
    $channel->wait();
}
echo "Graceful shutdown", PHP_EOL;
