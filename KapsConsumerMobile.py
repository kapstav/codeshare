import argparse
from psycopg2.extras import RealDictCursor
import psycopg2
from pykafka import KafkaClient, SslConfig
from configparser import ConfigParser

def KapsConsumerMobile(service_uri, ca_path, cert_path, key_path):

    # from ConfigParser import ConfigParser  
    config_file = 'config.ini'
 
    configP = ConfigParser()
    configP.read(config_file)
    
    uri=configP['database']['postgresql_uri']

    #connection string using psycopg2 library
    db_conn = psycopg2.connect(uri)

    #opening a cursor with dictionary objects as output
    c = db_conn.cursor(cursor_factory=RealDictCursor)

    #configuration object for pykafka connection. Refer Aiven Console for these immutable access files per account 
    configS = SslConfig(cafile=ca_path,certfile=cert_path,keyfile=key_path)   

    #creating kafka client with Aiven kafka uri
    client = KafkaClient(hosts=service_uri,ssl_config=configS);

     #retrieving the topic name from config file viz., KapsTopic
    topictxt=configP['kafka']['topic']
    topic = client.topics[str(topictxt).encode()]  
    
    print ("~~~~~~~~~~~~~~~Consumer Mobile Web Started~~~~~~~~~~~~~~~~");  
    
    #creating a simple consumer by pykafka.  
    consumer = topic.get_simple_consumer(consumer_group=b"Mobile",auto_commit_enable=True,auto_commit_interval_ms=1000,consumer_timeout_ms=1000)
    for message in consumer:
        if message is not None:
    
            messageval = str(message.value).replace("b\'","").replace("\"","").replace(",","|").replace("'","")
            print(messageval)
            xGUID = messageval.split("|")[0]
            xMobilePAGEID = messageval.split("|")[1]
            xTOTALHITS = messageval.split("|")[2]
            xMOSTSEARCHED = messageval.split("|")[3]
            xCRTDT = messageval.split("|")[4]
            xSRCREGION = messageval.split("|")[5]
             
            c.execute("CALL crtWebSearches(%s, %s, %s, %s, %s, %s, %s);", (xGUID,xMobilePAGEID, xTOTALHITS, xMOSTSEARCHED,xCRTDT,xSRCREGION, 'Mobile'))

            #committing the crud operation
            db_conn.commit() 

    #Close the current cursor
    c.close()

    #Close the connection
    db_conn.close()
    
    print ("~~~~~~~~~~~~~~~Consumer Mobile Web Finished~~~~~~~~~~~~~~~~");  

