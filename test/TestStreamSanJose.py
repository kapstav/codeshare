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
 
uri = "postgres://avnadmin:mycaz65d9c99lcdc@pgsql-kaps-kapstav-dd56.aivencloud.com:18512/defaultdb?sslmode=require"
db_conn = psycopg2.connect(uri)
c = db_conn.cursor(cursor_factory=RealDictCursor)
def TestStreamSanJose(service_uri, ca_path, cert_path, key_path):
    c.execute("DELETE from public.\"CellPhoneWebSearches\"")
    c.execute("DELETE from public.\"DesktopWebSearches\"")
    KapsProducerSanJose(service_uri, ca_path, cert_path, key_path)
    KapsConsumerMobile(service_uri, ca_path, cert_path, key_path);
    KapsConsumerWeb(service_uri, ca_path, cert_path, key_path);
    c.execute("select count(*) num from public.\"CellPhoneWebSearches\"")
    result1 = c.fetchone()
    c.execute("select count(*) num from public.\"DesktopWebSearches\"")
    result2 = c.fetchone()
    if (result1['num']+result2['num'] == 10):
        print("TestStreamSanJose Results Matched")
    else:
        print("TestStreamSanJose Results Did not Match")	

