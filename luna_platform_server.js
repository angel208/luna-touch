const spawn = require("child_process").spawn;

const express = require('express')
const app = express()
var axios = require('axios')
var bodyParser = require('body-parser')
app.use(bodyParser.json())

const config = require("./config.json")
var port = config.port

//---- Starting up services ---
//TODO restart the service if the service needs to be up
//TODO enable/disable services withour restart (not a priority)

var t2s_service = null
var telegram_service = null 
var storage_service = null
var touch_service = null;

console.log("Starting services...")

if (config.touch_enabled){

    console.log("Starting touch services...")
    touch_service = spawn('node',["./luna-touch/luna_touch_service.py"]);

    touch_service.on('exit', function (code, signal) {
        console.log('Touch service exited with ' + `code ${code} and signal ${signal}`);
    });
    
    touch_service.on('error', function (err) {
        console.log('Error in the touch service:' + ` ${err}`);
    });
    

}
if (config.t2s_enabled){

    console.log("Starting text to speech services...")
    t2s_service = spawn('node',["./luna-text-2-speech/text-2-speech-service.js"]);

    t2s_service.on('exit', function (code, signal) {
        console.log('Text to speech service exited with ' + `code ${code} and signal ${signal}`);
    });
    
    t2s_service.on('error', function (err) {
        console.log('Error in the text to speech service:' + ` ${err}`);
    });

}
if (config.telegram_enabled){

    console.log("Starting telegram services...")
    telegram_service = spawn('node',["./luna-telegram/telegram-service.js"]);
    
    telegram_service.on('exit', function (code, signal) {
        console.log('Telegram service exited with ' + `code ${code} and signal ${signal}`);
    });

    telegram_service.on('error', function (err) {
        console.log('Error in the telegram service:' + ` ${err}`);
    });


}
if (config.storage_enabled){

    console.log("Starting storage services...")
    storage_service = spawn('node',["./luna-storage/storage-service.js"]);
    
    storage_service.on('exit', function (code, signal) {
        console.log('Storage service exited with ' + `code ${code} and signal ${signal}`);
    });
    
    storage_service.on('error', function (err) {
        console.log('Error in the storage service:' + ` ${err}`);
    });
}

console.log("Services started!")


//---------- Handling exit of this sever -------------------

//this handles Ctrl+C
process.on('SIGINT', function () {
    console.log('Ctrl-C...');
    
    process.exit(2);
});

process.on('exit', function () {
    process.emit('cleanup');
});

process.on('cleanup', function(){

    if (touch_service) touch_service.kill('SIGINT');
    if (t2s_service) t2s_service.kill('SIGINT');
    if (telegram_service) telegram_service.kill('SIGINT');
    if (storage_service) storage_service.kill('SIGINT');

    console.log("exited successfully!");
});

//------- Server Start ------------
app.listen(port, () => console.log(`Luna Platform is listening on port ${port}!`))
 
