export BUCKET_NAME=gs://kafka-to-bigquery
export PROJECT_ID=kafka-to-bigquery
export PIPELINE_FOLDER=${BUCKET_NAME}
export JOB_NAME=kafka-to-bigquery-jrossthomson-`date +"%Y%m%d-%H%M"`
export MY_HOST=10.128.0.12
export MY_TOPIC=test

gcloud dataflow jobs run ${JOB_NAME} \
	--gcs-location=${PIPELINE_FOLDER}/templates/KafkaToBigQuery.json \
	--zone=us-central1-b \
	--parameters \
"bootstrapServers=${MY_HOST}:9092,inputTopic=${MY_TOPIC},\
outputTableSpec=kafka_demo.demodata,runner=DirectRunner,\
outputDeadletterTable=kafka_demo.kafka_to_bigquery_deadletter"

