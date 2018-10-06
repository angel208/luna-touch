const { app, BrowserWindow } = require('electron')
const path = require('path')
const spawn = require("child_process").spawn

const fs = require('fs');

//only for dev purposes!!
require('electron-reload')(__dirname);
/*require('electron-reload')(__dirname, {
    electron: path.join(__dirname, 'node_modules', '.bin', 'electron')
  });*/

 //TODO adding some way to know if the process started successfully
  
// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.

let apps_window 
var luna_service

function createWindow () {

    apps_window = new BrowserWindow({ width: 800, height: 600 })

    apps_window.loadFile('index.html')

    // Open the DevTools.
    apps_window.webContents.openDevTools() 

    // Emitted when the window is closed.
    apps_window.on('closed', () => {
        if( luna_service ) luna_service.kill('SIGINT')
        apps_window = null
    })
  
}

exports.apps_window = apps_window;

//------------ LIFECICLE -------------

app.on('ready', () => {

    console.log("Starting Luna services...")
    luna_service = spawn('node',[path.join(__dirname,"../luna_platform_server.js")]);

    luna_service.on('exit', function (code, signal) {
        console.log('Text to speech service exited with ' + `code ${code} and signal ${signal}`);
    });
    
    luna_service.on('error', function (err) {
        console.log('Error in the text to speech service:' + ` ${err}`);
    });

    createWindow();

})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

//only for mac
app.on('activate', () => {
    if (apps_window === null) {
        createWindow()
    }
})

//------------------------------------------------
