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
            $('<li>').append(
                $('<button>').attr('class', 'app').attr('type', 'button').attr('value', app_exec_path).append(
                    $('<span>').attr('class', 'tab').append(app_folder)
        )))

    }

  });

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


