const mongoose= require('mongoose')
const Schema = mongoose.Schema

var genericSchema = new Schema({ placeholder: Number }, { strict: false });

var GenericObject = mongoose.model('Generic', genericSchema);

module.exports = GenericObject