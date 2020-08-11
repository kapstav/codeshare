from time import sleep
from json import dumps
from pykafka import KafkaClient, SslConfig
config = SslConfig(cafile='ca.pem',
                   certfile='service.cert', 
                   keyfile='service.key',
    		   auto_offset_reset="earliest",
    		   client_id="demo-client-1",
    		   group_id="demo-group")   

client = KafkaClient(hosts="kapskafka-kapstav-dd56.aivencloud.com:18514",ssl_config=config);
 
topic = client.topics[b"KapsTopic"]
 
consumer = topic.get_simple_consumer()
for message in consumer:
    if message is not None:
        print(message.offset, message.value)
print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
