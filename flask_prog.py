# webserver creates
# /close/<garage door name>
# /open/<garage door name>
# to open and close your garage door
# entry points produce 200 error code always
# output is useful for trouble shooting only

# Seperate entrypoint exists for testing, that is /secret/<messsage>
# which will output a reply that contains the message & 200 error code


import datetime
import time
import sys
from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/secret/<secret>")
def hello(secret):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    st = st + " " + secret
    print(st)
    return st


@app.route("/close/<garage>")
def close_garage(garage):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    output = ''
    error = 0
    strs = str(st) + " Closed " + garage
    try:
        subprocess.check_output(['python3', 'myq-garage.py', 'close', garage])
    except subprocess.CalledProcessError as Argument:
        strs = strs + str( Argument.returncode ) + str ( Argument.output)
    print(strs)
    return strs

@app.route("/open/<garage>")
def open_garage(garage):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    output = ''
    error = 0
    strs = str(st) + " Opened " + garage
    try:
        subprocess.check_output(['python3', 'myq-garage.py', 'open', garage])
    except subprocess.CalledProcessError as Argument:
        strs = strs + str( Argument.returncode ) + str ( Argument.output)
    print(strs)
    return strs

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
