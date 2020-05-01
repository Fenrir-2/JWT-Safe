from flask import Flask
from flask import request
import flasgger
import json

app = Flask("Protected Ressource Access")
swagger = flasgger.Swagger(app)

@app.route('/api/access', methods=['GET'])
@flasgger.swag_from('docs/token_check.yml')
def token_check():
    token = request.args.get('token', default='', type=str)
    if token == '':
        return json.dumps({"Error" : "No token provided"})

    message = ''
    context = zmq.Context()
    try:
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://token_dealer:7000")
        socket.send_json({"check" : token})
    
        message = socket.recv_json()
    
        if message['status'] != "ok":
            return abort(403)
    
        if message['valid']:
            return json.dumps({"Status" : "Everything worked fine"})
    except:
        return json.dumps({"Error" : "No token dealer"})
