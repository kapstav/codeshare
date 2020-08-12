import argparse
import datetime
import random
import uuid
import os
import sys 
from pykafka import KafkaClient, SslConfig

def KapsProducerSanDiego(service_uri, ca_path, cert_path, key_path):
    #configuration object for pykafka connection. Refer Aiven Console for these immutable access files per account 
    config = SslConfig(cafile=ca_path,certfile=cert_path,keyfile=key_path)   

    #creating kafka client with Aiven kafka uri
    client = KafkaClient(hosts=service_uri,ssl_config=config);
    #print(client.topics);


    #creating a topic named KapsTopic
    topic = client.topics[b"KapsTopic"]

    print ("~~~~~~~~~~~~~~~Producer SD Started~~~~~~~~~~~~~~~~");

    #random search string collection
    Search_keywords = ['Floyd','Mail in','Trump', 'Covid', 'Matrix 4', 'China', 'Oxford', 'Reopening']

    #creating a synchronus producer by pykafka library.
    with topic.get_sync_producer() as producer:
         for i in range(5):
         #generating 5 rows of randomized data with San Diego as tag
             msg = str(uuid.uuid4()).encode() + str("|").encode() \
             + b'WebPage' +  str(random.randint(1,20)).encode() \
             + str("|").encode()+str(random.randint(600,1200)).encode() \
             + str("|").encode() +str(random.choice(Search_keywords)).encode() \
             + str("|").encode() +str(datetime.datetime.now()).encode() \
             + str("|").encode() +b'San Diego'
             print(msg)
             producer.produce(msg)
    print ("~~~~~~~~~~~~~~~Producer SD Finished~~~~~~~~~~~~~~~~");
