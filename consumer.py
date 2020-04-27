from kafka import KafkaConsumer
import ast
import multiprocessing
import config

class Consumer:
    def get_memory_metrics(self):
        consumer = KafkaConsumer('resource-monitor-metrics')
        for message in consumer:
            dict_str = message.value.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata['metric_type'] == 'memory':
                return mydata

    def get_network_metrics(self):
        consumer = KafkaConsumer('resource-monitor-metrics')
        for message in consumer:
            dict_str = message.value.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata['metric_type'] == 'network':
                return mydata

    def get_system_metrics(self):
        consumer = KafkaConsumer('resource-monitor-metrics')
        for message in consumer:
            dict_str = message.value.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata['metric_type'] == 'system_metrics':
                return mydata

    def get_process_metrics(self):
        consumer = KafkaConsumer('resource-monitor-metrics', consumer_timeout_ms=4900)
        processes = {}
        for message in consumer:
            dict_str = message.value.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata['metric_type'] == 'processes':
                if mydata['memory'] >= config.MIN_MEMORY:
                    processes[mydata['pid']] = {'memory': mydata['memory'], 'state': mydata['state'], 'name': mydata['name']}
        return processes


    def get_cpu_core_metrics(self):
        num_cores = multiprocessing.cpu_count()
        consumer = KafkaConsumer('resource-monitor-metrics')
        count = 0
        core_dict = {}
        for message in consumer:
            dict_str = message.value.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata['metric_type'] == 'cpu_core':
                core_dict[mydata['core_id']] = mydata['core_utilization']
                count += 1
                if count == num_cores:
                    return core_dict

    def get_cpu_metrics(self):
        consumer = KafkaConsumer('resource-monitor-metrics')
        for message in consumer:
            dict_str = message.value.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata['metric_type'] == 'cpu':
                return mydata

