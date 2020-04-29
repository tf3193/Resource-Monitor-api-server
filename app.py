from flask import Flask
from flask_cors import CORS
import multiprocessing
import consumer

consumer = consumer.Consumer()

app = Flask(__name__)
CORS(app)


@app.route('/api/memory')
def memory():
    value = consumer.get_memory_metrics()
    return {'value': value}

@app.route('/api/cpu')
def cpu():
    value = consumer.get_cpu_metrics()
    return {'value': value}

@app.route('/api/total_core')
def core_count():
    num_cores = multiprocessing.cpu_count()
    return {'value': num_cores}

@app.route('/api/core')
def core():
    value = consumer.get_cpu_core_metrics()
    return value

@app.route('/api/processes')
def process():
    value = consumer.get_process_metrics()
    return value


if __name__ == '__main__':
    app.run()
