#!/usr/bin/env python

"""

"""
from absl import app
from absl import flags
from google.cloud import storage
from kafka import KafkaProducer

import fastavro
import json
import os
import io

FLAGS = flags.FLAGS

flags.DEFINE_list('input', '', 'Files to load, comma separated.')
flags.DEFINE_integer('blob_limit', 10, 'Max number of blobs to process. -1 means all.')
flags.DEFINE_string('project', 'kafka-to-bigquery', 'Current Project.')
flags.DEFINE_string('bucket', 'ztf_20191031', 'Source Bucket.')
flags.DEFINE_string('source_blob_name',
                    '1033112310015010003.avro', 'Source File/Object Name.')
flags.DEFINE_string('destination_file_name',
                    '1033112310015010003.avro', 'Destination File Name.')
flags.DEFINE_string('source_folder', 'data', 'Source Folder Name.')
flags.DEFINE_string('topic', 'test', 'Kafka Topic')
flags.DEFINE_list('host', 'localhost:9092', 'Kafka Broker Hosts')

# alert_fields = 'objectId,jd,fid,pid,diffmaglim,pdiffimfilename,programpi,programid,candid,isdiffpos,tblid,nid,rcid,field,xpos,ypos,\
# ra,dec,magpsf,sigmapsf,chipsf,magap,sigmagap,distnr,magnr,sigmagnr,chinr,sharpnr,sky,magdiff,\
# fwhm,classtar,mindtoedge,magfromlim,seeratio,aimage,bimage,aimagerat,bimagerat,elong,nneg,nbad,rb,ssdistnr,\
# ssmagnr,ssnamenr,sumrat,magapbig,sigmagapbig,ranr,decnr,sgmag1,srmag1,simag1,szmag1,sgscore1,distpsnr1,ndethist,ncovhist,\
# jdstarthist,jdendhist,scorr,tooflag,objectidps1,objectidps2,sgmag2,srmag2,simag2,szmag2,sgscore2,distpsnr2,objectidps3,sgmag3,\
# srmag3,simag3,szmag3,sgscore3,distpsnr3,nmtchps,rfid,jdstartref,jdendref,nframesref'


def produce_message(topic, key, message):
    producer = KafkaProducer(bootstrap_servers=FLAGS.host)
    producer.send(topic, key=key, value=message)
    producer.close()


def get_blob_list(bucket_name, project):
    storage_client = storage.Client(project=project)
    blobs = storage_client.list_blobs(bucket_name)
    return(blobs)


def get_blob_as_string(bucket_name, source_folder, source_blob_name, destination_file_name, project):

    storage_client = storage.Client(project=project)
    bucket = storage_client.get_bucket(bucket_name)
    source_name = os.path.join(source_folder, source_blob_name)
    blob = bucket.blob(source_name)
    return(blob.download_as_string())


def read_avro(file_as_string):
    file_stream = io.BytesIO(file_as_string)
    freader = fastavro.reader(file_stream)
    # schema = freader.schema
    # print(schema)
    for packet in freader:
        print(packet.keys())
        print(packet['publisher'])
        print(packet['objectId'])
    # print(json.dumps(packet['candidate']))
    # print(json.dumps(packet['prv_candidates']))
    # print(json.dumps(packet['candid']))
    #    print(packet['cutoutScience']['stampData'])
    # print(json.dumps(packet['cutoutScience']))
    # print(json.dumps(packet['cutoutTemplate']))
    # print(json.dumps(packet['cutoutDifference']))
        # print(packet['prv_candidates'])


def main(_):
    if len(FLAGS.input) > 0:
        for filename in FLAGS.input:
            blob_string = get_blob_as_string(
                  FLAGS.bucket, FLAGS.source_folder, filename, filename, FLAGS.project)
            read_avro(blob_string)

        exit()

    blob_list = get_blob_list(FLAGS.bucket, FLAGS.project)
    count_down = FLAGS.blob_limit
    for b in blob_list:
        if count_down == 0:
            exit()
        else:
            count_down -= 1
        head_tail = os.path.split(b.name)
        print(head_tail[1])
        blob_string = get_blob_as_string(
            FLAGS.bucket, head_tail[0], head_tail[1], head_tail[1], FLAGS.project)
        read_avro(blob_string)
        produce_message(FLAGS.topic, b.name.encode(),  blob_string)


if __name__ == '__main__':
    app.run(main)
