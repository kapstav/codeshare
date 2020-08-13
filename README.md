# codeshare
<h2>PyKafka Example</h2>
This example uses the pyKafka library to interact with Kafka both as a producer of messages and a consumer.

<h3>Subscribing to Kafka Service</h3>
Go to Aiven Console at to create the kafka service. Use all the defaults, unless you have a need to tweak them. The service will take few minutes to start running.<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig10.jpg"></img>
You can find the connection details in the "Overview" tab in the Aiven Console for the application we are installing. The service URI generated are usually in the format xxxxx-yyyyy-dd99.aivencloud.com:nnnnn

<h4>Topic Creation:</h4>
Use the Aiven Client to create a topic in your Kafka cluster (named KapsTopic here, can be changed) <img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig9.jpg"></img>
<h3> Sourcecode download </h3> Download the zip from https://github.com/kapstav/codeshare.git 
Extract every *.py files (viz., KapsConsumerMobile.py, KapsConsumerWeb.py, KapsProducerSanDiego.py, KapsProducerSanJose.py, TestKafkatoDBStream.py & runkafka.py) in a base local windows directory, together with config.ini. Download secrets file (service.key,service.cert & ca.pem) and save them in the directory of your choice from Aiven Console. Note the path where you download these files as the links for run time read needs to be provided later.
<h3>Installing Dependencies</h3>
Make sure you have downloaded the following binaries in the base local windows directory using pip. You might have to preinstall npm, pip and python too. Refer to these product webpages if you need pip & python pre installed before going to next step.

   <br/>pip install PyKafka
   <br/>pip install psycopg2

   <br/>The binaries for these is included in the bin folder if your environment can't access them.
   <h4>Database integration:</h4> Subscribe for PostgreSQL at Aivent console. This will generate a connection endpoint (ServiceURI) to be used for database crud operations in the defaultdb database. Leave most of the setting parameters for the exercise as default. You should also install some client like PGAdmin 4 to visualize the database query results. <img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig11.jpg"></img>
   <br/> Run the following command in a fresh PostgreSQL window which has defaultdb created in public schema using any client of your choice, seek help of a db developer if in confusion.
   <pre>
   -- Table: public.CellPhoneWebSearches

-- DROP TABLE public."CellPhoneWebSearches";

CREATE TABLE public."CellPhoneWebSearches"
(
    "GUID" uuid,
    "WEBPAGEID" character varying(24) COLLATE pg_catalog."default",
    "TOTALHITS" bigint,
    "MOSTSEARCHED" character varying(16) COLLATE pg_catalog."default",
    "CRTDT" timestamp without time zone,
    "SRCREGION" character varying(16) COLLATE pg_catalog."default",
    "CONSUMER" character varying(16) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public."CellPhoneWebSearches"
    OWNER to avnadmin;

COMMENT ON TABLE public."CellPhoneWebSearches"
    IS 'GUID, WEBPAGEID, TOTALHITS, MOSTSEARCHED,CRTDT';

COMMENT ON COLUMN public."CellPhoneWebSearches"."SRCREGION"
    IS 'Source Region';
	
;
	
	
-- Table: public.DesktopWebSearches

-- DROP TABLE public."DesktopWebSearches";

CREATE TABLE public."DesktopWebSearches"
(
    "GUID" uuid,
    "WEBPAGEID" character varying(24) COLLATE pg_catalog."default",
    "TOTALHITS" bigint,
    "MOSTSEARCHED" character varying(16) COLLATE pg_catalog."default",
    "CRTDT" timestamp without time zone,
    "SRCREGION" character varying(16) COLLATE pg_catalog."default",
    "CONSUMER" character varying(16) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public."DesktopWebSearches"
    OWNER to avnadmin;

COMMENT ON TABLE public."DesktopWebSearches"
    IS 'GUID, WEBPAGEID, TOTALHITS, MOSTSEARCHED,CRTDT';

COMMENT ON COLUMN public."DesktopWebSearches"."SRCREGION"
    IS 'Source Region';


;

create or replace procedure crtWebSearches(xGUID varchar(24),xWEBPAGEID varchar(16), xTOTALHITS varchar(4), xMOSTSEARCHED varchar(16)
,xCRTDT varchar(24),xSRCREGION varchar(16), xCONSUMER varchar(16))
language plpgsql
as $$
declare
begin
	IF xCONSUMER ='Web' THEN
	 IF NOT EXISTS (SELECT * FROM "DesktopWebSearches" WHERE "GUID" = UUID(xGUID)) THEN
			INSERT INTO "DesktopWebSearches"("GUID","WEBPAGEID","TOTALHITS","MOSTSEARCHED","CRTDT","SRCREGION","CONSUMER")
			VALUES(UUID(xGUID),xWEBPAGEID, CAST(xTOTALHITS as bigint), xMOSTSEARCHED,CAST(xCRTDT as timestamp),xSRCREGION, xCONSUMER);
     END IF;
	ELSE
	 IF NOT EXISTS (SELECT * FROM "CellPhoneWebSearches" WHERE "GUID" = UUID(xGUID)) THEN
			INSERT INTO "CellPhoneWebSearches"("GUID","WEBPAGEID","TOTALHITS","MOSTSEARCHED","CRTDT","SRCREGION","CONSUMER")
			VALUES(UUID(xGUID),xWEBPAGEID, CAST(xTOTALHITS as bigint), xMOSTSEARCHED,CAST(xCRTDT as timestamp),xSRCREGION, xCONSUMER);
     END IF;

	END IF;
end; $$

;
create or replace procedure testWebSearches(xPATTERN varchar(16),INOUT val varchar(16) DEFAULT null)
language plpgsql
as $$
declare
val1 int=0;
val2 int=0;
begin
--Querying the number of fresh record created in the database should be 20. (5/producer X 2producer X 2consumer)
select count(*) INTO val1 from public."CellPhoneWebSearches" Where "MOSTSEARCHED" IN(xPATTERN); 
select count(*) INTO val2  from public."DesktopWebSearches" Where "MOSTSEARCHED" IN(xPATTERN);
val= val1+val2;

--deleting records for next test session for this pattern
delete from public."CellPhoneWebSearches" Where "MOSTSEARCHED" IN(xPATTERN);
delete from public."DesktopWebSearches" Where "MOSTSEARCHED" IN(xPATTERN);
end; $$
;
</pre>
<h4>Setup Config.ini:</h4>
The kafka & pgsql endpoints, topic name and sample seed data are set in config.ini. Open it and update appropriately with your subscriptions gotten from Aiven Console.

<h4>Produce some messages:</h4>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --producer
  <br/>Download service.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the path appropriately. Replace the appropriate URI in the service uri parameter too.
<h4>Consume some messages:</h4>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --consumer
   <br/>Download service.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the path appropriately. Replace the appropriate URI in the service uri parameter too.
<h4>Test some messages:</h4>
py runkafka.py --key-path="./home/service.key" --cert-path="./home/service.cert" --ca-path="./home/ca.pem" --testrig
   <br/>Download service.key, service.cert and ca.pem in local drives from Aiven Console on server (say ./home/) and change the above path appropriately. Replace the appropriate URI in the service uri parameter too.


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

 

<h3>Screenshots:</h3>
<h4>Sample Producer run</h4>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig1.jpg"></img>
<h4>Sample Consumer run</h4>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig3.jpg"></img>
<h4>Sample Testrig run</h4>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig41.jpg"></img>
<h4>Sample PostgreSQL Snapshot</h4>
<img src="https://raw.githubusercontent.com/kapstav/codeshare/master/img/fig5.jpg"></img>
 
