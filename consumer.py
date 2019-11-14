from absl import app
from absl import flags
from astropy.io import fits
from kafka import KafkaConsumer
from kafka import KafkaClient
from PIL import Image

import gzip
import fastavro
import io
import logging
import numpy as np

FLAGS = flags.FLAGS

flags.DEFINE_string('topic', 'test', 'Kafka Topic')
flags.DEFINE_list('host', 'localhost:9092', 'Kafka broker host.')
flags.DEFINE_string('project', 'kafka-to-bigquery', 'Current Project.')
flags.DEFINE_string('bucket', 'ztf_20191031', 'Destination Bucket.')
flags.DEFINE_string('destination_folder', 'images', 'Destination Folder Name.')


# Borrowed from Will Henney : https://github.com/will-henney/fits2image
# Some Modifications: don't allow max and min to be passed. And pass the file name.

def fits_to_png(data, filename):

    # Clip data to min max brightness limits
    vmin = data.min()
    vmax = data.max()
    data = (data - vmin)/(vmax - vmin)

    # Convert to 8-bit integer  
    data = (255*data).astype(np.uint8)

    # Invert y axis -- JRT -- not sure why
    data = data[::-1, :]

    # Create image from data array and save as jpg
    image = Image.fromarray(data, 'L')
    image.save(filename, format='png')


def read_avro(file_as_string):
    file_stream = io.BytesIO(file_as_string)
    freader = fastavro.reader(file_stream)
    for packet in freader:
        print(packet['publisher'])
        objectId = packet['objectId']
        print(packet['objectId'])
        print(packet['candidate'])
        print(packet['cutoutScience'].keys())
        data = packet['cutoutScience']['stampData']
        with gzip.open(io.BytesIO(data), 'rb') as f:
            with fits.open(io.BytesIO(f.read())) as hdul:
                fits_to_png(hdul[0].data, objectId + '.png')


def iterate_consumer():
    consumer = KafkaConsumer(
                    FLAGS.topic,
                    bootstrap_servers=FLAGS.host,
                    fetch_max_bytes=1000000,
                    auto_offset_reset='earliest',
                    consumer_timeout_ms=10000
            )

    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.key))
        print(read_avro(message.value))


def main(_):

   iterate_consumer()

if __name__ == '__main__':
    app.run(main)
