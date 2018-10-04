const express = require('express')
const app = express()
var url = require('url');
const port = 5004

var redis = require('redis')
var client = redis.createClient();


client.on('connect', function() {
    console.log('Redis client connected');
});

client.on('error', function (err) {
    console.log('Something went wrong with redis client:' + err);
});


function prepare_json_string( string ){

    var result = string.replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']')
    return result

}

var touches =[
                {"area":24,"delta_position":[0,0],"delta_time":0,"frames_missing":0,"id":0,"position":[600,450],"radius":2,"state":1,"timestamp":1538328381053},
                {"area":23,"delta_position":[0,0],"delta_time":0,"frames_missing":0,"id":1,"position":[23,43],"radius":2,"state":2,"timestamp":1538328381053},
                {"area":23,"delta_position":[0,0],"delta_time":0,"frames_missing":0,"id":2,"position":[23,43],"radius":2,"state":2,"timestamp":1538328381053},
                {"area":23,"delta_position":[0,0],"delta_time":0,"frames_missing":0,"id":3,"position":[23,43],"radius":2,"state":3,"timestamp":1538328381053}
            ]
        
var touch_state_dictionary = { 'began' : 1, 'ended': 2, 'still': 3, 'moved' : 4 , 'missed': 5 }

var last_touch;

app.get('/touches', (req, res) => {

    

    client.LPOP("luna-touch-queue", function(err, reply) {

        if(err){
            res.status(500).send(err)
        }
        else{


            if(reply == null ){
                res.send(last_touch)
                console.log("empty")
            }else{

                var touches_reply = JSON.parse( prepare_json_string(reply) )
                last_touch = touches_reply

                if(req.query.state != undefined){
                    
                    if( req.query.state in touch_state_dictionary){

                        filtered_response_data = touches_reply.filter(function(o){

                            query_state = touch_state_dictionary[req.query.state]
                            return ( o.state == query_state )

                        });

                        res.status(200).send( filtered_response_data )
                    }
                    else{

                        res.status(404).send({ error: "invalid touch state. valid states: began, ended, still, missed, moved" })
                    }

                }
                else{
                    response_data = touches_reply
                    res.status(200).send(response_data)
                }
            }

        }

    }); 


   

})

app.get('/touches/:id', (req, res) => {
    
    res.send('Hello World! ' + req.params.id)

})

app.listen(port, () => console.log(`Luna touch is listening on port ${port}!`))