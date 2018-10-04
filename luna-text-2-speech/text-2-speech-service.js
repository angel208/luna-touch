const express = require('express')
const app = express()

const config = require("./config.json")
const port = config.port

var validate = require('express-validation')
var validation = require('./validation/talk.js');

var bodyParser = require('body-parser')
app.use(bodyParser.json())

const SimpleTTS = require("simpletts")
const tts = new SimpleTTS()

//text-2-speech init
tts.getVoices().then((voices) => {
 
    console.log(voices[0].name)
    console.log(voices[0].gender)
 
}).catch((err) => {
    console.log(err)
});

//this is validated using express-validation: https://www.npmjs.com/package/express-validation
app.post('/speak', validate(validation), (req, res) => {

    var request = req.body

    // is equal to { "text": "this is a test", "voice": voices[0], "volume": 100, "speed": 50 }
    tts.read(request).then(() => { 
        console.log("Ok")
        res.status(200).send("request successful")
    }).catch((err) => {
        console.log(err)
        res.status(500).send("error while processing your request")
    });  

})

app.listen(port, () => console.log(`Luna text-2-speech is listening on port ${port}!`))
 
