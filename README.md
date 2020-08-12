# codeshare
<h2>PyKafka Example</h2>
This example uses the pyKafka library to interact with Kafka both as a producer of messages and a consumer.

<h3>Installing Dependencies</h3>
        pip install PyKafka
   <br/>pip install psycopg2

   <br/>The binaries for these is included in the bin folder if your environment can't access them.
<h3>Running The Example</h3>
Go to Aiven Console at to create the kafka service. Use all the defaults, unless you have a need to tweak them. The service will take few minutes to statt running.<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig10.jpg"></img>
You can find the connection details in the "Overview" tab in the Aiven Console for the application we are installing. The service URI generated are usually in the format xxxxx-yyyyy-dd99.aivencloud.com:nnnnn

<h4>Topic Creation:</h4>
Use the Aiven Client to create a topic in your Kafka cluster (named KapsTopic here)
 <br/>avn service topic-create <kafka-service-name>  KapsTopic --partitions 3 --replication 1
 <br/> Alternatively you can use Aiven Console to do the same <img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig9.jpg"></img>
<h4>Produce some messages:</h4>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --service-uri="xxxxx-yyyyy-dd99.aivencloud.com:nnnnn" --producer
  <br/>Download serice.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the path appropriately. Replace the appropriate URI in the service uri parameter too.
<h4>Consume some messages:</h4>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --service-uri="xxxxx-yyyyy-dd99.aivencloud.com:nnnnn" --consumer
   <br/>Download serice.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the path appropriately. Replace the appropriate URI in the service uri parameter too.
<h4>Test some messages:</h4>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --service-uri="xxxxx-yyyyy-dd99.aivencloud.com:nnnnn" --testrig
   <br/>Download serice.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the above path appropriately. Replace the appropriate URI in the service uri parameter too.
   <h4>Database integration:</h4> Subscribe for PostgreSQL at Aivent console. This will generate a connection endpoint (ServiceURI) to be used for database crud operations in the defaultdb database. Leave most of the setting parameters for the exercise as default. You should also install some client like PGAdmin 4 to visualize the database query results. <img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig11.jpg"></img>
  <hr/>
  <h2>Component Details</h2>
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
 <br/>This is a postgreSQL table connected to MobileConsumer created in defaultdb public schema

<h3>DesktopWebSearches(1): </h3>
 <br/>This is a postgreSQL table connected to DesktopConsumer created in defaultdb public schema
<h3>crtWebSearches(1): </h3>
 <br/>This is a postgreSQL stored procedure invoked by consumers.

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
