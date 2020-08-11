# codeshare
The project would demo Aiven kafka elements deployment using standard python libraries to populate postgresql with browser stats from the wild. 

Console Applications are created for producing and consuming the data streams.

The consumers are simulated to be in San Diego and San Jose and source of generation is either Mobile App or Web App. A single topic is serving every traffic here. Both the producer and consumer are adding their own tags to identify the source and destination of the data.

Kafka Producer(2):
Will generate arbitrary data for website visits and most searched phrases. Python Random function will be used here.
Will write a comma separated data string in the topic for website statistics sample data generated above
Five rows of randomized data will be created per invocation. To end do a Ctrl-Z on command prompt
There are two producer sources. One has San Diego and another has San Jose marked for easy identification

Kafka Consumer(2):
Will pick only fresh additions to topic
Will create a PGSQL compatible insert statement
Will insert the record
Will poll for more additions to topic. To end do a Ctrl-Z on command prompt
There are two consuming end points. One has Mobile and another has Web marked for easy identification

CellPhoneWebSearches(1):
This is a postgreSQL table connected to MobileConsumer.

DesktopWebSearches(1):
This is a postgreSQL table connected to DesktopConsumer.

KapsTopic(1):
This is a single topic both the consumers are consuming from and producers are writing to.
