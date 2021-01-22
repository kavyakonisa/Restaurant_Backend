from flask import Flask
from flask import request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
#added the basic authentication using flask_httpauth
auth=HTTPBasicAuth()
#This callback function will use to obtain the password for a given user.
@auth.get_password
def get_password(username):
  if username=='kavya':
    return 'python'
  return None 

#error-handler callback is used when it needs to send an unauthorized error
@auth.error_handler
def unauthorized():
    response = jsonify({'error':'Unauthorized access'})
    return response, 404