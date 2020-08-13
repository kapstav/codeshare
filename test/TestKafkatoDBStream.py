import datetime
import random
import uuid
from pykafka import KafkaClient, SslConfig
import argparse
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
import psycopg2
from KapsProducerSanDiego import KapsProducerSanDiego
from KapsProducerSanJose import KapsProducerSanJose
from KapsConsumerWeb import KapsConsumerWeb
from KapsConsumerMobile import KapsConsumerMobile
from configparser import ConfigParser
import sys 

# from ConfigParser import ConfigParser  
config_file = 'config.ini'
configP = ConfigParser()
configP.read(config_file)
try:
    db_serv=configP['database']['postgresql_serv']
except(KeyError) as e:
    print("-->Test Kafka::Can't read db server info from config.ini<--");
    sys.exit(1);
db_uri="postgres://"+"avnadmin:mycaz65d9c99lcdc@"+db_serv
service_uri=configP['kafka']['service_uri']  
searchtxt=configP['testsearch']['sample'] #e.g.- like 'Tesla'

    
try:
    db_conn = psycopg2.connect(db_uri)
except (psycopg2.OperationalError) as e:
    print("-->TestKafka2DB Consumer::Unable to connect to a PostgreSQL Server. Check the service_uri value in config.ini<--");
    sys.exit(1);
c = db_conn.cursor(cursor_factory=RealDictCursor)
def TestKafkatoDBStream(ca_path, cert_path, key_path, db_cred):
  
    #Running the two producers and two consumers in test mode
    KapsProducerSanJose(ca_path, cert_path, key_path,"test")
    KapsProducerSanDiego(ca_path, cert_path, key_path,"test")
    KapsConsumerMobile(ca_path, cert_path, key_path, db_cred);
    KapsConsumerWeb(ca_path, cert_path, key_path, db_cred);
    
    #Querying the number of fresh record created in the database should be 20. (5/producer X 2producer X 2consumer)
    c.execute("call testWebSearches("+searchtxt.replace("','",",")+",'')")
    result = c.fetchone()
    if (int(result['val']) >= 20):
        print("TestKafkatoDBStream Results Matched")
    else:
        print("TestKafkatoDBStream Results Did not Match")	
 	

