mvn compile exec:java \
	-Dexec.mainClass=com.google.cloud.teleport.templates.KafkaToBigQuery \
	-Dexec.cleanupDaemonThreads=false \
	-Dexec.args=" \
--project=kafka-to-bigquery \
--stagingLocation=gs://kafka-to-bigquery/staging \
--tempLocation=gs://kafka-to-bigquery/temp \
--templateLocation=gs://kafka-to-bigquery/templates/KafkaToBigQuery.json \
--runner=DataflowRunner"

