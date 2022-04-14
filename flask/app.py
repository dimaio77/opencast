
import json
import os
import random
import socket

from mpdclient import MyMPD, Dispatcher
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CONTENT_DIR = "/music"
LSOAP_DIR = "/home/liquidsoap/content/music"
cors = CORS(app)

@app.route('/mpd', methods=['GET', 'POST'])
def parse_request():
    if request.method == 'POST':
        command = request.form["command"].strip()
        #print "CMD %s" % command
        if " " in command:
            args = ' '.join(command.split()[1:])
            #print "ARGS", args
            command = command.split(' ')[0]
        else:
            args = None
        myclient = MyMPD()
        client = myclient.connect()
        disp = Dispatcher(client)
        return disp.dispatch(command, args)


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
    #app.run(host='0.0.0.0')
