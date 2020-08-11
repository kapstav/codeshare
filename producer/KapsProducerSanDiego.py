import datetime
import random
import uuid
from pykafka import KafkaClient, SslConfig

#configuration object for pykafka connection. Refer Aiven Console for these immutable access files per account 
config = SslConfig(cafile='ca.pem',
                   certfile='service.cert', 
                   keyfile='service.key')   

#creating kafka client with Aiven kafka uri
client = KafkaClient(hosts="kapskafka-kapstav-dd56.aivencloud.com:18514",ssl_config=config);
#print(client.topics);


#creating a topic named KapsTopic
topic = client.topics[b"KapsTopic"]

print ("~~~~~~~~~~~~~~~Producer SD Started~~~~~~~~~~~~~~~~");

#random search string collection
Search_keywords = ['Floyd','Mail in','Trump', 'Covid', 'Matrix 4', 'China', 'Oxford', 'Reopening']

#creating a synchronus producer by pykafka library.
with topic.get_sync_producer() as producer:
     for i in range(5):
         msg=str("'").encode() \
	+ str(uuid.uuid4()).encode() + str("\',\'").encode() \
	+ b'WebPage' +  str(random.randint(1,20)).encode() \
	+ str("\',").encode()+str(random.randint(600,1200)).encode() \
	+ str(",'").encode() +str(random.choice(Search_keywords)).encode() \
	+ str("\',\'").encode() +str(datetime.datetime.now()).encode() \
	+ str("\',\'").encode() +b'San Diego' + str("\'").encode()
         print(msg)
         producer.produce(msg)
print ("~~~~~~~~~~~~~~~Producer SD Finished~~~~~~~~~~~~~~~~");
