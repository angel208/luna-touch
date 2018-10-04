var Joi = require('joi');
 
module.exports = {
  body: {
    text: Joi.string().required(),
    volume: Joi.number(),
    speed: Joi.number()
  },
  options:{
    status: 422,
    statusText: 'Unprocessable Entity',
    allowUnknownBody: false,
  },
};