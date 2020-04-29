from kafka import KafkaConsumer
import ast
import config


class Consumer:

    consumer = KafkaConsumer('resource-monitor-metrics', client_id = "frontend", consumer_timeout_ms=4.95)
    metrics = {
        "cpu": [],
        "memory": [],
        "faults": [],
        "cpu_core": {},
        "processes": {},
        "network": [{}]
    }

    def poll_consumer(self):
        """
        Call poll on the consumer and then store the metrics gathered into the metrics dictionary
        :return:
        """
        poll_results = self.consumer.poll(timeout_ms=5000)
        # I need the list of keys because poll results unlike messages inside of consumer, is a dictionary not a list.
        keys = list(poll_results)
        for message in poll_results[keys[0]]:
            #Convert the message from bytes to utf
            dict_str = message.value.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            metric_type = mydata['metric_type']

            if metric_type == 'memory':
                self.metrics['memory'].append(mydata['utilization'])
                self.metrics['faults'].append(mydata['page_faults'])
            elif metric_type == 'cpu':
                self.metrics['cpu'].append(mydata['utilization'])
            elif metric_type == 'processes':
                #Check the configured memory value in config.py, as long as we are using more we will keep track of this
                #process
                if config.MIN_MEMORY <= mydata['memory']:
                    self.metrics['processes'][mydata['pid']] = {'memory': mydata['memory'], 'state': mydata['state'],
                                            'name': mydata['name']}
            elif metric_type == 'cpu_core':
                self.metrics['cpu_core'][mydata['core_id']] = mydata['core_utilization']
            elif metric_type == 'network':
                self.metrics['network'].append({"send": mydata['send'], 'receive': mydata['receive']})

    def get_memory_metrics(self):
        """
        Call poll_consumer and then return the latest memory metric
        :return: float
        """
        self.poll_consumer()
        return self.metrics['memory'][-1]

    def get_network_metrics(self):
        """
        Call poll consume rthen return the latest network statistics
        :return: dict
        """
        self.poll_consumer()
        return self.metrics['network'][-1]

    def get_system_metrics(self):

        for message in self.consumer:
            dict_str = message.value.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata['metric_type'] == 'system_metrics':
                return mydata

    def get_process_metrics(self):
        """
        Call poll consumer and then return the process dictionary.
        :return: dict
        """
        self.poll_consumer()
        #There is an edge case where the first call only gathers memory/cpu etc so until we find any process metrics we loop
        while len(list(self.metrics['processes'])) <= 1:
            self.poll_consumer()
        return self.metrics['processes']



    def get_cpu_core_metrics(self):
        """
        Call poll consumer and then return the cpu_core dictionary
        :return: dict
        """
        self.poll_consumer()
        return self.metrics['cpu_core']

    def get_cpu_metrics(self):
        """
        call poll consumer then return the latest utilization
        :return: float
        """
        self.poll_consumer()
        return self.metrics['cpu'][-1]

