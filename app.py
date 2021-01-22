from flask import Flask
from flask import request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from authenticate import auth
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
 app.run()