#invocation:py runkafka.py --key-path="service.key" --cert-path="service.cert" --ca-path="ca.pem" --service-uri="kapskafka-kapstav-dd56.aivencloud.com:18514"
import argparse
import datetime
import random
import uuid
import os
import sys 
from pykafka import KafkaClient, SslConfig
from KapsProducerSanDiego import KapsProducerSanDiego
from KapsProducerSanJose import KapsProducerSanJose
from KapsConsumerWeb import KapsConsumerWeb
from KapsConsumerMobile import KapsConsumerMobile

def validate_args(args):
   for path_option in ("ca_path", "key_path", "cert_path"):
       path = getattr(args, path_option)
       if not os.path.isfile(path):
           fail(f"Failed to open --{path_option.replace('_', '-')} at path: {path}.\n"
                f"You can get these details from Overview tab in the Aiven Console")
   if args.producer and args.consumer:
       fail("--producer and --consumer are mutually exclusive")
   elif not args.producer and not args.consumer:
       fail("--producer or --consumer are required")


def fail(message):
   print(message, file=sys.stderr)
   exit(1)
    
def runkafka():
#parsing the commandline arguments   
    parser = argparse.ArgumentParser()
    parser.add_argument('--service-uri', help="Service URI in the form host:port",
                            required=True)
    parser.add_argument('--ca-path', help="Path to project CA certificate (obtained from Aiven Console, if in trial)",
                            required=True)
    parser.add_argument('--key-path', help="Path to the Kafka Access Key (obtained from Aiven Console)",
                            required=True)
    parser.add_argument('--cert-path', help="Path to the Kafka Certificate Key (obtained from Aiven Console)",
                            required=True)
    parser.add_argument('--producer', action='store_true', default=False, help="Run Kafka producer simulator")
    parser.add_argument('--consumer', action='store_true', default=False, help="Run Kafka consumer simulator")

    args = parser.parse_args()
    validate_args(args)

    kwargs = {k: v for k, v in vars(args).items() if k not in ("producer", "consumer")}
    if args.producer:
        KapsProducerSanDiego(**kwargs)
        KapsProducerSanJose(**kwargs)
    elif args.consumer:
        KapsConsumerWeb(**kwargs)
        KapsConsumerMobile(**kwargs)
   
if __name__ == '__main__':
    runkafka()

    
# # ca_path = getattr(args, "ca_path")
# # cert_path = getattr(args, "cert_path")
# # key_path = getattr(args, "key_path")
# # service_uri = getattr(args, "service_uri")

# # #configuration object for pykafka connection. Refer Aiven Console for these immutable access files per account 
# # config = SslConfig(cafile=ca_path,certfile=cert_path,keyfile=key_path)   

# # #creating kafka client with Aiven kafka uri
# # client = KafkaClient(hosts=service_uri,ssl_config=config);
# # #print(client.topics);


# # #creating a topic named KapsTopic
# # topic = client.topics[b"KapsTopic"]

# # print ("~~~~~~~~~~~~~~~Producer SD Started~~~~~~~~~~~~~~~~");

# # #random search string collection
# # Search_keywords = ['Floyd','Mail in','Trump', 'Covid', 'Matrix 4', 'China', 'Oxford', 'Reopening']

# # #creating a synchronus producer by pykafka library.
# # with topic.get_sync_producer() as producer:
     # # for i in range(5):
	 # # #generating 5 rows of randomized data with San Diego as tag
         # # msg = str(uuid.uuid4()).encode() + str("|").encode() \
         # # + b'WebPage' +  str(random.randint(1,20)).encode() \
         # # + str("|").encode()+str(random.randint(600,1200)).encode() \
         # # + str("|").encode() +str(random.choice(Search_keywords)).encode() \
         # # + str("|").encode() +str(datetime.datetime.now()).encode() \
         # # + str("|").encode() +b'San Diego'
         # # print(msg)
         # # producer.produce(msg)
# # print ("~~~~~~~~~~~~~~~Producer SD Finished~~~~~~~~~~~~~~~~");
