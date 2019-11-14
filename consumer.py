from absl import app
from absl import flags
from astropy.io import fits
from google.cloud import storage
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
flags.DEFINE_string('bucket', 'kafka-to-bigquery', 'Destination Bucket.')
flags.DEFINE_string('destination_folder', 'images', 'Destination Folder Name.')



class ZTFAvro:

    def __init__(self, packet):
        self.packet = packet

        self.objectId = packet['objectId']

        self.cutoutScience = self.stamp_avro_to_fits(packet['cutoutScience']['stampData'])
        self.cutoutTemplate = self.stamp_avro_to_fits(packet['cutoutTemplate']['stampData'])
        self.cutoutDifference = self.stamp_avro_to_fits(packet['cutoutDifference']['stampData'])

    def stamp_avro_to_fits(self, stamp_string):
            with gzip.open(io.BytesIO(stamp_string), 'rb') as f:
                with fits.open(io.BytesIO(f.read())) as hdul:
                    return(hdul[0].data)
    

    def store_avro_to_GCS(self):

        storage_client = storage.Client(project=FLAGS.project)
        bucket = storage_client.get_bucket(FLAGS.bucket)

        blob = bucket.blob(FLAGS.destination_folder + '/' + self.objectId + "_scie.png")
        blob.upload_from_string(self.fits_to_png(self.cutoutScience))
        blob = bucket.blob(FLAGS.destination_folder + '/' + self.objectId + "_temp.png")
        blob.upload_from_string(self.fits_to_png(self.cutoutTemplate))
        blob = bucket.blob(FLAGS.destination_folder + '/' + self.objectId + "_diff.png")
        blob.upload_from_string(self.fits_to_png(self.cutoutDifference))

       # f = open(self.objectId + "_scie.png", "wb")
       # f.write(self.fits_to_png(self.cutoutScience))
       # f = open(self.objectId + "_temp.png", "wb")
       # f.write(self.fits_to_png(self.cutoutTemplate))
       # f = open(self.objectId + "_diff.png", "wb")
       # f.write(self.fits_to_png(self.cutoutDifference))

    def fits_to_png(self, data):

        # Borrowed from Will Henney : https://github.com/will-henney/fits2image
        # Some Modifications: don't allow max and min to be passed. And pass the file name.

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
            with io.BytesIO() as output:
                image.save(output, format='png')
                return(output.getvalue())


class ZTFConsumer:

    def __init__(self):
        self.consumer = KafkaConsumer(
                FLAGS.topic,
                bootstrap_servers=FLAGS.host,
                fetch_max_bytes=1000000,
                auto_offset_reset='earliest',
                consumer_timeout_ms=1000
            )



    def read_avro_from_string(self, file_as_string):
        file_stream = io.BytesIO(file_as_string)
        freader = fastavro.reader(file_stream)

        for packet in freader:
            ztfa = ZTFAvro(packet)
            ztfa.store_avro_to_GCS()

    def iterate_consumer(self):

        for message in self.consumer:
            print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.key))
            self.read_avro_from_string(message.value)


def main(_):

    ztfconsumer = ZTFConsumer()
    ztfconsumer.iterate_consumer()

if __name__ == '__main__':
    app.run(main)
