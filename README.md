# capping-api-server
This is an api server which assumes you have Kafka already running on your localhost. This will create a flask server
with various endpoints which can be accessed via http get requests. Currently it supports Memory, CPU, CPU cores, and 
processes.

## Running the API Server
You must have already started kafka and the kafka resource gatherer [here](https://github.com/jonathansavas/marist-mscs710-capping-project/tree/adding-modules)
Once you have started the resource gatherer you can simply start the server with `python app.py`.
