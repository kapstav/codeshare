import argparse
from psycopg2.extras import RealDictCursor
import psycopg2
from pykafka import KafkaClient, SslConfig

def KapsConsumerWeb(service_uri, ca_path, cert_path, key_path):
    #uri provided by Aiven console for postgres sql connection
    uri = "postgres://avnadmin:mycaz65d9c99lcdc@pgsql-kaps-kapstav-dd56.aivencloud.com:18512/defaultdb?sslmode=require"

    #connection string using psycopg2 library
    db_conn = psycopg2.connect(uri)

    #opening a cursor with dictionary objects as output
    c = db_conn.cursor(cursor_factory=RealDictCursor)

    #configuration object for pykafka connection. Refer Aiven Console for these immutable access files per account 
    config = SslConfig(cafile=ca_path,certfile=cert_path,keyfile=key_path)   

    #creating kafka client with Aiven kafka uri
    client = KafkaClient(hosts=service_uri,ssl_config=config);
    #print(client.topics);


    #creating a topic named KapsTopic
    topic = client.topics[b"KapsTopic"]
     
    print ("~~~~~~~~~~~~~~~Consumer Desktop Web Started~~~~~~~~~~~~~~~~");
         
    #creating a simple consumer by pykafka. 
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

