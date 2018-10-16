const ipc = require('electron').ipcRenderer;


$(document).on( 'click', '#start-btn', function(e){

    e.preventDefault(); 
    console.log("asd")
    ipc.send('load-page', './app-list.html');

})