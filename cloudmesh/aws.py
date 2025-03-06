import boto3
from datetime import datetime, timedelta

class AWSReservationCost:
    def __init__(self, access_key, secret_key, region):
        self.client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_reservation_cost(self, start_date=None, end_date=None, granularity="MONTHLY"):
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")

        response = self.client.get_reservation_utilization(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity=granularity
        )
        return response
