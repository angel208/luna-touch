const express = require('express')
const app = express()

const config = require("./config.json")
const fs = require('fs'); 

var port = config.port

var validate = require('express-validation')
var validation = require('./validation/SendTGMessage.js');

var bodyParser = require('body-parser')
app.use(bodyParser.json())

/* TODO 

fill the help message
create strings file

make help and start regexp case insensitive
define the negative regexp (anything but help and start)

*/


const TelegramBot = require('node-telegram-bot-api');
 
// replace the value below with the Telegram token you receive from @BotFather
const token = config.bot_token;
 
// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, {polling: true});

var chatId;
 
// Matches "/start"
bot.onText(/start/, (msg, match) => {
  
  chatId = msg.chat.id;

  config.chat_id = chatId 
  save_chat_id_to_config( chatId )

  // send the response to the chat
  bot.sendMessage(chatId, "The bot has been registered in Luna! now you can receive notifications about the classroom activities in this chat.");

});

bot.onText(/help/, (msg, match) => {
  
    // send the response to the chat
    bot.sendMessage(config.chat_id, "help placeholder");
  
  });


bot.onText(/anything/, (msg, match) => {
  
    // send the response to the chat
    bot.sendMessage(config.chat_id, "This bot is only for notification purposes. for more information type 'help'");
  
});

//this is validated using express-validation: https://www.npmjs.com/package/express-validation
app.post('/message', validate(validation), (req, res) => {

    if( config.chat_id != undefined){

        var message = req.body.message

        // send the message to the chat
        bot.sendMessage( config.chat_id , message );
        res.status(200).send("success!")

    }
    else{

        res.status(403).send("The bot has not been registered in Luna. Please enter the command '/start' in the chat with your bot and try again.")

    }
    
    
})

function save_chat_id_to_config( id ){

    var jsonContent = JSON.stringify( config ); 

    fs.writeFile("./config.json", jsonContent, 'utf8', function (err) {
        if (err) {
            console.log("An error occured while writing JSON Object to File.");
            return console.log(err);
        }
     
        console.log("JSON file has been saved.");
    }); 
}

app.listen(port, () => console.log(`Luna Telegram module is listening on port ${port}!`))
 
