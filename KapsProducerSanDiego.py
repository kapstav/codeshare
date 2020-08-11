import datetime
import random
import uuid
from pykafka import KafkaClient, SslConfig


config = SslConfig(cafile='ca.pem',
                   certfile='service.cert', 
                   keyfile='service.key')   
client = KafkaClient(hosts="kapskafka-kapstav-dd56.aivencloud.com:18514",ssl_config=config);
#print(client.topics);
topic = client.topics[b"KapsTopic"]

Search_keywords = ['Floyd','Mail in','Trump', 'Covid', 'Matrix 4', 'China', 'Oxford', 'Reopening']
 
print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
with topic.get_sync_producer() as producer:
     for i in range(5):
         producer.produce( str("'").encode() + str(uuid.uuid4()).encode() + str("\',\'").encode()
	+b'WebPage' +  str(random.randint(1,20)).encode() + str("\',").encode()
	+str(random.randint(600,1200)).encode() + str(",'").encode()
	+str(random.choice(Search_keywords)).encode() + str("\',\'").encode()
	+str(datetime.datetime.now()).encode() + str("\',\'").encode()
	+b'San Diego' + str("\'").encode())

consumer = topic.get_simple_consumer()
for message in consumer:
    if message is not None:
        print(message.offset, message.value)

# Force sending of all messages

#producer.flush()
#sleep(5);
#print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
