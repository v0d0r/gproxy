#!/usr/bin/python
from flask import Flask, request, abort
from flup.server.fcgi import WSGIServer
import socket
from functools import wraps
from flask import request, Response
import logging

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'password'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


app = Flask(__name__)
app.config.from_object(__name__)
HOST = 'localhost'
PORT = 2003

@app.route('/upload', methods = ['POST'])
@requires_auth
def upload():
    if request.method == 'POST':
        data = request.form['data']
        if data:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((HOST,PORT))
            s.sendall(data)
            s.sendall("\n")
            s.close()
            app.logger.debug('sent %s to %s' % (data,HOST))
        else:
            app.logger.error("no data :(")
    return "OK"

if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/gproxy.log',level=logging.DEBUG,
     format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%b %d %H:%M:%S')
    app.run(host='0.0.0.0', port=5000)
