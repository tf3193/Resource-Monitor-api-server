import kafkaConsumer
import pytest

def test_get_cpu_metrics():
 data = kafkaConsumer.get_cpu_metrics()
 assert data['metric_type'] == 'cpu'

def test_get_cpu_core_metrics():
 data = kafkaConsumer.get_cpu_core_metrics()
 assert data['metric_type'] == 'cpu_core'

def test_get_memory_metrics():
 data = kafkaConsumer.get_memory_metrics()
 assert data['metric_type'] == 'memory'

def test_get_network_metrics():
 data = kafkaConsumer.get_network_metrics()
 assert data['metric_type'] == 'network'


def test_get_system_metrics():
 data = kafkaConsumer.get_system_metrics()
 assert data['metric_type'] == 'system_metrics'




