# codeshare
<h3>PyKafka Example</h3>
This example uses the pyKafka library to interact with Kafka both as a producer of messages and a consumer.

<h3>Installing Dependencies</h3>
pip install PyKafka
<h3>Running The Example</h3>
Note: You can find the connection details in the "Overview" tab in the Aiven Console. 

<h3>Use the Aiven Client to create a topic in your Kafka cluster:</h3>
avn service topic-create <kafka-service-name>  KapsTopic --partitions 3 --replication 1
<h3>Produce some messages:</h3>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --service-uri="xxxxx-yyyyy-dd99.aivencloud.com:nnnnn" --producer
  <br/>Download serice.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the path appropriately.Replace the appropriate URI in the service uri parameter after querying Aiven console
<h3>Consume some messages:</h3>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --service-uri="xxxxx-yyyyy-dd99.aivencloud.com:nnnnn" --consumer
   <br/>Download serice.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the path appropriately.Replace the appropriate URI in the service uri parameter after querying Aiven console
<h3>Test some messages:</h3>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --service-uri="xxxxx-yyyyy-dd99.aivencloud.com:nnnnn" --testrig
   <br/>Download serice.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the above path appropriately. Replace the appropriate URI in the service uri parameter after querying Aiven console
  <hr/>
  <br/>The project would demo Aiven kafka elements deployment using standard python libraries to populate postgresql with browser stats from the wild. 

<br/>Windows Console Applications are created in this project for producing and consuming the data streams. Producer and consumer needs to be run concurrently or consumer can run later, the offset of last read is maintained. Both have to share the same topic.

<br/>The producers are simulated to be in San Diego and San Jose and consumers are attached to either Mobile App Group or Web App Group. A single topic is serving every traffic here although both the producer and consumer are adding their own tags to identify the source and destination for the dataset.

 <h3><br/>Kafka Producer(2): </h3>
 <br/>Will generate arbitrary data for website visits and most searched phrases. Python Random function will be used here.
 <br/>Will write a comma separated data string in the topic for website statistics sample data generated above
 <br/>Five rows of randomized data will be created per invocation. To end do a Ctrl-Z on command prompt
 <br/>There are two producer sources. One has San Diego and another has San Jose marked for easy identification

 <h3><br/>Kafka Consumer(2): </h3>
 <br/>Will pick only fresh additions to topic
 <br/>Will create a PGSQL compatible insert statement
 <br/>Will insert the record
 <br/>Will poll for more additions to topic. To end do a Ctrl-Z on command prompt
 <br/>There are two consuming end points. One has Mobile and another has Web marked for easy identification

<h3>CellPhoneWebSearches(1): </h3>
 <br/>This is a postgreSQL table connected to MobileConsumer.

<h3>DesktopWebSearches(1): </h3>
 <br/>This is a postgreSQL table connected to DesktopConsumer.
<h3>crtWebSearches(1): </h3>
 <br/>This is a postgreSQL stored procedure invoked my consumers.

<h3>KapsTopic(1): </h3>
 <br/>This is a single topic both the consumers are consuming from and producers are writing to.
<hr/>

<h3>Screenshots:</h3>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig1.jpg"></img>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig2.jpg"></img>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig3.jpg"></img>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig4.jpg"></img>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig5.jpg"></img>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig6.jpg"></img>
