#invocation:py runkafka.py --key-path="./service.key" --cert-path="./service.cert" --ca-path="./ca.pem" --db-cred="avnadmin:mycaz65d9c99lcdc@" --testrig
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
   elif not args.producer and not args.consumer and not args.testrig:
       fail("--producer or --consumer are required")


def fail(message):
   print(message, file=sys.stderr)
   exit(1)
    
def runkafka():
#parsing the commandline arguments   
    parser = argparse.ArgumentParser()

    parser.add_argument('--ca-path', help="Path to project CA certificate (obtained from Aiven Console, if in trial)",
                            required=True)
    parser.add_argument('--key-path', help="Path to the Kafka Access Key (obtained from Aiven Console)",
                            required=True)
    parser.add_argument('--cert-path', help="Path to the Kafka Certificate Key (obtained from Aiven Console)",
                            required=True)
    parser.add_argument('--db-cred', required=True, help="Enter DB credential string here")
    parser.add_argument('--producer', action='store_true', default=False, help="Run Kafka producer simulator")
    parser.add_argument('--consumer', action='store_true', default=False, help="Run Kafka consumer simulator")
    parser.add_argument('--testrig', action='store_true', default=False, help="Run Kafka Test Rig, calls both consumer/producer")
   

    args = parser.parse_args()
    validate_args(args)

    
    kwargs = {k: v for k, v in vars(args).items() if k not in ("producer", "consumer","testrig")}
    if args.producer:
        KapsProducerSanDiego(**kwargs)
        KapsProducerSanJose(**kwargs)
    elif args.consumer:
        KapsConsumerWeb(**kwargs)
        KapsConsumerMobile(**kwargs)
    elif args.testrig:
        from TestKafkatoDBStream import TestKafkatoDBStream
        TestKafkatoDBStream(**kwargs)

   
if __name__ == '__main__':
    runkafka()

