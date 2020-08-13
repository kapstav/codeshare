import argparse
from psycopg2.extras import RealDictCursor
import psycopg2
from pykafka import KafkaClient, SslConfig
from configparser import ConfigParser
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable

def KapsConsumerWeb(ca_path, cert_path, key_path):

    # from ConfigParser import ConfigParser  
    config_file = 'config.ini'
 
    configP = ConfigParser()
    configP.read(config_file)
    
    #retrieving the service_uri name for kafka
    service_uri=configP['kafka']['service_uri']  
    
    db_uri=configP['database']['postgresql_uri']

    #connection string using psycopg2 library
    db_conn = psycopg2.connect(db_uri)

    #opening a cursor with dictionary objects as output
    c = db_conn.cursor(cursor_factory=RealDictCursor)

    #configuration object for pykafka connection. Refer Aiven Console for these immutable access files per account 
    configS = SslConfig(cafile=ca_path,certfile=cert_path,keyfile=key_path)   

    #creating kafka client with Aiven kafka uri
    client = KafkaClient(hosts=service_uri,ssl_config=configS);

     #retrieving the topic name from config file viz., KapsTopic
    topictxt=configP['kafka']['topic']
    topic = client.topics[str(topictxt).encode()]  
    
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

