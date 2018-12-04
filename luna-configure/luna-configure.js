const { app, BrowserWindow } = require('electron')
const path = require('path')
const spawn = require("child_process").spawn
const ipcMain = require('electron').ipcMain;

const url = require("url");

const fs = require('fs');

//only for dev purposes!!
require('electron-reload')(__dirname);
/*require('electron-reload')(__dirname, {
    electron: path.join(__dirname, 'node_modules', '.bin', 'electron')
  });*/

 //TODO adding some way to know if the process started successfully
 //TODO block if clicked once
  
// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.

let apps_window 
var luna_service

function createWindow () {

    apps_window = new BrowserWindow({ width: 800, height: 600 })

    apps_window.loadURL(
        url.format({
          pathname: path.join(__dirname, `./dist/luna-configure/index.html`),
          protocol: "file:",
          slashes: true
        })
    );

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
