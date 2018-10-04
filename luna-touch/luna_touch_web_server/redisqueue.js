var redis = require('redis')
var client = redis.createClient();

client.on('connect', function() {
    console.log('Redis client connected');
    console.log(qsize())
});

client.on('error', function (err) {
    console.log('Something went wrong ' + err);
});

function qsize(){
    client.BLPOP("luna-touch-queue", 0, function(err, reply) {
        console.log(reply); //prints 2
    });
}

