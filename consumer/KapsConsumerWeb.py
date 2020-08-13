import argparse
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
import psycopg2
from pykafka import KafkaClient, SslConfig
from configparser import ConfigParser
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable, NoBrokersAvailableError,ConsumerStoppedException, PartitionOwnedError, UnknownTopicOrPartition
import sys 

def KapsConsumerWeb(ca_path, cert_path, key_path, db_cred):

    # from ConfigParser import ConfigParser  
    config_file = 'config.ini'
 
    configP = ConfigParser()
    configP.read(config_file)
    
    #retrieving the service_uri name for kafka
    service_uri=configP['kafka']['service_uri']  
    
    try:
        db_serv=configP['database']['postgresql_serv']
    except(KeyError) as e:
        print("-->Web Consumer::Can't read db server info from config.ini<--");
        sys.exit(1);
 
    db_uri="postgres://"+db_cred+db_serv

    #connection string using psycopg2 library
    try:
        db_conn = psycopg2.connect(db_uri)
    except (psycopg2.OperationalError) as e:
        print("-->Mobile Consumer::Unable to connect to a kafka broker, or the service is shutdown. Check the service_uri value in config.ini<--");
        sys.exit(1);

    #opening a cursor with dictionary objects as output
    c = db_conn.cursor(cursor_factory=RealDictCursor)

    #configuration object for pykafka connection. Refer Aiven Console for these immutable access files per account 
    configS = SslConfig(cafile=ca_path,certfile=cert_path,keyfile=key_path)   

    #creating kafka client with Aiven kafka uri
    try:
        client = KafkaClient(hosts=service_uri,ssl_config=configS);
    except(NoBrokersAvailableError) as e:
        print("-->SanDiego Producer::Unable to connect to a kafka broker. Check the service_uri value in config.ini<--");
        sys.exit(1);

    #retrieving the topic name from config file viz., KapsTopic
    try:
        topictxt=configP['kafka']['topic']
    except(KeyError) as e:
        print("-->Web Consumer::topic text can not be read from config.ini<--");
        sys.exit(1);
    try:
        topic = client.topics[str(topictxt).encode()]
    except(UnknownTopicOrPartition) as e:
        print("-->Web Consumer::this topic not found in the kafka ecosystem<--");
        sys.exit(1);
    
    print ("~~~~~~~~~~~~~~~Consumer Desktop Web Started~~~~~~~~~~~~~~~~");  
    
    #creating a simple consumer by pykafka.  
    consumer = topic.get_simple_consumer(consumer_group=b"Web",auto_commit_enable=True,auto_commit_interval_ms=1000,consumer_timeout_ms=1000)
    try:
        consumer.consume() #Try consuming. If there is a network error, retry one more time automatically.
    except (SocketDisconnectedError) as e:
        consumer = topic.get_simple_consumer(consumer_group=b"Web",auto_commit_enable=True,auto_commit_interval_ms=1000,consumer_timeout_ms=1000)
    
    for message in consumer:
        if message is not None:

            #print(" [key=%18s, id=%5s, offset=%2s]" % (message.value, message.partition_key, message.offset));
     
            messageval = str(message.value).replace("b\'","").replace("\"","").replace(",","|").replace("'","")
            print(messageval)
            xGUID = messageval.split("|")[0]
            xWEBPAGEID = messageval.split("|")[1]
            xTOTALHITS = messageval.split("|")[2]
            xMOSTSEARCHED = messageval.split("|")[3]
            xCRTDT = messageval.split("|")[4]
            xSRCREGION = messageval.split("|")[5]
             
            c.execute("CALL crtWebSearches(%s, %s, %s, %s, %s, %s, %s);", (xGUID,xWEBPAGEID, xTOTALHITS, xMOSTSEARCHED,xCRTDT,xSRCREGION, 'Web'))

            #committing the crud operation
            db_conn.commit() 

    #Close the current cursor
    c.close()

    #Close the connection
    db_conn.close()
    print ("~~~~~~~~~~~~~~~Consumer Desktop Web Finished~~~~~~~~~~~~~~~~");

