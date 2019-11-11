from absl import app
from absl import flags
from kafka import KafkaConsumer
from kafka import KafkaClient

import io
import fastavro
import logging

FLAGS = flags.FLAGS

flags.DEFINE_string('topic', 'test', 'Kafka Topic')
flags.DEFINE_list('host', 'localhost:9092', 'Kafka broker host.')
flags.DEFINE_string('project', 'kafka-to-bigquery', 'Current Project.')
flags.DEFINE_string('bucket', 'ztf_20191031', 'Destination Bucket.')
flags.DEFINE_string('destination_folder', 'images', 'Destination Folder Name.')

def read_avro(file_as_string):
    file_stream = io.BytesIO(file_as_string)
    freader = fastavro.reader(file_stream)
    for packet in freader:
        print(packet['publisher'])
        print(packet['objectId'])


def main(_):
    consumer = KafkaConsumer(FLAGS.topic, bootstrap_servers=FLAGS.host, fetch_max_bytes=100000000, auto_offset_reset='earliest', enable_auto_commit=False)

    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.key))
        print(read_avro(message.value))

if __name__ == '__main__':
    app.run(main)
