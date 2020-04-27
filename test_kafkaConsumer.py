import consumer
consumer.Consumer()

def test_get_cpu_metrics():
 data = consumer.get_cpu_metrics()
 assert data['metric_type'] == 'cpu'


def test_get_cpu_core_metrics():
 data = consumer.get_cpu_core_metrics()
 assert data['metric_type'] == 'cpu_core'


def test_get_memory_metrics():
 data = consumer.get_memory_metrics()
 assert data['metric_type'] == 'memory'

def test_get_network_metrics():
 data = consumer.get_network_metrics()
 assert data['metric_type'] == 'network'


def test_get_system_metrics():
 data = consumer.get_system_metrics()
 assert data['metric_type'] == 'system_metrics'


def test_get_cpu_metrics_value():
 data = consumer.get_cpu_metrics()
 assert data['utilization'] <= 1
 assert data['utilization'] >= 0


def test_get_cpu_core_metrics_value():
 data = consumer.get_cpu_core_metrics()
 for core in data:
  if core != "metric_type":
   assert data[core] <= 1
   assert data[core] >= 0


def test_get_memory_metrics_value():
 data = consumer.get_memory_metrics()
 assert data['utilization'] <= 1
 assert data['utilization'] >= 0




