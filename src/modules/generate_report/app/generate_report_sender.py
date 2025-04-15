import datetime
import time

from src.shared.environments import Environments

from .generate_report_extractor import GenerateReportExtractor
from .generate_report_aggregator import GenerateReportAggregator

repo = Environments.get_envs().get_booking_repo()()


def lambda_handler(event, context):
    extractor = GenerateReportExtractor(repo)
    #"2025-04-03T15:00:00Z" date format

    current_date_str = event.get("current_date", None)

    if current_date_str:
        current_date = datetime.datetime.fromisoformat(current_date_str.replace('Z', '+00:00'))

        year = current_date.year
        year_start_date = datetime.datetime(year, 1, 1)

        start_date = int(time.mktime(year_start_date.timetuple()))
        final_date = int(time.mktime(current_date.timetuple()))

        file_fomart = f"relatorio_gerado_em_{current_date.day}_{current_date.month}_{current_date.year}.xlsx"

    else:
        start_date = int(time.mktime(datetime.datetime(datetime.datetime.now().year, 1, 1).timetuple()))
        final_date = int(time.mktime(datetime.datetime.now().timetuple()))

        file_format = f"relatorio_gerado_em_{datetime.datetime.now().day}_{datetime.datetime.now().month}_{datetime.datetime.now().year}.xlsx"


    extractor = GenerateReportExtractor(repo)
    aggregator = GenerateReportAggregator(extractor)
    report = aggregator(start_date, final_date)

    if report:

        Environments.get_envs()


