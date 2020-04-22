from kafka import KafkaConsumer
import ast
import multiprocessing

def get_cpu_metrics():
 consumer = KafkaConsumer('resource-monitor-metrics')
 for message in consumer:
  dict_str = message.value.decode("UTF-8")
  mydata = ast.literal_eval(dict_str)
  if mydata['metric_type'] == 'cpu':
   return mydata

def get_cpu_core_metrics():
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
    core_dict['metric_type'] = 'cpu_core'
    return core_dict

def get_memory_metrics():
 consumer = KafkaConsumer('resource-monitor-metrics')

 for message in consumer:
  dict_str = message.value.decode("UTF-8")
  mydata = ast.literal_eval(dict_str)
  if mydata['metric_type'] == 'memory':
   return mydata

def get_network_metrics():
 consumer = KafkaConsumer('resource-monitor-metrics')
 for message in consumer:
  dict_str = message.value.decode("UTF-8")
  mydata = ast.literal_eval(dict_str)
  if mydata['metric_type'] == 'network':
   return mydata

def get_system_metrics():
 consumer = KafkaConsumer('resource-monitor-metrics')
 for message in consumer:
  dict_str = message.value.decode("UTF-8")
  mydata = ast.literal_eval(dict_str)
  if mydata['metric_type'] == 'system_metrics':
   return mydata




