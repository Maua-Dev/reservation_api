import pytest

from src.modules.generate_report.app.generate_report_aggregator import GenerateReportAggregator
from src.modules.generate_report.app.generate_report_extractor import GenerateReportExtractor
from src.shared.infra.repositories.booking_repository_dynamo import BookingRepositoryDynamo


class TestGenerateReportAggregator:

    @pytest.mark.skip("Can't run test in gh actions")
    def test_generate_report_aggregator(self):

        repo = BookingRepositoryDynamo()

        # Arrange
        extractor = GenerateReportExtractor(booking_repository=repo)
        aggregator = GenerateReportAggregator(extractor)

        # Act
        result = aggregator(1577836800, 1767225600)

        print(result)