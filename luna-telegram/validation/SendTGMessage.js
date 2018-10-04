var Joi = require('joi');
 
module.exports = {
  body: {
    message: Joi.string().required(),
  },
  options:{
    status: 422,
    statusText: 'Unprocessable Entity',
    allowUnknownBody: false,
  },
};