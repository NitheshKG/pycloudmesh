import boto3
from datetime import datetime, timedelta
from pycloudmesh.definitions import AWSReservationService


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

    def get_reservation_recommendation(self, look_back_period: str = '60', term: str = 'ONE_YEAR',
                                           payment_option: str = "ALL_UPFRONT",
                                           /):

        services_list = [AWSReservationService.AMAZONEC2, AWSReservationService.AMAZONRDS,
                         AWSReservationService.AMAZONREDSHIFT, AWSReservationService.AMAZONELASTICCACHE,
                         AWSReservationService.AMAZONOPENSEARCHSERVICE]

        params = {
            "LookbackPeriodInDays": look_back_period,
            "TermInYears": term,
            "PaymentOption": payment_option
        }

        all_response = []

        for service in services_list:
            params["service"] = service
            response = self.client.get_reservation_recommendation(params)
            all_response.extend(response.get("Recommendations"))

        return all_response


class AWSBudgetManagement:
    def __init__(self, access_key: str, secret_key: str, region: str):
        self.client = boto3.client(
            "budgets",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def list_budgets(self, account_id: str,
                     /,
                     *,
                     max_results: int = None,
                     next_token: str = None):
        params = {"AccountId": account_id}
        if max_results:
            params["MaxResults"] = max_results
        if next_token:
            params["NextToken"] = next_token

        response = self.client.describe_budgets(**params)
        return response


class AWSCostManagement:
    def __init__(self, access_key: str, secret_key: str, region: str):
        self.client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_aws_cost_data(self, start_date: str = None, end_date: str = None, granularity: str = "MONTHLY"):
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")

        all_results = []
        next_token = None

        while True:
            params = {
                "TimePeriod": {"Start": start_date, "End": end_date},
                "Granularity": granularity,
            }

            if next_token:
                params["NextPageToken"] = next_token

            response = self.client.get_cost_and_usage(**params)
            all_results.extend(response.get("ResultsByTime", []))

            next_token = response.get("NextPageToken")
            if not next_token:
                break

        return all_results
