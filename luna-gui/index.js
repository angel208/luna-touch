const ipc = require('electron').ipcRenderer;
var async = require("async");


$(document).on( 'click', '#start-btn', function(e){

    e.preventDefault(); 
    console.log("asd")
    ipc.send('load-page', './app-list.html');

})

