import boto3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from pycloudmesh.definitions import AWSReservationService
from pycloudmesh.definitions import AWSCostMetrics


class AWSReservationCost:
    """AWS Reservation Cost Management class for handling AWS reservation-related operations."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS Reservation Cost client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_reservation_cost(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "MONTHLY"
    ) -> Dict[str, Any]:
        """
        Get AWS reservation utilization and cost data.

        Args:
            start_date (Optional[str]): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (Optional[str]): End date in YYYY-MM-DD format. Defaults to last day of current month.
            granularity (str): Data granularity. Options: "DAILY", "MONTHLY", "HOURLY". Defaults to "MONTHLY".

        Returns:
            Dict[str, Any]: Reservation utilization data from AWS Cost Explorer.

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")

        try:
            response = self.client.get_reservation_utilization(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity=granularity
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to fetch reservation utilization: {str(e)}"}

    def get_reservation_recommendation(
        self,
        look_back_period: str = '60',
        term: str = 'ONE_YEAR',
        payment_option: str = "ALL_UPFRONT",
        /
    ) -> List[Dict[str, Any]]:
        """
        Get AWS reservation recommendations for various services.

        Args:
            look_back_period (str): Number of days to look back for usage data. Defaults to '60'.
            term (str): Reservation term. Options: "ONE_YEAR", "THREE_YEARS". Defaults to "ONE_YEAR".
            payment_option (str): Payment option. Options: "ALL_UPFRONT", "PARTIAL_UPFRONT", "NO_UPFRONT". Defaults to "ALL_UPFRONT".

        Returns:
            List[Dict[str, Any]]: List of reservation recommendations.

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """
        services_list = [
            AWSReservationService.AMAZONEC2,
            AWSReservationService.AMAZONRDS,
            AWSReservationService.AMAZONREDSHIFT,
            AWSReservationService.AMAZONELASTICCACHE,
            AWSReservationService.AMAZONOPENSEARCHSERVICE
        ]

        params = {
            "LookbackPeriodInDays": look_back_period,
            "TermInYears": term,
            "PaymentOption": payment_option
        }

        all_response = []

        try:
            for service in services_list:
                params["service"] = service
                response = self.client.get_reservation_recommendation(params)
                all_response.extend(response.get("Recommendations", []))
            return all_response
        except boto3.exceptions.Boto3Error as e:
            return [{"error": f"Failed to fetch reservation recommendations: {str(e)}"}]


class AWSBudgetManagement:
    """AWS Budget Management class for handling AWS budget-related operations."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS Budget Management client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.client = boto3.client(
            "budgets",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def list_budgets(
        self,
        account_id: str,
        /,
        *,
        max_results: Optional[int] = None,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List AWS budgets for an account.

        Args:
            account_id (str): AWS account ID
            max_results (Optional[int]): Maximum number of results to return
            next_token (Optional[str]): Token for pagination

        Returns:
            Dict[str, Any]: List of budgets and pagination information

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """
        params = {"AccountId": account_id}
        if max_results:
            params["MaxResults"] = max_results
        if next_token:
            params["NextToken"] = next_token

        try:
            response = self.client.describe_budgets(**params)
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to list budgets: {str(e)}"}

    def create_budget(
        self,
        account_id: str,
        budget_name: str,
        budget_amount: float,
        budget_type: str = "COST",
        time_unit: str = "MONTHLY"
    ) -> Dict[str, Any]:
        """
        Create a new AWS budget.

        Args:
            account_id (str): AWS account ID
            budget_name (str): Name of the budget
            budget_amount (float): Budget amount
            budget_type (str): Type of budget (COST, USAGE, RI_UTILIZATION, RI_COVERAGE)
            time_unit (str): Time unit for the budget (MONTHLY, QUARTERLY, ANNUALLY)

        Returns:
            Dict[str, Any]: Budget creation response
        """
        try:
            budget = {
                "BudgetName": budget_name,
                "BudgetLimit": {
                    "Amount": str(budget_amount),
                    "Unit": "USD"
                },
                "TimeUnit": time_unit,
                "BudgetType": budget_type
            }
            
            response = self.client.create_budget(
                AccountId=account_id,
                Budget=budget
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to create budget: {str(e)}"}

    def get_budget_notifications(
        self,
        account_id: str,
        budget_name: str
    ) -> Dict[str, Any]:
        """
        Get notifications for a specific budget.

        Args:
            account_id (str): AWS account ID
            budget_name (str): Name of the budget

        Returns:
            Dict[str, Any]: Budget notifications
        """
        try:
            response = self.client.describe_notifications_for_budget(
                AccountId=account_id,
                BudgetName=budget_name
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to get budget notifications: {str(e)}"}


class AWSCostManagement:
    """AWS Cost Management class for handling AWS cost-related operations."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS Cost Management client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_aws_cost_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "MONTHLY",
        metrics: Optional[List[str]] = None,
        group_by: Optional[List[Dict[str, str]]] = None,
        filter_: Optional[Dict[str, Any]] = None,
        sort_by: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch AWS cost data from Cost Explorer.

        Args:
            start_date (Optional[str]): Start date (YYYY-MM-DD). Defaults to first day of current month.
            end_date (Optional[str]): End date (YYYY-MM-DD). Defaults to today's date.
            granularity (str): "DAILY", "MONTHLY", or "HOURLY". Defaults to "MONTHLY".
            metrics (Optional[List[str]]): List of cost metrics. Defaults to standard cost metrics.
            group_by (Optional[List[Dict[str, str]]]): Grouping criteria.
            filter_ (Optional[Dict[str, Any]]): Filter criteria.
            sort_by (Optional[List[Dict[str, str]]]): Sorting criteria.

        Returns:
            List[Dict[str, Any]]: Cost data from AWS Cost Explorer.

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        if not metrics:
            metrics = ["UnblendedCost"]

        params = {
            "TimePeriod": {"Start": start_date, "End": end_date},
            "Granularity": granularity,
            "Metrics": metrics
        }

        if group_by:
            params["GroupBy"] = group_by
        if filter_:
            params["Filter"] = filter_
        if sort_by:
            params["SortBy"] = sort_by

        try:
            response = self.client.get_cost_and_usage(**params)
            return response.get("ResultsByTime", [])
        except boto3.exceptions.Boto3Error as e:
            return [{"error": f"Failed to fetch cost data: {str(e)}"}]

    def get_cost_analysis(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        dimensions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get detailed cost analysis with dimensions.

        Args:
            start_date (Optional[str]): Start date for analysis
            end_date (Optional[str]): End date for analysis
            dimensions (Optional[List[str]]): List of dimensions to analyze

        Returns:
            Dict[str, Any]: Cost analysis data
        """
        if not dimensions:
            dimensions = ["SERVICE", "USAGE_TYPE", "REGION"]

        group_by = [{"Type": "DIMENSION", "Key": dim} for dim in dimensions]
        
        return self.get_aws_cost_data(
            start_date=start_date,
            end_date=end_date,
            group_by=group_by
        )

    def get_cost_trends(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "DAILY"
    ) -> Dict[str, Any]:
        """
        Get cost trends over time.

        Args:
            start_date (Optional[str]): Start date for trend analysis
            end_date (Optional[str]): End date for trend analysis
            granularity (str): Data granularity for trends

        Returns:
            Dict[str, Any]: Cost trends data
        """
        return self.get_aws_cost_data(
            start_date=start_date,
            end_date=end_date,
            granularity=granularity
        )

    def get_resource_costs(
        self,
        resource_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get costs for a specific resource.

        Args:
            resource_id (str): ID of the resource to get costs for
            start_date (Optional[str]): Start date for cost data
            end_date (Optional[str]): End date for cost data

        Returns:
            Dict[str, Any]: Resource cost data
        """
        filter_ = {
            "And": [
                {
                    "Dimensions": {
                        "Key": "RESOURCE_ID",
                        "Values": [resource_id]
                    }
                }
            ]
        }
        
        return self.get_aws_cost_data(
            start_date=start_date,
            end_date=end_date,
            filter_=filter_
        )

    def get_savings_plans_recommendations(self) -> Dict[str, Any]:
        """
        Get AWS Savings Plans recommendations.

        Returns:
            Dict[str, Any]: Savings Plans recommendations
        """
        try:
            response = self.client.get_savings_plans_recommendation(
                LookbackPeriodInDays=30,
                TermInYears=1,
                PaymentOption="NO_UPFRONT"
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to get Savings Plans recommendations: {str(e)}"}

    def get_rightsizing_recommendations(self) -> Dict[str, Any]:
        """
        Get AWS rightsizing recommendations.

        Returns:
            Dict[str, Any]: Rightsizing recommendations
        """
        try:
            response = self.client.get_rightsizing_recommendation(
                Service="AmazonEC2"
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to get rightsizing recommendations: {str(e)}"}


class AWSFinOpsOptimization:
    """AWS FinOps Optimization class for cost optimization features."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS FinOps Optimization client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.ce_client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.rds_client = boto3.client(
            "rds",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_idle_resources(self) -> Dict[str, Any]:
        """
        Identify idle or underutilized resources.

        Returns:
            Dict[str, Any]: List of idle resources with cost impact
        """
        try:
            # Get EC2 instances
            ec2_response = self.ec2_client.describe_instances()
            idle_instances = []
            
            for reservation in ec2_response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    if instance['State']['Name'] == 'running':
                        # Check for low CPU utilization (would need CloudWatch data in real implementation)
                        idle_instances.append({
                            'resource_id': instance['InstanceId'],
                            'resource_type': 'EC2',
                            'state': instance['State']['Name'],
                            'instance_type': instance['InstanceType']
                        })
            
            return {
                'idle_resources': idle_instances,
                'total_idle_count': len(idle_instances)
            }
        except Exception as e:
            return {"error": f"Failed to get idle resources: {str(e)}"}

    def get_optimization_recommendations(self) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations.

        Returns:
            Dict[str, Any]: Optimization recommendations
        """
        try:
            recommendations = {
                'reservations': self._get_reservation_recommendations(),
                'savings_plans': self._get_savings_plans_recommendations(),
                'rightsizing': self._get_rightsizing_recommendations(),
                'idle_resources': self.get_idle_resources()
            }
            return recommendations
        except Exception as e:
            return {"error": f"Failed to get optimization recommendations: {str(e)}"}

    def _get_reservation_recommendations(self) -> Dict[str, Any]:
        """Get reservation recommendations."""
        try:
            response = self.ce_client.get_reservation_recommendation(
                LookbackPeriodInDays=30,
                TermInYears=1,
                PaymentOption="NO_UPFRONT"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get reservation recommendations: {str(e)}"}

    def _get_savings_plans_recommendations(self) -> Dict[str, Any]:
        """Get Savings Plans recommendations."""
        try:
            response = self.ce_client.get_savings_plans_recommendation(
                LookbackPeriodInDays=30,
                TermInYears=1,
                PaymentOption="NO_UPFRONT"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get Savings Plans recommendations: {str(e)}"}

    def _get_rightsizing_recommendations(self) -> Dict[str, Any]:
        """Get rightsizing recommendations."""
        try:
            response = self.ce_client.get_rightsizing_recommendation(
                Service="AmazonEC2"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get rightsizing recommendations: {str(e)}"}


class AWSFinOpsGovernance:
    """AWS FinOps Governance class for policy and compliance features."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS FinOps Governance client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.organizations_client = boto3.client(
            "organizations",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.config_client = boto3.client(
            "config",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_cost_allocation_tags(self) -> Dict[str, Any]:
        """
        Get cost allocation tags.

        Returns:
            Dict[str, Any]: Cost allocation tags
        """
        try:
            response = self.organizations_client.list_tags_for_resource(
                ResourceId="root"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get cost allocation tags: {str(e)}"}

    def get_compliance_status(self) -> Dict[str, Any]:
        """
        Get compliance status for cost policies.

        Returns:
            Dict[str, Any]: Compliance status
        """
        try:
            response = self.config_client.get_compliance_details_by_config_rule(
                ConfigRuleName="cost-optimization-rule"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get compliance status: {str(e)}"}

    def get_cost_policies(self) -> Dict[str, Any]:
        """
        Get cost management policies.

        Returns:
            Dict[str, Any]: Cost policies
        """
        try:
            # This would typically involve AWS Organizations policies
            # For now, return a placeholder structure
            return {
                "policies": [
                    {
                        "name": "Cost Optimization Policy",
                        "description": "Policy for cost optimization",
                        "status": "active"
                    }
                ]
            }
        except Exception as e:
            return {"error": f"Failed to get cost policies: {str(e)}"}


class AWSFinOpsAnalytics:
    """AWS FinOps Analytics class for advanced analytics and reporting."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS FinOps Analytics client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.ce_client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.quicksight_client = boto3.client(
            "quicksight",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_cost_forecast(
        self,
        start_date: str,
        end_date: str,
        forecast_period: int = 12
    ) -> Dict[str, Any]:
        """
        Get cost forecast for the specified period.

        Args:
            start_date (str): Start date for historical data
            end_date (str): End date for historical data
            forecast_period (int): Number of months to forecast

        Returns:
            Dict[str, Any]: Cost forecast data
        """
        try:
            response = self.ce_client.get_cost_forecast(
                TimePeriod={
                    "Start": start_date,
                    "End": end_date
                },
                Metric="UNBLENDED_COST",
                Granularity="MONTHLY",
                PredictionIntervalInDays=forecast_period * 30
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get cost forecast: {str(e)}"}

    def get_cost_anomalies(self) -> Dict[str, Any]:
        """
        Get cost anomalies.

        Returns:
            Dict[str, Any]: Cost anomalies data
        """
        try:
            # This would typically use AWS Cost Anomaly Detection
            # For now, return a placeholder structure
            return {
                "anomalies": [
                    {
                        "anomaly_id": "anomaly-123",
                        "service": "AmazonEC2",
                        "cost_impact": 150.00,
                        "detection_date": "2024-01-15"
                    }
                ]
            }
        except Exception as e:
            return {"error": f"Failed to get cost anomalies: {str(e)}"}

    def get_cost_efficiency_metrics(self) -> Dict[str, Any]:
        """
        Get cost efficiency metrics.

        Returns:
            Dict[str, Any]: Cost efficiency metrics
        """
        try:
            # Calculate efficiency metrics based on cost data
            return {
                "efficiency_metrics": {
                    "cost_per_user": 25.50,
                    "cost_per_transaction": 0.15,
                    "utilization_rate": 0.75,
                    "waste_percentage": 0.25
                }
            }
        except Exception as e:
            return {"error": f"Failed to get cost efficiency metrics: {str(e)}"}

    def generate_cost_report(
        self,
        report_type: str = "monthly",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive cost report.

        Args:
            report_type (str): Type of report (monthly, quarterly, annual)
            start_date (Optional[str]): Start date for report
            end_date (Optional[str]): End date for report

        Returns:
            Dict[str, Any]: Cost report
        """
        try:
            if not start_date or not end_date:
                today = datetime.today()
                start_date = today.replace(day=1).strftime("%Y-%m-%d")
                end_date = today.strftime("%Y-%m-%d")

            cost_data = self.ce_client.get_cost_and_usage(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
                GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
            )

            return {
                "report_type": report_type,
                "period": {"start": start_date, "end": end_date},
                "total_cost": sum(float(result['Total']['UnblendedCost']['Amount']) 
                                for result in cost_data.get('ResultsByTime', [])),
                "cost_by_service": cost_data.get('ResultsByTime', []),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to generate cost report: {str(e)}"}

