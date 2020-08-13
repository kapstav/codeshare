import datetime
import random
import uuid
from pykafka import KafkaClient, SslConfig
import argparse
from psycopg2.extras import RealDictCursor
import psycopg2
from KapsProducerSanDiego import KapsProducerSanDiego
from KapsProducerSanJose import KapsProducerSanJose
from KapsConsumerWeb import KapsConsumerWeb
from KapsConsumerMobile import KapsConsumerMobile
from configparser import ConfigParser

# from ConfigParser import ConfigParser  
config_file = 'config.ini'
configP = ConfigParser()
configP.read(config_file)
uri=configP['database']['postgresql_uri']
searchtxt=configP['testsearch']['sample'] #e.g.- like 'Tesla'

db_conn = psycopg2.connect(uri)
c = db_conn.cursor(cursor_factory=RealDictCursor)
def TestKafkatoDBStream(service_uri, ca_path, cert_path, key_path):
  
    #Running the two producers and two consumers in test mode
    KapsProducerSanJose(service_uri, ca_path, cert_path, key_path,"test")
    KapsProducerSanDiego(service_uri, ca_path, cert_path, key_path,"test")
    KapsConsumerMobile(service_uri, ca_path, cert_path, key_path);
    KapsConsumerWeb(service_uri, ca_path, cert_path, key_path);
    
    #Querying the number of fresh record created in the database should be 20. (5/producer X 2producer X 2consumer)
    c.execute("call testWebSearches("+searchtxt+",'')")
    result = c.fetchone()
    if (int(result['val']) >= 20):
        print("TestKafkatoDBStream Results Matched")
    else:
        print("TestKafkatoDBStream Results Did not Match")	
 	

