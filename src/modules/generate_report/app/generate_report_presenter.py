import datetime
import time

from src.shared.environments import Environments
from src.shared.clients.s3_client import s3_client

from .generate_report_extractor import GenerateReportExtractor
from .generate_report_aggregator import GenerateReportAggregator
from .generate_report_transformer import GenerateReportTransformer

repo = Environments.get_envs().get_booking_repo()()


def lambda_handler(event, context):
    extractor = GenerateReportExtractor(repo)
    #"2025-04-03T15:00:00Z" date format

    current_date = datetime.datetime.now()

    year = current_date.year
    month = current_date.month
    year_start_date = datetime.datetime(year, 1, 1)

    start_date = int(time.mktime(year_start_date.timetuple())) * 1000
    final_date = int(time.mktime(current_date.timetuple())) * 1000

    file_name = f"relatorio_gerado_em_{current_date.day}_{month}_{year}.xlsx"
    file_path = f"relatorios/"

    extractor = GenerateReportExtractor(booking_repository=repo)
    aggregator = GenerateReportAggregator(extractor=extractor)
    transformer = GenerateReportTransformer(aggregator=aggregator)
    report = transformer(start_date, final_date)

    if report:

        bucket_manager = s3_client()

        try:

            response = bucket_manager.upload_file(key=file_path + file_name,
                                                  file_type=".xlsx",
                                                  decode_string=report,
                                                  )

            print("Report generated and uploaded successfully")

            return 1

        except:

            raise Exception("Error uploading file to S3")


    else:

        raise Exception("Error generating report")
