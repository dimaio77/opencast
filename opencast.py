#!/usr/bin/env python

#Vordun

'''

Receives commands from Second Life via HTTP
and sends them to mpd.

'''

from flask import Flask, request
from mpdclient import MyMPD, Dispatcher

app = Flask(__name__)


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
    app.run(host='0.0.0.0', port=5000)

