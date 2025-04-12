import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


class UpperCaseNamesFn(beam.DoFn):
    def process(self, element):
        import csv
        from io import StringIO

        # CSV line to dict
        reader = csv.DictReader(StringIO(element), fieldnames=["id", "name", "age"])
        row = next(reader)
        row["name"] = row["name"].upper()
        return [row]


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='GCS input path')
    parser.add_argument('--output_table', required=True, help='BigQuery output table')
    args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args, save_main_session=True)

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "Read CSV lines" >> beam.io.ReadFromText(args.input, skip_header_lines=1)
            | "Parse and Transform" >> beam.ParDo(UpperCaseNamesFn())
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                args.output_table,
                schema='id:INTEGER,name:STRING,age:INTEGER',
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )


if __name__ == '__main__':
    run()
