#invocation:py runkafka.py --key-path="./service.key" --cert-path="./service.cert" --ca-path="./ca.pem" --db-cred="avnadmin:mycaz65d9c99lcdc@" --producer
import argparse
import datetime
import random
import uuid
import os
import sys 
from pykafka import KafkaClient, SslConfig
from configparser import ConfigParser
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable, NoBrokersAvailableError,ConsumerStoppedException, PartitionOwnedError, UnknownTopicOrPartition

def KapsProducerSanDiego(ca_path, cert_path, key_path, db_cred, runmode="standard"):

    # from ConfigParser import ConfigParser  
    config_file = 'config.ini'
 
    configP = ConfigParser()
    configP.read(config_file)
    
    #configuration object for pykafka connection. Refer Aiven Console for these immutable access files per account 
    configS = SslConfig(cafile=ca_path,certfile=cert_path,keyfile=key_path)   

    #retrieving the service_uri name for kafka
    service_uri=configP['kafka']['service_uri']  
    
    #creating kafka client with Aiven kafka uri
    try:
        client = KafkaClient(hosts=service_uri,ssl_config=configS);
    except(NoBrokersAvailableError) as e:
        print("-->SanDiego Producer::Unable to connect to a kafka broker, or the service is shutdown. Check the service_uri value in config.ini<--");
        sys.exit(1);

    #random search string collection
    try:
        if(runmode=="test"):    searchtxt=configP['testsearch']['sample']
        else:   searchtxt=configP['search']['sample']
        Search_keywords = eval('[' + searchtxt + ']') # e.g. - ['Floyd','Mail in','Trump', 'Covid', 'Matrix 4', 'China', 'Oxford', 'Reopening']
    except(KeyError) as e:
        print("-->SanDiego Producer::Unable to read appropriate section in config.ini<--");
        sys.exit(1);
        
    #retrieving the topic name from config file viz., KapsTopic
    try:
        topictxt=configP['kafka']['topic']
    except(KeyError) as e:
        print("-->SanDiego Producer::topic text can not be read from config.ini<--");
        sys.exit(1);
    try:
        topic = client.topics[str(topictxt).encode()]
    except(UnknownTopicOrPartition) as e:
        print("-->SanDiego Producer::this topic not found in the kafka ecosystem<--");
        sys.exit(1);

    print ("~~~~~~~~~~~~~~~Producer SD Started~~~~~~~~~~~~~~~~");
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
             try:
                producer.produce(msg)
             except (SocketDisconnectedError, LeaderNotAvailable, PartitionOwnedError) as e:
                print("-->Unable to connect to a kafka broker. Retrying..<--");
                producer = topic.get_sync_producer()
                producer.produce(msg)
    print ("~~~~~~~~~~~~~~~Producer SD Finished~~~~~~~~~~~~~~~~");
