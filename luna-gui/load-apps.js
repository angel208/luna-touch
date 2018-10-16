const ipc = require('electron').ipcRenderer;

const fs = require('fs');
const path = require('path');

var exec = require('child_process').execFile;

//TODO handle exec errors
//TODO adding images
//TODO visuals of the menu
//TODO create and link main window with big start button


appFolder = path.join(__dirname,"./apps")
iconFolder = path.join(__dirname,"./icons")

fs.readdir(appFolder, (err, app_folders) => {

  app_folders.forEach( app_folder => {

    app_root_dir = path.join(__dirname, "apps", app_folder)

    app_exec = get_executable_in_directory(app_root_dir)

    let app_exec_path = path.join( app_root_dir, String(app_exec))


    if ( app_exec != undefined ){

        $("#app-list").append(
            $('<div>').attr('class', 'card').append(
                $('<button>').attr('class', 'app').attr('value', app_exec_path).append(
                    $('<div>').attr('class', 'card-image').append(
                        $('<img>').attr('src', './icons/Luna Simple Piano.jpg')
        ))))


    }

  });

})

$(document).on( 'click', '#back-btn', function(e){

    e.preventDefault(); 
    console.log("asd")
    ipc.send('load-page', './index.html');

})


$(document).on( 'click', '.app', function(e){

    e.preventDefault(); 
    var app = $(this).val()
    execute_app( app )

    console.log( app )

})

function execute_app( exe ){

    console.log("executing: " + exe );

    exec( exe , function(err, data) {  
         console.log(err)
         console.log(data.toString());   
         console.log('TERMINATED')                    
     });  

 }

function get_executable_in_directory( app_dir ){

    let app_dir_content = fs.readdirSync( app_dir );
    let file_exec = app_dir_content.filter( function( elm ) {return elm.match(/.*\.exe/ig);})[0];

    return file_exec;

}

function get_icon_in_directory( icon_dir, app_name ){

    let icon_dir_content = fs.readdirSync( icon_dir );

    var re = new RegExp( app_name + ".*", "g");

    let file_exec = icon_dir_content.filter( function( elm ) {return elm.match(re);})[0];

    return file_exec;

}


