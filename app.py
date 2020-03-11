from flask import Flask
import random
import datetime
import time

app = Flask(__name__)


@app.route('/api/memory')
def memory():
    d = {}
    ts = time.time()
    value = random.randint(1, 101)
    d[ts] = value
    return d

@app.route('/api/cpu')
def cpu():
    d = {}
    ts = time.time()
    value = random.randint(1, 101)
    d[ts] = value
    return d

@app.route('/api/gpu')
def gpu():
    d = {}
    ts = time.time()
    value = random.randint(1, 101)
    d[ts] = value
    return d




if __name__ == '__main__':
    app.run()
