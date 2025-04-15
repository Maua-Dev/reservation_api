import pytest

from src.modules.generate_report.app.generate_report_aggregator import GenerateReportAggregator
from src.modules.generate_report.app.generate_report_extractor import GenerateReportExtractor
from src.modules.generate_report.app.generate_report_sender import lambda_handler
from src.modules.generate_report.app.generate_report_transformer import GenerateReportTransformer
from src.shared.infra.repositories.booking_repository_dynamo import BookingRepositoryDynamo


class TestGenerateReportSender:

    @pytest.mark.skip("Can't run test in gh actions")
    def test_generate_report_sender(self):

        event_from_event_bridge = {
            "version": "0",
            "id": "12345678-1234-1234-1234-123456789012",
            "detail-type": "EC2 Instance State-change Notification",
            "source": "aws.ec2",
            "account": "123456789012",
            "time": "2023-11-11T12:00:00Z",
            "region": "us-east-1",
            "resources": [
                "arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0"
            ],
            "detail": {
                "instance-id": "i-1234567890abcdef0",
                "state": "running"
            }
        }

        sender = lambda_handler(event_from_event_bridge, None)
