 Pipeline from Kafka to BigQuery Tutorial
## Table of Contents

<!-- No converter for: TABLE_OF_CONTENTS -->
_--_

This tutorial describes how to construct a pipeline from a Kafka producer to 
load generic messages into BigQuery. In it you will set up a Kafka cluster, 
create a simple Kafka Producer, build a Dataflow pipeline to receive Kafka 
messages using the Kafka Connector and stream those messages into a BigQuery 
table.

# Objectives 

* Build a Kafka Cluster
* Create code to push Produce Kafka message
* Build a Dataflow Pipeline to Consume messages
* Push the consumed messages into BigQuery

----

# Costs

This tutorial uses billable components of Google Cloud Platform, including:

* Compute Engine
* Dataflow
* BigQuery

Use the [Pricing Calculator](https://cloud.google.com/products/calculator) to 
generate a cost estimate based on your projected usage.  
-----

# Before you begin

1. Select or create a GCP project.

[GO TO THE MANAGE RESOURCES 
](https://console.cloud.google.com/cloud-resource-manager)[PAGE](https://console.cloud.google.com/cloud-resource-manager)

1. Enable billing for your project.

[ENABLE BILLING](https://support.google.com/cloud/answer/6293499#enable-billing)

1. Create a service account to run the af

When you finish this tutorial, you can avoid continued billing by deleting the 
resources you created. See [Cleaning up](#heading=h.mlrdlgcohh7k) for more 
detail.

---

# Create a Kafka Cluster

This section creates a Kafka cluster to produce messages

1. Open Cloud Shell
1. Create directory kafka2bigquery
1. Change directory to kafka2bigquery
1. Click on Cloud Shell Editor
1. Create a file defining your project configuration. Call it vars.sh
1. Edit these values to match your own, cut and paste into Cloud Shell window

> \# &lt;var&gt;project-id&lt;/var&gt; is the id of your project  
> export PROJECTID='&lt;var&gt;project-id&lt;/var&gt;'  
> \# &lt;var&gt;service-account&lt;/var&gt; is the service account you created 
> in the setup  
> export SERVICE\_ACCOUNT='&lt;var&gt;service-account&lt;/var&gt;'  
> \# &lt;var&gt;zone&lt;/var&gt; is the zone where you will run the VM  
> export ZONE='&lt;var&gt;zone&lt;/var&gt;'

1. Run the following to create a VM for the Kafka cluster

gcloud compute --project=$PROJECTID instances create kafka-instance-1 
--zone=$ZONE --machine-type=n1-standard-1 --subnet=default 
--network-tier=PREMIUM --maintenance-policy=MIGRATE 
--service-account=$SERVICE\_ACCOUNT 
--scopes=https://www.googleapis.com/auth/devstorage.read\_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append 
--image=debian-9-drawfork-v20190611 --image-project=eip-images 
--boot-disk-size=100GB --boot-disk-type=pd-standard 
--boot-disk-device-name=instance-1

[https://www.apache.org/dyn/closer.cgi?path=/kafka](https://www.apache.org/dyn/closer.cgi?path=/kafka)  
Download the latest bin archive for example  
_wget https://www-us.apache.org/dist/kafka/2.3.1/kafka\_2.12-2.3.1.tgz_  
[https://www.apache.org/dyn/closer.cgi/zookeeper/](https://www.apache.org/dyn/closer.cgi/zookeeper/)  
Download the latest bin archive, for example:  
wget 
https://www-us.apache.org/dist/zookeeper/stable/apache-zookeeper-3.5.6-bin.tar.gz  
sudo apt-get -y install default-jdk

Unarchive

_tar xvf kafka\_2.12-2.3.1.tgz_  
_tar xvf apache-zookeeper-3.5.6-bin.tar.gz_

cd kafka\_2.12-2.2.0

# Create a BigQuery Table

This section creates a BigQuery table to store the Kafka messages.

1. Open Cloud Shell
1. Create a dataset
1. Create a table with name value columns

## Setup environment

sudo apt-get install python3-venv

wget https://ztf.uw.edu/alerts/public/ztf\_public\_20191031.tar.gz  
git clone https://github.com/ZwickyTransientFacility/ztf-avro-alert.git  
virtualenv ztf-avro-alert/

# Create the Dataflow Pipeline

There are multiple ways to create a Dataflow pipeline. Here we are considering 
two.

## Template approach

There is an existing template to use the   
Setup Kafka

Quick Start

Kafka  
Go to 
https://www.apache.org/dyn/closer.cgi?path=/kafka/2.2.0/kafka\_2.12-2.2.0.tgz  
Find link to download  
wget [download link]

Zookeeper  
Go to https://zookeeper.apache.org/ find link  
Wget [download link]

sudo apt-get -y install default-jdk  
&gt; tar -xzf kafka\_2.12-2.2.0.tgz  
&gt; cd kafka\_2.12-2.2.0

Start Zookeeper  
bin/zookeeper-server-start.sh config/zookeeper.properties &

Start the Kafka server:  
 bin/kafka-server-start.sh config/server.properties &

Create Topic  
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 
--replication-factor 1 --partitions 1 --topic test  
List Topic  
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

Producer / Consumer

Producer  
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test  
&gt;This is a simple message  
&gt;Take it to the floor

Consumer  
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test 
--from-beginning

Different machine  
bin/kafka-console-producer.sh --broker-list instance-1:9092 --topic test

Kafka to BigQuery Dataflow  
sudo apt-get install git  
git clone https://github.com/GoogleCloudPlatform/DataflowTemplates.git  
cd DataflowTemplates/  
sudo apt-get install maven

mvn compile exec:java \  
-Dexec.mainClass=com.google.cloud.teleport.templates.KafkaToBigQuery \  
-Dexec.cleanupDaemonThreads=false \  
-Dexec.args=" \  
--project=community-broker \  
--stagingLocation=gs://community-broker/staging \  
--tempLocation=gs://community-broker/temp \  
--templateLocation=gs://community-broker/templates/KafkaToBigQuery.json \  
--runner=DataflowRunner"

V2 no UDF  
export BUCKET\_NAME=gs://community-broker  
export PROJECT\_ID=community-broker  
export PIPELINE\_FOLDER=${BUCKET\_NAME}  
export JOB\_NAME=kafka-to-bigquery-jrossthomson-\`date +"%Y%m%d-%H%M"\`  
export MY\_HOST=10.128.0.2  
export MY\_TOPIC=test

gcloud dataflow jobs run ${JOB\_NAME} \  
--gcs-location=${PIPELINE\_FOLDER}/templates/KafkaToBigQuery.json \  
--zone=us-east1-d \  
--parameters \  
"bootstrapServers=${MY\_HOST}:9092,inputTopic=${MY\_TOPIC},\  
outputTableSpec=community-broker:kafka.kafka\_to\_bigquery,\  
outputDeadletterTable=community-broker:kafka.kafka\_to\_bigquery\_deadletter"

SImple Producer

Run  
java -cp "libs/\*":. SimpleProducer test  
Build  
javac -cp "libs/\*" SimpleProducer.java 

Code

//import util.properties packages  
import java.util.Properties;

//import simple producer packages  
import org.apache.kafka.clients.producer.Producer;

//import KafkaProducer packages  
import org.apache.kafka.clients.producer.KafkaProducer;

//import ProducerRecord packages  
import org.apache.kafka.clients.producer.ProducerRecord;

//Create java class named "SimpleProducer"  
public class SimpleProducer {  
     
   public static void main(String[] args) throws Exception{  
        
      // Check arguments length value  
      if(args.length == 0){  
         System.out.println("Enter topic name");  
         return;  
      }  
        
      //Assign topicName to string variable  
      String topicName = args[0].toString();  
        
      // create instance for properties to access producer configs     
      Properties props = new Properties();  
        
      //Assign localhost id  
      props.put("bootstrap.servers", "localhost:9092");  
        
      //Set acknowledgements for producer requests.        
      props.put("acks", "all");  
        
      //If the request fails, the producer can automatically retry,  
      props.put("retries", 0);  
        
      //Specify buffer size in config  
      props.put("batch.size", 16384);  
        
      //Reduce the no of requests less than 0     
      props.put("linger.ms", 1);  
        
      //The buffer.memory controls the total amount of memory available to the 
producer for buffering.     
      props.put("buffer.memory", 33554432);  
        
      props.put("key.serializer",   
         "org.apache.kafka.common.serialization.StringSerializer");  
           
      props.put("value.serializer",   
         "org.apache.kafka.common.serialization.StringSerializer");  
        
      Producer&lt;String, String&gt; producer = new KafkaProducer  
         &lt;String, String&gt;(props);  
              
      for(int i = 0; i &lt; 10; i++)  
         producer.send(new ProducerRecord&lt;String, String&gt;(topicName,   
           // Integer.toString(i), "this ist list" + Integer.toString(i)));  
            Integer.toString(i), "{\"name\": \""  + Integer.toString(i) + " \", 
\"value\": \"" + Integer.toString(i) + "\"}"

                    )) ;  
               System.out.println("Message sent successfully");  
               producer.close();  
   }  
}

Add library  
http://www.java2s.com/Code/Jar/o/Downloadorgapachecommonsiojar.htm

Wget 
http://www.java2s.com/Code/JarDownload/org.apache.commons/org.apache.commons.io.jar.zip

Image Producer

Run  
java -cp "libs/\*":. ImageProducer test

Build  
javac -cp "libs/\*" ImageProducer.java 

Code

import java.util.Properties;

import java.io.File;  
import java.io.IOException;  
import java.nio.file.\*;  
import java.util.Base64;  
import org.apache.commons.io.FileUtils;

//import simple producer packages  
import org.apache.kafka.clients.producer.Producer;

//import KafkaProducer packages  
import org.apache.kafka.clients.producer.KafkaProducer;

//import ProducerRecord packages  
import org.apache.kafka.clients.producer.ProducerRecord;

//Create java class named "SimpleProducer"  
public class ImageProducer {  
     
   public static String readFileEncodetoBase64(String filePath) throws 
IOException  
   {  
      File f = new File(filePath);  
      byte[] fileContent = FileUtils.readFileToByteArray(f);

      String encodedString = Base64.getEncoder().encodeToString(fileContent);  
      return(encodedString);  
   }

   public static void main(String[] args) throws Exception{  
        
      // Check arguments length value  
      if(args.length == 0){  
         System.out.println("Enter topic name");  
         return;  
      }  
        
      //Assign topicName to string variable  
      String topicName = args[0].toString();  
        
      // create instance for properties to access producer configs     
      Properties props = new Properties();  
        
      //Assign localhost id  
      props.put("bootstrap.servers", "localhost:9092");  
        
      //Set acknowledgements for producer requests.        
      props.put("acks", "all");  
        
      //If the request fails, the producer can automatically retry,  
      props.put("retries", 0);  
        
      //Specify buffer size in config  
      props.put("batch.size", 16384);  
        
      //Reduce the no of requests less than 0     
      props.put("linger.ms", 1);  
        
      //The buffer.memory controls the total amount of memory available to the 
producer for buffering.     
      props.put("buffer.memory", 33554432);  
        
      props.put("key.serializer",   
         "org.apache.kafka.common.serialization.StringSerializer");  
           
      props.put("value.serializer",   
         "org.apache.kafka.common.serialization.StringSerializer");  
        
      Producer&lt;String, String&gt; producer = new KafkaProducer  
         &lt;String, String&gt;(props);

      String imageString = readFileEncodetoBase64("file.png");  
              
      for(int i = 0; i &lt; 10000; i++)  
         producer.send(new ProducerRecord&lt;String, String&gt;(topicName,   
           // Integer.toString(i), "this ist list" + Integer.toString(i)));  
            Integer.toString(i), "{\"name\": \""  + Integer.toString(i) + " \", 
\"value\": \"" + imageString + "\"}"

                    )) ;  
               System.out.println("Message sent successfully");  
               producer.close();  
   }  
}

Decode Base64

 cat raw.txt | base64 --decode &gt; google.png

UDFs

/\*\*  
 \* A transform function which only accepts 42 as the answer to life.  
 \* @param {string} inJson  
 \* @return {string} outJson  
 \*/  
function transform(inJson) {  
  var obj = JSON.parse(inJson);  
  // only output objects which have an answer to life of 42.  
  if (obj.hasOwnProperty('answerToLife') && obj.answerToLife === 42) {  
    return JSON.stringify(obj);  
  }  
}

Sent message:   
{ "name": 'abc', "value": 'cde' 

Getting errors:

java.lang.IllegalArgumentException: Unable to encode element 
'FailsafeElement{originalPayload=KV{null, { "name": 'abc', "value": 'cde' }}, 
payload={ "name": 'abc', "value": 'cde' }, errorMessage=null, stacktrace=null}' 
with coder 'com.google.cloud.teleport.coders.FailsafeElementCoder@46e5696e'.  
        
org.apache.beam.sdk.coders.Coder.getEncodedElementByteSize(Coder.java:300)

Topics  
Delete Topic  
bin/kafka-topics.sh  --bootstrap-server localhost:9092 --topic kafka-test --  
delete

Create  
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 
--replication-factor 1 --partitions 1 --topic kafka-test

Consume

bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test 
--from-beginning  
bin/kafka-console-consumer.sh --bootstrap-server 10.128.0.2:9092 --topic 
kafka-test --from-beginning

Java  
Simple Java Producer

javac -cp "libs/\*" SimpleProducer.java 

Python

Code https://pypi.org/project/kafka-python/

from kafka import KafkaConsumer  
consumer = KafkaConsumer('kafka-test', bootstrap\_servers='localhost:9092')  
for msg in consumer:  
  print (msg)

from kafka import KafkaProducer  
producer = KafkaProducer(bootstrap\_servers='localhost:9092')  
for \_ in range(100):  
  producer.send('kafka-test', b'some\_message\_bytes')

## Cleaning up

_[The cleaning up section is required. Use it to ensure they don't get billed 
for any extra time.]_  
To avoid incurring charges to your Google Cloud Platform account for the 
resources used in this tutorial:

### Delete the project

The easiest way to eliminate billing is to delete the project you created for 
the tutorial.  
To delete the project:

1. In the Cloud Platform Console, go to the Projects page.

> [GO TO THE PROJECTS PAGE](https://console.cloud.google.com/iam-admin/projects)

1. In the project list, select the project you want to delete and click 
   **Delete**.
1. <img src="image00.png" width="624" height="156" />
1. In the dialog, type the project ID, and then click **Shut down** to delete 
   the project.

----

## What's next

_[The What's Next section is required. Use it to list links to the following 
types of content:_

* _Related__ tutorials they might be interested in._
* _Conceptual articles or reference docs._

_All tutorials must include the following bullet in the What's Next section.]_

* Try out other Google Cloud Platform features for yourself. Have a look at our 
  [tutorials](https://cloud.google.com/docs/tutorials).
