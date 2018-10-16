const mongoose= require('mongoose')
const Schema = mongoose.Schema

const EvaluationSchema = new Schema({
    name: String,
    weigth: Number
})

//(collection, schema)
const Evaluation = mongoose.model('evaluation', EvaluationSchema)

module.exports = Evaluation

