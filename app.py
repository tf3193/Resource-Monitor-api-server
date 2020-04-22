from flask import Flask
import random
import datetime
import kafkaConsumer
import time
from flask_cors import CORS
import multiprocessing


app = Flask(__name__)
CORS(app)


@app.route('/api/memory')
def memory():
    d = {}
    value = kafkaConsumer.get_memory_metrics()
    d['value'] = value['utilization']
    return d

@app.route('/api/cpu')
def cpu():
    d = {}
    value = kafkaConsumer.get_cpu_metrics()
    d['value'] = value['utilization']
    return d

@app.route('/api/total_core')
def core_count():
    d = {}
    num_cores = multiprocessing.cpu_count()
    d['value'] = num_cores
    return d

@app.route('/api/core')
def core():
    value = kafkaConsumer.get_cpu_core_metrics()
    return value

@app.route('/api/gpu')
def gpu():
    d = {}
    ts = time.time()
    value = random.randint(1, 101)
    d[ts] = value
    return d




if __name__ == '__main__':
    app.run()
