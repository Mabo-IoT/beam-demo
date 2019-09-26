# from __future__ import absolute_import

import argparse
import logging
import re

from past.builtins import unicode

import json
import apache_beam as beam
from apache_beam import window
from apache_beam.io.external.kafka import ReadFromKafka
from apache_beam.io.external.kafka import WriteToKafka
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import WriteToText


class ParseTimestamp(beam.DoFn):

    def process(self, element):
        # Extract the numeric Unix seconds-since-epoch timestamp to be
        # associated with the current log entry.
        unix_timestamp = self.extract_timestamp(element)
        # Wrap and emit the current entry and new timestamp in a
        # TimestampedValue.
        yield beam.window.TimestampedValue(element, unix_timestamp)
    
    def extract_timestamp(self, element): 
        timestamp = element["Timestamp"]
        return timestamp


class ParseJson(beam.DoFn):
    def process(self, element):
        data = json.loads(element)
    
        yield data


def run(argv=None):
    """
    Main entry point; defines and runs the wordcount pipeline.
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',
                      dest='output',
                      required=True,
                      help='Output file to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_args.extend([
        "--runner=FlinkRunner",
        "--flink_master_url=localhost:8081", 
        # "--runner=DirectRunner",
        "--environment_type=LOOPBACK",
        "--experiments=beam_fn_api",

    ])

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    p = beam.Pipeline(options=pipeline_options)
    # 1. creat kafka message read io
    consumer_config: dict = {
        "bootstrap.servers": "192.168.0.110:9092",
        
    }
    topics: List[str] = ["test"]
    expansion_service = "localhost:8097",   # flink jobserver sevice

    message = (p
            |"ReadFromKafka"  >> ReadFromKafka(consumer_config,topics, expansion_service = "localhost:8097")
            |"ParseJson"      >> beam.ParDo(ParseJson())
            |"TimestampValue" >> beam.ParDo(ParseTimestamp())
            |"Windows"        >> beam.WindowInto((window.FixedWindows(60)))
    )
    # write into text
    message | 'write' >> WriteToText(known_args.output)

    result= p.run()
    result.wait_until_finish()

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
