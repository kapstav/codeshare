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
db_uri=configP['database']['postgresql_uri']
service_uri=configP['kafka']['service_uri']  
searchtxt=configP['testsearch']['sample'] #e.g.- like 'Tesla'

    
db_conn = psycopg2.connect(db_uri)
c = db_conn.cursor(cursor_factory=RealDictCursor)
def TestKafkatoDBStream(ca_path, cert_path, key_path):
  
    #Running the two producers and two consumers in test mode
    KapsProducerSanJose(ca_path, cert_path, key_path,"test")
    KapsProducerSanDiego(ca_path, cert_path, key_path,"test")
    KapsConsumerMobile(ca_path, cert_path, key_path);
    KapsConsumerWeb(ca_path, cert_path, key_path);
    
    #Querying the number of fresh record created in the database should be 20. (5/producer X 2producer X 2consumer)
    c.execute("call testWebSearches("+searchtxt.replace("','",",")+",'')")
    result = c.fetchone()
    if (int(result['val']) >= 20):
        print("TestKafkatoDBStream Results Matched")
    else:
        print("TestKafkatoDBStream Results Did not Match")	
 	

