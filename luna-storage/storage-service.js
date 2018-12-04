const express = require('express')
const app = express()

const config = require("./config.json")
const port = config.port

var bodyParser = require('body-parser')
app.use(bodyParser.json())


//===================MONGOSE CONNECTION=================

const mongoose = require('mongoose')

bluebird = require('bluebird')
mongoose.Promise = bluebird

const Evaluation = require('./models/evaluation')
const GenericObject = require('./models/generic')

mongoose.connect( "mongodb://"+config.mongo_host+"/"+config.mongo_db, { useNewUrlParser: true } )

mongoose.connection.once('open', function(){
    console.log('Connection success!')
}).on('error', function(error){
    console.log("connection eror:", error)
})

//==================================================

//this is validated using express-validation: https://www.npmjs.com/package/express-validation
app.post('/generic', (req, res) => {

    var request = req.body

    var genericObject = new GenericObject( request );

    genericObject.save().then( function(){

        console.log('saved')
        res.status(201).send( genericObject )

    }).catch(function(){

        console.log('saved')
        res.status(400).send( "Ups! Could not save that record."  )

    });

})

app.post('/evaluation', (req, res) => {

    var request = req.body

    var evalObject = new Evaluation( request );

    evalObject.save().then( function(){

        console.log('saved')
        res.status(201).send( evalObject )

    }).catch(function(){

        console.log('saved')
        res.status(400).send( "Ups! Could not save that record."  )

    });

})


app.get('/generic', (req, res) => {

    var request = req.body

    var GenericModel = GenericObject

    GenericModel.find( req.query ).then( function( err, docs){

        res.status(200).send( docs )

    }).catch(function(){

        res.status(400).send( "Ups! Could not save that record."  )

    });

})

app.get('/evaluation', (req, res) => {

    var request = req.body

    var EvalModel = Evaluation;

    EvalModel.find( req.query ).then( function( docs, err){
        console.log(err)
        console.log(docs)
        res.status(200).send( docs )

    }).catch(function(){

        res.status(400).send( "Ups! Could not save that record."  )

    });

})


app.listen(port, () => console.log(`Luna storage is listening on port ${port}!`))
 
