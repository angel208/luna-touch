const mongoose= require('mongoose')
const Schema = mongoose.Schema

const EvaluationSchema = new Schema({
    subject: { type: String },
    class: { required: true, type:Number },
    app: { required: true, type:String },
    student: { required: true,type:String },
    results: [
        {
            goal: String,
            value: String
        }
    ]
})

//(collection, schema)
const Evaluation = mongoose.model('evaluation', EvaluationSchema)

module.exports = Evaluation

