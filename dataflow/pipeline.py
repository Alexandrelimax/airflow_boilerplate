import argparse
import csv
from csv import DictReader
from io import StringIO
from apache_beam.io import ReadFromText, WriteToBigQuery, BigQueryDisposition
from apache_beam import DoFn, ParDo, Pipeline
from apache_beam.options.pipeline_options import PipelineOptions


class UpperCaseNamesFn(DoFn):
    def process(self, element):
        try:
            reader = DictReader(StringIO(element), fieldnames=["id", "name", "age"])
            row = next(reader)
            row["name"] = row["name"].upper()
            return [row]
        except Exception:
            return []


schema = {
    'fields': [
        {'name': 'id', 'type': 'INTEGER'},
        {'name': 'name', 'type': 'STRING'},
        {'name': 'age', 'type': 'INTEGER'}
    ]
}

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='GCS input path')
    parser.add_argument('--output_table', required=True, help='BigQuery output table')
    args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args, save_main_session=True)

    with Pipeline(options=pipeline_options) as p:
        (
            p
            | "Read CSV lines" >> ReadFromText(args.input, skip_header_lines=1)
            | "Parse and Transform" >> ParDo(UpperCaseNamesFn())
            | "Write to BigQuery" >> WriteToBigQuery(
                args.output_table,
                schema=schema,
                write_disposition=BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED
            )
        )


if __name__ == '__main__':
    run()
