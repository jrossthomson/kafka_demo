from kafka import KafkaConsumer
consumer = KafkaConsumer('sample', bootstrap_servers='localhost:9092',
        api_version=(0, 10, 2))

for message in consumer:
    print (message)
consumer.close()
