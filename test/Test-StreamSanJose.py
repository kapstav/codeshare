import datetime
import random
import uuid
from pykafka import KafkaClient, SslConfig
import argparse
from psycopg2.extras import RealDictCursor
import psycopg2

uri = "postgres://avnadmin:mycaz65d9c99lcdc@pgsql-kaps-kapstav-dd56.aivencloud.com:18512/defaultdb?sslmode=require"
db_conn = psycopg2.connect(uri)
c = db_conn.cursor(cursor_factory=RealDictCursor)

config = SslConfig(cafile='ca.pem',
                   certfile='service.cert', 
                   keyfile='service.key')   
client = KafkaClient(hosts="kapskafka-kapstav-dd56.aivencloud.com:18514",ssl_config=config);
#print(client.topics);
topic = client.topics[b"KapsTopic"]
guid=""
print ("~~~~~~~~~~~~~~~Producer SJ Started~~~~~~~~~~~~~~~~");
Search_keywords = ['Tesla']
with topic.get_sync_producer() as producer:
     for i in range(1):
         guid=uuid.uuid4()
         msg=str("'").encode() \
	+ str(guid).encode() + str("\',\'").encode() \
	+ b'WebPage' +  str("0").encode() \
	+ str("\',").encode()+str("9999").encode() \
	+ str(",'").encode() +str(random.choice(Search_keywords)).encode() \
	+ str("\',\'").encode() +str(datetime.datetime.now()).encode() \
	+ str("\',\'").encode() +b'San Jose' + str("\'").encode()
         #print(msg)
         producer.produce(msg)
print ("~~~~~~~~~~~~~~~Producer SJ Finished~~~~~~~~~~~~~~~~");


c.execute("select \"GUID\" from public.\"CellPhoneWebSearches\" where \"TOTALHITS\" = 9999 and \"WEBPAGEID\" ='WebPage0' order by \"CRTDT\" Desc")
result = c.fetchone()
rs  = result['GUID']
print(str(rs))
print(str(guid))
if str(rs) == str(guid):
	print("Results Matched")
else:
	print("Results Did not Match")	

