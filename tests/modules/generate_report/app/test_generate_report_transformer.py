import pytest

from src.modules.generate_report.app.generate_report_aggregator import GenerateReportAggregator
from src.modules.generate_report.app.generate_report_extractor import GenerateReportExtractor
from src.modules.generate_report.app.generate_report_transformer import GenerateReportTransformer
from src.shared.infra.repositories.booking_repository_dynamo import BookingRepositoryDynamo
import tempfile
import os

class TestGenerateReportTransformer:

    @pytest.mark.skip("Can't run test in gh actions")
    def test_generate_report_transformer(self):

        repo = BookingRepositoryDynamo()
        extractor = GenerateReportExtractor(booking_repository=repo)
        aggregator = GenerateReportAggregator(extractor=extractor)

        transformer = GenerateReportTransformer(aggregator=aggregator)

        output = transformer(1577836800, 1767225600)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
            tmp_file.write(output.read())
            tmp_file_path = tmp_file.name

        os.startfile(tmp_file_path)