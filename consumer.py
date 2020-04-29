from kafka import KafkaConsumer
import ast
import constants
import config

class Consumer:
    consumer = KafkaConsumer('resource-monitor-metrics', client_id="frontend")
    # This is initialized just for sanity sake and for a bit of clarity for modifying in the future.
    metrics = {
        constants.CPU: [],
        constants.MEMORY: [],
        constants.PAGE_FAULTS: [],
        constants.CPU_CORE: {},
        constants.PROCESSES: {},
        constants.NETWORK: [{}]
    }

    def poll_consumer(self):
        """
        Call poll on the consumer and then store the metrics gathered into the metrics dictionary
        :return:
        """

        poll_results = self.consumer.poll(timeout_ms=5000)
        # I need the list of keys because poll results unlike messages inside of consumer, is a dictionary not a list.
        keys = list(poll_results)
        # This handles an edge case to fail gracefully.
        if len(keys) == 0:
            return

        for message in poll_results[keys[0]]:
            # Convert the message from bytes to utf
            dict_str = message.value.decode("UTF-8")
            metric_dict = ast.literal_eval(dict_str)
            metric_type = metric_dict['metric_type']

            if metric_type == constants.MEMORY:
                self.metrics[constants.MEMORY].append(metric_dict[constants.UTILIZATION])
                self.metrics[constants.PAGE_FAULTS].append(metric_dict[constants.PAGE_FAULTS])
            elif metric_type == constants.CPU:
                self.metrics[constants.CPU].append(metric_dict[constants.UTILIZATION])
            elif metric_type == constants.PROCESSES:
                # Check the constantsured memory value in constants.py, as long as we are using more we will keep
                # track of this process
                if config.MIN_MEMORY <= metric_dict[constants.MEMORY]:
                    self.metrics[constants.PROCESSES][metric_dict[constants.PID]] = {
                        constants.MEMORY: metric_dict[constants.MEMORY],
                        constants.STATE: metric_dict[constants.STATE],
                        constants.NAME: metric_dict[constants.NAME]}
            elif metric_type == constants.CPU_CORE:
                self.metrics[constants.CPU_CORE][metric_dict[constants.CORE_ID]] = \
                    metric_dict[constants.CORE_UTILIZATION]
            elif metric_type == constants.NETWORK:
                self.metrics[constants.NETWORK].append({constants.SEND: metric_dict[constants.SEND],
                                                        constants.RECEIVE: metric_dict[constants.RECEIVE]})

    def get_memory_metrics(self):
        """
        Call poll_consumer and then return the latest memory metric
        :return: float
        """
        self.poll_consumer()
        return self.metrics[constants.MEMORY][-1]

    def get_network_metrics(self):
        """
        Call poll consume rthen return the latest network statistics
        :return: dict
        """
        self.poll_consumer()
        return self.metrics[constants.NETWORK][-1]

    def get_process_metrics(self):
        """
        Call poll consumer and then return the process dictionary.
        :return: dict
        """
        self.poll_consumer()
        # There is an edge case where the first call only gathers memory/cpu etc so until we find any process metrics we loop
        while len(list(self.metrics[constants.PROCESSES])) < 1:
            self.poll_consumer()
        return self.metrics[constants.PROCESSES]

    def get_cpu_core_metrics(self):
        """
        Call poll consumer and then return the cpu_core dictionary
        :return: dict
        """
        self.poll_consumer()
        return self.metrics[constants.CPU_CORE]

    def get_cpu_metrics(self):
        """
        call poll consumer then return the latest utilization
        :return: float
        """
        self.poll_consumer()
        return self.metrics[constants.CPU][-1]
