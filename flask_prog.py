import datetime
import time
import sys
from flask import Flask
import subprocess

app = Flask(__name__)

# serves to test
@app.route("/secret/<secret>")
def hello(secret):
    st = generate_log_string('secret', secret)
    log(st)
    return st

# closes garage based on name
@app.route("/close/<garage>")
def close_garage(garage):
    return manipulate_garage('close', garage)

# opens garage based on name
@app.route("/open/<garage>")
def open_garage(garage):
    return manipulate_garage('open', garage)

# generate html string of logs in descending order
@app.route("/")
def dump_log_buffer():
    lines = logs[log_index:] + logs[:log_index]
    lines.reverse()
    return '<br>'.join(lines)
    
# log buffer
logs = 30 * ['']
log_index = 0

# log to buffer and 
def log(data):
    global logs
    global log_index
    print(data)
    logs[log_index] = data
    log_index = (log_index + 1)%len(logs)

def generate_log_string(command, data):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return str(st) + " " + command + " " + data

# does "open" or "close" of your named garage
def manipulate_garage(command, garage):
    strs = generate_log_string( command,  garage)
    try:
        subprocess.check_output(['python3', 'pymyq-wrapper.py', command, garage])
    except subprocess.CalledProcessError as Argument:
        strs = strs + str( Argument.returncode ) + " " + str ( Argument.output)
    log(strs)
    return strs


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
