import argparse
from psycopg2.extras import RealDictCursor
import psycopg2

from pykafka import KafkaClient, SslConfig

uri = "postgres://avnadmin:mycaz65d9c99lcdc@pgsql-kaps-kapstav-dd56.aivencloud.com:18512/defaultdb?sslmode=require"

db_conn = psycopg2.connect(uri)
c = db_conn.cursor(cursor_factory=RealDictCursor)

#c.execute("select * from public.\"CellPhoneWebSearches\"")
#result = c.fetchone()
#print(result)

config = SslConfig(cafile='ca.pem',
                   certfile='service.cert', 
                   keyfile='service.key')   

client = KafkaClient(hosts="kapskafka-kapstav-dd56.aivencloud.com:18514",ssl_config=config);
 
topic = client.topics[b"KapsTopic"]
 
consumer = topic.get_simple_consumer(consumer_group=b"Mobile",auto_commit_enable=True)
for message in consumer:
    if message is not None:
        #print(" [key=%18s, id=%5s, offset=%2s]" % (message.value, message.partition_key, message.offset));
        sqlstmt=("INSERT INTO public.\"CellPhoneWebSearches\" VALUES("+ str(message.value).replace("b\"","").replace("\"","")+",'Mobile'" +")")
        print(sqlstmt)
        c.execute(sqlstmt)
        db_conn.commit() 
c.close()
db_conn.close()

