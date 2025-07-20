from typing import Optional, Dict, Any, Union, List
from functools import lru_cache
from abc import ABC, abstractmethod
from pycloudmesh.providers.aws import (
    AWSBudgetManagement, AWSCostManagement, AWSReservationCost,
    AWSFinOpsOptimization, AWSFinOpsGovernance, AWSFinOpsAnalytics
)
from pycloudmesh.providers.azure import (
    AzureReservationCost, AzureBudgetManagement, AzureCostManagement,
    AzureFinOpsOptimization, AzureFinOpsGovernance, AzureFinOpsAnalytics
)
from pycloudmesh.providers.gcp import (
    GCPReservationCost, GCPCostManagement, GCPBudgetManagement,
    GCPFinOpsOptimization, GCPFinOpsGovernance, GCPFinOpsAnalytics
)


class CloudProvider(ABC):
    """Abstract base class for cloud providers with comprehensive FinOps features."""
    
    # Core FinOps Features
    @abstractmethod
    def get_reservation_cost(self) -> Dict[str, Any]:
        """Get reservation costs."""
        pass
    
    @abstractmethod
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        """Get reservation recommendations."""
        pass
    
    @abstractmethod
    def list_budgets(self, **kwargs) -> Dict[str, Any]:
        """List budgets."""
        pass
    
    @abstractmethod
    def get_cost_data(self, **kwargs) -> Dict[str, Any]:
        """Get cost data for the cloud provider."""
        pass
    
    @abstractmethod
    def get_cost_analysis(self, **kwargs) -> Dict[str, Any]:
        """Get detailed cost analysis with dimensions."""
        pass
    
    @abstractmethod
    def get_cost_trends(self, **kwargs) -> Dict[str, Any]:
        """Get cost trends over time."""
        pass
    
    @abstractmethod
    def get_resource_costs(self, resource_id: str, **kwargs) -> Dict[str, Any]:
        """Get costs for a specific resource."""
        pass
    
    # Advanced FinOps Features
    @abstractmethod
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        """Get comprehensive optimization recommendations."""
        pass
    
    @abstractmethod
    def get_cost_forecast(self, **kwargs) -> Dict[str, Any]:
        """Get cost forecast for the specified period."""
        pass
    
    @abstractmethod
    def get_cost_anomalies(self, **kwargs) -> Dict[str, Any]:
        """Get cost anomalies."""
        pass
    
    @abstractmethod
    def get_cost_efficiency_metrics(self, **kwargs) -> Dict[str, Any]:
        """Get cost efficiency metrics."""
        pass
    
    @abstractmethod
    def generate_cost_report(self, **kwargs) -> Dict[str, Any]:
        """Generate comprehensive cost report."""
        pass
    
    @abstractmethod
    def get_governance_policies(self, **kwargs) -> Dict[str, Any]:
        """Get governance policies and compliance status."""
        pass


class AWSProvider(CloudProvider):
    def __init__(self, access_key: str, secret_key: str, region: str):
        self.reservation_client = AWSReservationCost(access_key, secret_key, region)
        self.cost_client = AWSCostManagement(access_key, secret_key, region)
        self.budget_client = AWSBudgetManagement(access_key, secret_key, region)
        self.optimization_client = AWSFinOpsOptimization(access_key, secret_key, region)
        self.governance_client = AWSFinOpsGovernance(access_key, secret_key, region)
        self.analytics_client = AWSFinOpsAnalytics(access_key, secret_key, region)
    
    # Core FinOps Features
    def get_reservation_cost(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS reservation utilization and cost data.

        This method retrieves reservation utilization and cost data from AWS Cost Explorer,
        providing insights into how effectively your reservations are being used.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to one month before today.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            granularity (str, optional): Data granularity. One of "DAILY", "MONTHLY", or "HOURLY". Defaults to "MONTHLY".

        Returns:
            Dict[str, Any]: Reservation utilization data from AWS Cost Explorer including:
                - Reservation utilization metrics
                - Cost data for reservation period
                - Reservation order details
                - Individual reservation information
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_reservation_cost(
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="MONTHLY"
            ... )
        """
        return self.reservation_client.get_reservation_cost(**kwargs)
    
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS reservation purchase recommendations.

        This method provides reservation purchase recommendations for various AWS services
        using Cost Explorer, helping you identify cost optimization opportunities.

        Args:
            Service (str, optional): AWS service name. Defaults to "AmazonEC2".
                Common values: "AmazonEC2", "AmazonRDS", "AmazonElastiCache", etc.
            LookbackPeriodInDays (str, optional): Lookback period for analysis.
                One of "SEVEN_DAYS", "THIRTY_DAYS", "SIXTY_DAYS". Defaults to "SIXTY_DAYS".
            TermInYears (str, optional): Reservation term. One of "ONE_YEAR", "THREE_YEARS". Defaults to "ONE_YEAR".
            PaymentOption (str, optional): Payment option. One of "NO_UPFRONT", "PARTIAL_UPFRONT", "ALL_UPFRONT". Defaults to "NO_UPFRONT".
            AccountScope (str, optional): Account scope. One of "PAYER", "LINKED". Defaults to "PAYER".
            AccountId (str, optional): AWS Account ID for specific account analysis.
            NextPageToken (str, optional): Token for pagination.
            PageSize (int, optional): Page size for pagination.
            Filter (dict, optional): Filter criteria for recommendations.
            ServiceSpecification (dict, optional): Service-specific specifications.

        Returns:
            Dict[str, Any]: Reservation purchase recommendations from AWS Cost Explorer including:
                - Recommended reservation purchases
                - Potential savings estimates
                - Usage analysis data
                - Service-specific recommendations
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_reservation_recommendation(
            ...     Service="AmazonEC2",
            ...     LookbackPeriodInDays="THIRTY_DAYS",
            ...     TermInYears="ONE_YEAR",
            ...     PaymentOption="NO_UPFRONT"
            ... )
        """
        return self.reservation_client.get_reservation_recommendation(**kwargs)
    
    def get_reservation_coverage(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS reservation coverage data.

        This method retrieves reservation coverage data from AWS Cost Explorer,
        showing how much of your usage is covered by reservations.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to 30 days ago.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            granularity (str, optional): Data granularity. One of "DAILY" or "MONTHLY". Defaults to "MONTHLY".
            GroupBy (list, optional): List of grouping dicts for analysis.
            Filter (dict, optional): Filter criteria for the coverage data.
            NextPageToken (str, optional): Token for pagination.

        Returns:
            Dict[str, Any]: Reservation coverage data from AWS Cost Explorer including:
                - Coverage metrics by time period
                - Reservation utilization percentages
                - Coverage breakdown by service/region
                - Uncovered usage analysis
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_reservation_coverage(
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="DAILY",
            ...     GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
            ... )
        """
        return self.reservation_client.get_reservation_coverage(**kwargs)
    
    def list_budgets(self, **kwargs) -> Dict[str, Any]:
        """
        List AWS budgets for an account.

        This method retrieves all budgets configured for the specified AWS account,
        including budget details and pagination information.

        Args:
            aws_account_id (str): AWS account ID (required).
            aws_max_results (int, optional): Maximum number of results to return.
            aws_next_token (str, optional): Token for pagination.

        Returns:
            Dict[str, Any]: List of budgets and pagination information from AWS including:
                - Budgets: List of budget objects with details
                - NextToken: Token for pagination (if more results available)
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.list_budgets(
            ...     aws_account_id="123456789012",
            ...     aws_max_results=10
            ... )
        """
        return self.budget_client.list_budgets(
            kwargs.get('aws_account_id'),
            max_results=kwargs.get('aws_max_results'),
            next_token=kwargs.get('aws_next_token')
        )
    
    def get_cost_data(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch AWS cost data for a given period and dimensions using Cost Explorer.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            granularity (str, optional): Data granularity. One of "DAILY", "MONTHLY", or "HOURLY". Defaults to "MONTHLY".
            metrics (list, optional): List of cost metrics to aggregate. Defaults to ["UnblendedCost"].
                Common values: "UnblendedCost", "BlendedCost", "AmortizedCost", "NetAmortizedCost", "UsageQuantity", etc.
            group_by (list, optional): List of grouping dicts, e.g., [{"Type": "DIMENSION", "Key": "SERVICE"}].
                See AWS Cost Explorer docs for valid dimensions.
            filter_ (dict, optional): Additional filter criteria for the query (see AWS Cost Explorer filter syntax).

        Returns:
            Dict[str, Any]: Cost data from AWS Cost Explorer. If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_cost_data(
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="MONTHLY",
            ...     metrics=["UnblendedCost"],
            ...     group_by=[{"Type": "DIMENSION", "Key": "SERVICE"}],
            ...     filter_={
            ...         "Dimensions": {
            ...             "Key": "REGION",
            ...             "Values": ["us-east-1"]
            ...         }
            ...     }
            ... )
        """
        return self.cost_client.get_aws_cost_data(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'MONTHLY'),
            metrics=kwargs.get('metrics'),
            group_by=kwargs.get('group_by'),
            filter_=kwargs.get('filter_')
        )
    
    def get_cost_analysis(self, **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost analysis with insights and breakdowns for AWS.

        This method provides comprehensive cost analysis including cost breakdowns by service,
        top services by cost, cost trends, and actionable insights.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            dimensions (list, optional): List of dimensions to analyze (max 2). Defaults to ["SERVICE", "REGION"].
                Common values: "SERVICE", "REGION", "USAGE_TYPE", "LINKED_ACCOUNT", "OPERATION", etc.

        Returns:
            Dict[str, Any]: Cost analysis with insights, breakdowns, and trends.
                {
                    "period": {"start": ..., "end": ...},
                    "dimensions": [...],
                    "total_cost": ...,
                    "cost_breakdown": {...},
                    "top_services": [...],
                    "cost_trends": [...],
                    "insights": [...]
                }
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_cost_analysis(
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     dimensions=["SERVICE", "REGION"]
            ... )
        """
        return self.cost_client.get_aws_cost_analysis(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            dimensions=kwargs.get('dimensions')
        )
    
    def get_cost_trends(self, **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost trends analysis with insights and patterns for AWS.

        This method provides comprehensive cost trend analysis including growth rates,
        peak periods, patterns, and actionable insights.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            granularity (str, optional): Data granularity. One of "DAILY", "MONTHLY", or "HOURLY". Defaults to "DAILY".
            metrics (list, optional): List of cost metrics to analyze. Defaults to ["UnblendedCost"].
            group_by (list, optional): List of grouping dicts for analysis.
            filter_ (dict, optional): Additional filter criteria for the query.
            sort_by (list, optional): Sorting criteria for the results.

        Returns:
            Dict[str, Any]: Cost trends analysis with patterns, growth rates, and insights.
                {
                    "period": {"start": ..., "end": ...},
                    "granularity": ...,
                    "total_periods": ...,
                    "total_cost": ...,
                    "average_daily_cost": ...,
                    "cost_periods": [...],
                    "trend_direction": ...,
                    "growth_rate": ...,
                    "peak_periods": [...],
                    "low_periods": [...],
                    "patterns": [...],
                    "insights": [...]
                }
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_cost_trends(
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="DAILY",
            ...     group_by=[{"Type": "DIMENSION", "Key": "SERVICE"}]
            ... )
        """
        return self.cost_client.get_aws_cost_trends(**kwargs)
    
    def get_resource_costs(self, **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost analysis for a specific AWS resource.

        This method provides comprehensive cost analysis for a specific resource including
        cost breakdowns, utilization insights, and optimization recommendations.

        Args:
            resource_id (str, required): ID of the resource to get costs for.
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            granularity (str, optional): Data granularity. One of "DAILY", "MONTHLY", or "HOURLY". Defaults to "DAILY".

        Returns:
            Dict[str, Any]: Detailed resource cost analysis with insights and breakdowns.
                {
                    "resource_id": ...,
                    "resource_type": ...,
                    "period": {"start": ..., "end": ...},
                    "granularity": ...,
                    "total_cost": ...,
                    "total_periods": ...,
                    "active_periods": ...,
                    "cost_periods": [...],
                    "cost_breakdown": {...},
                    "utilization_insights": [...],
                    "cost_trends": [...],
                    "recommendations": [...]
                }
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_resource_costs(
            ...     resource_id="i-1234567890abcdef0",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="DAILY"
            ... )
        """
        return self.cost_client.get_aws_resource_costs(
            resource_id=kwargs.get('resource_id'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'DAILY')
        )
    
    # Advanced FinOps Features
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations for AWS.

        This method provides optimization recommendations including savings plans,
        reservations, rightsizing, and idle resources.

        Args:
            **kwargs: Additional parameters for specific optimization types.

        Returns:
            Dict[str, Any]: Optimization recommendations including:
                - 'savings_plans': Savings Plans recommendations
                - 'reservations': Reserved Instance recommendations
                - 'rightsizing': Rightsizing recommendations
                - 'idle_resources': Idle resource recommendations
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_optimization_recommendations()
        """
        return self.optimization_client.get_optimization_recommendations()
    
    def get_cost_forecast(self, **kwargs) -> Dict[str, Any]:
        """
        Get cost forecast for the specified period using AWS Cost Explorer.

        This method provides cost forecasting capabilities with support for various
        parameters and ensures required parameters are present with sensible defaults.

        Args:
            TimePeriod (dict, optional): Time period for forecast. If not provided, defaults to future period.
            Metric (str, optional): Cost metric for forecasting. Defaults to "UNBLENDED_COST".
            Granularity (str, optional): Data granularity. Defaults to "MONTHLY".
            Filter (dict, optional): Filter criteria for the forecast.
            BillingViewArn (str, optional): Billing view ARN for the forecast.
            PredictionIntervalLevel (int, optional): Prediction interval level.

        Returns:
            Dict[str, Any]: Cost forecast data from AWS Cost Explorer.
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_cost_forecast(
            ...     TimePeriod={"Start": "2024-02-01", "End": "2024-03-01"},
            ...     Metric="UNBLENDED_COST",
            ...     Granularity="MONTHLY"
            ... )
        """
        return self.analytics_client.get_cost_forecast(**kwargs)
    
    def get_cost_anomalies(self, **kwargs) -> Dict[str, Any]:
        """
        Get cost anomalies using AWS Cost Explorer.

        This method identifies cost anomalies with support for various parameters
        and ensures required parameters are present with sensible defaults.

        Args:
            DateInterval (dict, optional): Date interval for anomaly detection. If not provided, defaults to last month.
            MonitorArn (str, optional): Monitor ARN for specific anomaly monitoring.
            Feedback (str, optional): Feedback for anomaly detection.
            TotalImpact (dict, optional): Total impact criteria for anomalies.
            NextPageToken (str, optional): Token for pagination.
            MaxResults (int, optional): Maximum number of results to return.

        Returns:
            Dict[str, Any]: Cost anomalies data from AWS Cost Explorer.
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_cost_anomalies(
            ...     DateInterval={"StartDate": "2024-01-01", "EndDate": "2024-01-31"},
            ...     MaxResults=10
            ... )
        """
        return self.analytics_client.get_cost_anomalies(**kwargs)
    
    def get_cost_efficiency_metrics(self, **kwargs) -> Dict[str, Any]:
        """
        Calculate cost efficiency metrics from AWS Cost Explorer.

        This method calculates real cost efficiency metrics with support for various
        parameters and ensures required parameters are present with sensible defaults.

        Args:
            user_count (int, optional): Number of users for cost per user calculation.
            transaction_count (int, optional): Number of transactions for cost per transaction calculation.
            TimePeriod (dict, optional): Time period for analysis. If not provided, defaults to current month.
            Granularity (str, optional): Data granularity. Defaults to "MONTHLY".
            Metrics (list, optional): List of cost metrics. Defaults to ["UnblendedCost"].
            GroupBy (list, optional): Grouping criteria. Defaults to [{"Type": "DIMENSION", "Key": "SERVICE"}].
            Filter (dict, optional): Filter criteria for the analysis.
            BillingViewArn (str, optional): Billing view ARN for the analysis.
            NextPageToken (str, optional): Token for pagination.

        Returns:
            Dict[str, Any]: Cost efficiency metrics including:
                - 'total_cost': Total cost for the period
                - 'cost_by_service': Cost breakdown by service
                - 'waste_estimate': Estimated waste cost
                - 'cost_per_user': Cost per user (if user_count provided)
                - 'cost_per_transaction': Cost per transaction (if transaction_count provided)
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_cost_efficiency_metrics(
            ...     user_count=100,
            ...     transaction_count=1000,
            ...     TimePeriod={"Start": "2024-01-01", "End": "2024-01-31"}
            ... )
        """
        return self.analytics_client.get_cost_efficiency_metrics(**kwargs)
    
    def generate_cost_report(self, **kwargs) -> Dict[str, Any]:
        """
        Generate comprehensive cost report using AWS Cost Explorer.

        This method generates comprehensive cost reports with support for various
        parameters and ensures required parameters are present with sensible defaults.

        Args:
            report_type (str, optional): Type of report (monthly, quarterly, annual). Defaults to "monthly".
            TimePeriod (dict, optional): Time period for the report. If not provided, defaults to current month.
            Granularity (str, optional): Data granularity. Defaults to "MONTHLY".
            Metrics (list, optional): List of cost metrics. Defaults to ["UnblendedCost"].
            GroupBy (list, optional): Grouping criteria. Defaults to [{"Type": "DIMENSION", "Key": "SERVICE"}].
            Filter (dict, optional): Filter criteria for the report.
            BillingViewArn (str, optional): Billing view ARN for the report.
            NextPageToken (str, optional): Token for pagination.

        Returns:
            Dict[str, Any]: Comprehensive cost report including:
                - 'report_type': Type of report generated
                - 'period': Time period covered
                - 'total_cost': Total cost for the period
                - 'cost_by_service': Cost breakdown by service
                - 'generated_at': Timestamp of report generation
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.generate_cost_report(
            ...     report_type="monthly",
            ...     TimePeriod={"Start": "2024-01-01", "End": "2024-01-31"},
            ...     GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
            ... )
        """
        return self.analytics_client.generate_cost_report(**kwargs)
    
    def get_governance_policies(self, **kwargs) -> Dict[str, Any]:
        """
        Get governance policies and compliance status for AWS.

        This method retrieves cost allocation tags, compliance status, and cost-related policies.

        Args:
            ResourceId (str, optional): Resource ID for cost allocation tags.
            ConfigRuleName (str, optional): Config rule name for compliance status.

        Returns:
            Dict[str, Any]: Governance policies and compliance information including:
                - 'cost_allocation_tags': Cost allocation tags
                - 'compliance_status': Compliance status for cost policies
                - 'cost_policies': Cost-related governance policies
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_governance_policies(
            ...     ResourceId="arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0",
            ...     ConfigRuleName="cost-optimization-rule"
            ... )
        """
        return {
            'cost_allocation_tags': self.governance_client.get_cost_allocation_tags(**kwargs),
            'compliance_status': self.governance_client.get_compliance_status(**kwargs),
            'cost_policies': self.governance_client.get_cost_policies(**kwargs)
        }
    
    def create_budget(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new AWS budget.

        This method creates a budget in AWS for the specified account, with support for notifications and custom budget types.

        Args:
            aws_account_id (str): AWS account ID (required).
            budget_name (str): Name of the budget (required).
            budget_amount (float): Budget amount in USD (required).
            budget_type (str, optional): Type of budget. One of "COST", "USAGE", "RI_UTILIZATION", "RI_COVERAGE".
                Defaults to "COST".
            time_unit (str, optional): Time unit for the budget. One of "MONTHLY", "QUARTERLY", "ANNUALLY".
                Defaults to "MONTHLY".
            notifications_with_subscribers (list, optional): List of notification dicts for budget alerts.
                Each dict should contain:
                    - Notification: {
                        "NotificationType": "ACTUAL" or "FORECASTED",
                        "ComparisonOperator": "GREATER_THAN" or "LESS_THAN" or "EQUAL_TO",
                        "Threshold": float (percentage),
                        "ThresholdType": "PERCENTAGE" or "ABSOLUTE_VALUE"
                      }
                    - Subscribers: [
                        {"SubscriptionType": "EMAIL", "Address": "user@example.com"},
                        ...
                      ]

        Returns:
            Dict[str, Any]: AWS response for budget creation. If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.create_budget(
            ...     aws_account_id="123456789012",
            ...     budget_name="monthly-budget",
            ...     budget_amount=1000.0,
            ...     budget_type="COST",
            ...     time_unit="MONTHLY",
            ...     notifications_with_subscribers=[
            ...         {
            ...             "Notification": {
            ...                 "NotificationType": "ACTUAL",
            ...                 "ComparisonOperator": "GREATER_THAN",
            ...                 "Threshold": 80.0,
            ...                 "ThresholdType": "PERCENTAGE"
            ...             },
            ...             "Subscribers": [
            ...                 {"SubscriptionType": "EMAIL", "Address": "admin@example.com"}
            ...             ]
            ...         }
            ...     ]
            ... )
        """
        return self.budget_client.create_budget(
            account_id=kwargs.get('aws_account_id'),
            budget_name=kwargs.get('budget_name'),
            budget_amount=kwargs.get('budget_amount'),
            budget_type=kwargs.get('budget_type', 'COST'),
            time_unit=kwargs.get('time_unit', 'MONTHLY'),
            notifications_with_subscribers=kwargs.get('notifications_with_subscribers')
        )
    
    def get_budget_notifications(self, **kwargs) -> Dict[str, Any]:
        """
        Get notifications for a specific AWS budget.

        This method retrieves all notifications configured for a specific budget.

        Args:
            aws_account_id (str): AWS account ID (required).
            budget_name (str): Name of the budget (required).

        Returns:
            Dict[str, Any]: Budget notifications from AWS. If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_budget_notifications(
            ...     aws_account_id="123456789012",
            ...     budget_name="monthly-budget"
            ... )
        """
        return self.budget_client.get_budget_notifications(
            account_id=kwargs.get('aws_account_id'),
            budget_name=kwargs.get('budget_name')
        )
    
    def get_savings_plans_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS Savings Plans recommendations.

        This method provides Savings Plans purchase recommendations with support for various parameters.

        Args:
            SavingsPlansType (str, optional): Type of Savings Plans. Defaults to "COMPUTE_SP".
            AccountScope (str, optional): Account scope. Defaults to "PAYER".
            LookbackPeriodInDays (str, optional): Lookback period. Defaults to "THIRTY_DAYS".
            TermInYears (str, optional): Term in years. Defaults to "ONE_YEAR".
            PaymentOption (str, optional): Payment option. Defaults to "NO_UPFRONT".
            NextPageToken (str, optional): Token for pagination.
            PageSize (int, optional): Page size for pagination.
            Filter (dict, optional): Filter criteria for recommendations.

        Returns:
            Dict[str, Any]: Savings Plans recommendations from AWS Cost Explorer.
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_savings_plans_recommendations(
            ...     SavingsPlansType="COMPUTE_SP",
            ...     TermInYears="ONE_YEAR",
            ...     PaymentOption="NO_UPFRONT"
            ... )
        """
        return self.optimization_client._get_savings_plans_recommendations(**kwargs)
    
    def get_rightsizing_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS rightsizing recommendations.

        This method provides rightsizing recommendations for EC2 instances and other resources.

        Args:
            **kwargs: Additional parameters for rightsizing recommendations.

        Returns:
            Dict[str, Any]: Rightsizing recommendations from AWS.
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_rightsizing_recommendations()
        """
        return self.optimization_client._get_rightsizing_recommendations(**kwargs)
    
    def get_idle_resources(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS idle resource recommendations.

        This method identifies idle or underutilized resources that could be stopped or downsized.

        Args:
            **kwargs: Additional parameters for idle resource detection.

        Returns:
            Dict[str, Any]: Idle resource recommendations from AWS.
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_idle_resources()
        """
        return self.optimization_client.get_idle_resources(**kwargs)
    
    def get_reservation_purchase_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS Reserved Instance purchase recommendations.

        This method provides Reserved Instance purchase recommendations with support for various parameters.

        Args:
            AccountScope (str, optional): Account scope. Defaults to "PAYER".
            LookbackPeriodInDays (str, optional): Lookback period. Defaults to "THIRTY_DAYS".
            TermInYears (str, optional): Term in years. Defaults to "ONE_YEAR".
            PaymentOption (str, optional): Payment option. Defaults to "NO_UPFRONT".
            Service (str, optional): Service name. Defaults to "Amazon Elastic Compute Cloud - Compute".
            AccountId (str, optional): AWS account ID.
            NextPageToken (str, optional): Token for pagination.
            PageSize (int, optional): Page size for pagination.
            Filter (dict, optional): Filter criteria for recommendations.
            ServiceSpecification (dict, optional): Service specification details.

        Returns:
            Dict[str, Any]: Reserved Instance recommendations from AWS Cost Explorer.
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> aws.get_reservation_purchase_recommendations(
            ...     Service="Amazon Elastic Compute Cloud - Compute",
            ...     TermInYears="ONE_YEAR",
            ...     PaymentOption="NO_UPFRONT"
            ... )
        """
        return self.optimization_client._get_reservation_purchase_recommendations(**kwargs)


class AzureProvider(CloudProvider):
    def __init__(self, subscription_id: str, token: str):
        self.reservation_client = AzureReservationCost(subscription_id, token)
        self.budget_client = AzureBudgetManagement(subscription_id, token)
        self.cost_client = AzureCostManagement(subscription_id, token)
        self.optimization_client = AzureFinOpsOptimization(subscription_id, token)
        self.governance_client = AzureFinOpsGovernance(subscription_id, token)
        self.analytics_client = AzureFinOpsAnalytics(subscription_id, token)
    
    # Core FinOps Features
    def get_reservation_cost(self, scope: str, **kwargs) -> Dict[str, Any]:
        """
        Get Azure reservation utilization and cost data.

        This method retrieves reservation utilization and cost data from Azure Cost Management,
        providing insights into how effectively your reservations are being used.

        Args:
            scope (str): Azure scope (subscription, resource group, etc.).
                Example: "/subscriptions/{subscription-id}/"
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to last day of current month.

        Returns:
            Dict[str, Any]: Reservation utilization data from Azure Cost Management including:
                - Reservation utilization metrics
                - Cost data for reservation period
                - Reservation order details
                - Individual reservation information
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> # Get reservation costs for a subscription with default date range
            >>> azure.get_reservation_cost(
            ...     scope="/subscriptions/your-subscription-id/"
            ... )
            
            >>> # Get reservation costs for a specific date range
            >>> azure.get_reservation_cost(
            ...     scope="/subscriptions/your-subscription-id/",
            ...     start_date="2024-06-01",
            ...     end_date="2024-06-30"
            ... )
            
            >>> # Get reservation costs for a resource group
            >>> azure.get_reservation_cost(
            ...     scope="/subscriptions/your-subscription-id/resourceGroups/your-rg/"
            ... )
        """
        return self.reservation_client.get_reservation_cost(
            scope,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date')
            )
    
    def get_reservation_recommendation(self, scope: str, **kwargs) -> Dict[str, Any]:
        """
        Get Azure reservation recommendations for various services.

        This method retrieves reservation purchase recommendations based on your usage patterns.
        You can filter recommendations by various criteria using OData filter syntax.

        Args:
            scope (str): Azure scope (subscription, resource group, etc.).
                Example: "/subscriptions/{subscription-id}/"
            filter (str, optional): OData filter string for server-side filtering.
                Common filter examples:
                - "ResourceGroup eq 'MyResourceGroup'"
                - "Location eq 'eastus'"
                - "Sku eq 'Standard_D2s_v3'"
                - "Term eq 'P1Y'" (1 year term)
                - "Term eq 'P3Y'" (3 year term)
            api_version (str, optional): API version for the Consumption API. Defaults to "2024-08-01".

        Returns:
            List[Dict[str, Any]]: List of reservation recommendations with details including:
                - Resource group, location, SKU information
                - Recommended quantity and term
                - Potential savings
                - Usage data used for recommendations

        Example:
            >>> # Get all recommendations for a subscription
            >>> recommendations = azure.get_reservation_recommendation(
            ...     scope="/subscriptions/your-subscription-id/"
            ... )
            
            >>> # Filter by resource group
            >>> recommendations = azure.get_reservation_recommendation(
            ...     scope="/subscriptions/your-subscription-id/",
            ...     filter="ResourceGroup eq 'Production'"
            ... )
            
            >>> # Filter by location and term
            >>> recommendations = azure.get_reservation_recommendation(
            ...     scope="/subscriptions/your-subscription-id/",
            ...     filter="Location eq 'eastus' and Term eq 'P1Y'"
            ... )
        """
        filter_param = kwargs.get('filter')
        api_version = kwargs.get('api_version', '2024-08-01')
        return self.reservation_client.get_reservation_recommendation(
            scope=scope,
            api_version=api_version,
            filter_param=filter_param
        )
    
    def get_cost_data(self, scope: str, **kwargs) -> Dict[str, Any]:
        """
        Fetch Azure cost data for a given scope (subscription, resource group, management group, or billing account).

        Args:
            scope (str): Azure scope string. Examples:
                - Subscription: "/subscriptions/{subscription-id}/"
                - Resource Group: "/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/"
                - Management Group: "/providers/Microsoft.Management/managementGroups/{management-group-id}/"
                - Billing Account: "/providers/Microsoft.Billing/billingAccounts/{billing-account-id}"
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today.
            granularity (str, optional): Data granularity. "Daily", "Monthly", or "None". Defaults to "Monthly".
            metrics (list, optional): List of cost metrics to aggregate. Defaults:
                - ["ActualCost"] for subscription/resource group/management group scopes
                - ["PreTaxCost"] for billing account scope
                Allowed values:
                    * Subscription/resource group/management group: "ActualCost", "AmortizedCost", "UsageQuantity"
                    * Billing account: "UsageQuantity", "PreTaxCost", "PreTaxCostUSD", "CostUSD", "Cost"
            group_by (list, optional): List of dimensions to group by (e.g., ["ResourceType", "ResourceLocation"]).
            filter_ (dict, optional): Additional filter criteria for the query.

        Returns:
            Dict[str, Any]: Cost data from Azure Cost Management API.

        Example:
            >>> # Subscription scope
            >>> azure.get_cost_data("/subscriptions/your-subscription-id/", granularity="Monthly", metrics=["ActualCost"])
            >>> # Billing account scope
            >>> azure.get_cost_data("/providers/Microsoft.Billing/billingAccounts/your-billing-account-id", metrics=["PreTaxCost"])
        """
        return self.cost_client.get_cost_data(
            scope,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'Monthly'),
            metrics=kwargs.get('metrics'),
            group_by=kwargs.get('group_by'),
            filter_=kwargs.get('filter_')
        )
    
    def get_cost_analysis(self, scope: str, **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost analysis with dimensions, returning a summary with breakdowns and insights.

        Args:
            scope (str): Azure scope (subscription, resource group, management group, or billing account)
            start_date (Optional[str]): Start date for analysis (YYYY-MM-DD). Defaults to first day of current month.
            end_date (Optional[str]): End date for analysis (YYYY-MM-DD). Defaults to today.
            dimensions (Optional[List[str]]): List of dimensions to analyze (group by). E.g. ["ResourceType", "ResourceLocation"]

        Returns:
            Dict[str, Any]: Cost analysis summary with breakdowns and insights.
                {
                    "period": {"start": ..., "end": ...},
                    "dimensions": [...],
                    "total_cost": ...,
                    "cost_breakdown": {...},
                    "cost_trends": [...],
                    "insights": [...]
                }

        Raises:
            ValueError: If invalid dimensions are provided for the given scope.

        Example:
            >>> azure.get_cost_analysis(
            ...     "/subscriptions/your-subscription-id/",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     dimensions=["ResourceType", "ResourceLocation"]
            ... )
        """
        return self.cost_client.get_cost_analysis(
            scope,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            dimensions=kwargs.get('dimensions')
        )
    
    def get_cost_trends(self, scope: str, **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost trends analysis with insights and patterns.

        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            start_date (Optional[str]): Start date for trend analysis (YYYY-MM-DD). Defaults to first day of current month.
            end_date (Optional[str]): End date for trend analysis (YYYY-MM-DD). Defaults to today.
            granularity (str, optional): Data granularity for trends ("Daily", "Monthly", etc.). Defaults to "Daily".

        Returns:
            Dict[str, Any]: Cost trends analysis with patterns, growth rates, and insights.
                {
                    "period": {"start": ..., "end": ...},
                    "granularity": ...,
                    "total_periods": ...,
                    "total_cost": ...,
                    "average_daily_cost": ...,
                    "cost_periods": [...],
                    "trend_direction": ...,
                    "growth_rate": ...,
                    "peak_periods": [...],
                    "low_periods": [...],
                    "patterns": [...],
                    "insights": [...]
                }

        Example:
            >>> azure.get_cost_trends(
            ...     "/subscriptions/your-subscription-id/",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="Daily"
            ... )
        """
        return self.cost_client.get_cost_trends(
            scope,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'Daily')
        )
    
    def get_resource_costs(self, scope: str, resource_id: str, **kwargs) -> Dict[str, Any]:
        """
        Get costs for a specific resource.

        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            resource_id (str): ID of the resource to get costs for.
            granularity (str, optional): Data granularity ("Daily", "Monthly", etc.).
            start_date (Optional[str]): Start date for cost data (YYYY-MM-DD).
            end_date (Optional[str]): End date for cost data (YYYY-MM-DD).
            metrics (Optional[str]): Cost metrics to retrieve.

        Returns:
            Dict[str, Any]: Resource cost data as returned by Azure Cost Management API.

        Example:
            >>> azure.get_resource_costs(
            ...     "/subscriptions/your-subscription-id/",
            ...     "/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.Compute/virtualMachines/your-vm",
            ...     granularity="Daily",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31"
            ... )
        """
        return self.cost_client.get_resource_costs(
            scope,
            resource_id,
            granularity=kwargs.get('granularity'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            metrics=kwargs.get('metrics')
        )
    
    def get_cost_forecast(self, scope, **kwargs) -> Dict[str, Any]:
        api_version = kwargs.get('api_version') or kwargs.get('api-version') or "2025-03-01"
        return self.analytics_client.get_cost_forecast(
            scope=scope,
            api_version=api_version,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            forecast_period=kwargs.get('forecast_period', 12),
            payload=kwargs.get('payload')
        )
    
    def get_cost_anomalies(self, scope: str, **kwargs) -> Dict[str, Any]:
        """
        Get cost anomalies using Azure Cost Management query API.
        
        This method uses the Azure Cost Management query API to analyze cost data
        and identify potential anomalies based on cost patterns and trends.

        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            start_date (str, optional): Start date for analysis (YYYY-MM-DD). Defaults to 30 days ago.
            end_date (str, optional): End date for analysis (YYYY-MM-DD). Defaults to today.
            api_version (str, optional): API version for the Cost Management API.
            payload (dict, optional): Custom payload for the query. If not provided, uses default payload.

        Returns:
            Dict[str, Any]: Cost analysis with potential anomalies identified.
        """
        return self.analytics_client.get_cost_anomalies(
            scope=scope,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            api_version=kwargs.get('api_version', '2023-03-01'),
            payload=kwargs.get('payload')
        )
    
    def get_cost_efficiency_metrics(self, scope: str, **kwargs) -> Dict[str, Any]:
        """
        Calculate real cost efficiency metrics from Azure Cost Management API.
        
        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            start_date (str, optional): Start date for analysis (YYYY-MM-DD). Defaults to first day of current month.
            end_date (str, optional): End date for analysis (YYYY-MM-DD). Defaults to today.
            user_count (int, optional): Number of users for cost per user calculation
            transaction_count (int, optional): Number of transactions for cost per transaction calculation
            api_version (str, optional): API version for the Cost Management API
            
        Returns:
            Dict[str, Any]: Cost efficiency metrics with detailed breakdown
        """
        return self.analytics_client.get_cost_efficiency_metrics(
            scope=scope,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            user_count=kwargs.get('user_count'),
            transaction_count=kwargs.get('transaction_count'),
            api_version=kwargs.get('api_version', '2023-03-01')
        )
    
    def generate_cost_report(self, scope: str, **kwargs) -> Dict[str, Any]:
        """
        Generate a comprehensive cost report for a given Azure scope.

        Args:
            scope (str): Azure scope (required). Examples:
                - Subscription: "/subscriptions/{subscription-id}/"
                - Resource Group: "/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/"
                - Billing Account: "/providers/Microsoft.Billing/billingAccounts/{billing-account-id}"
            report_type (str, optional): Type of report ("monthly", "quarterly", "annual"). Defaults to "monthly".
            start_date (str, optional): Start date for the report (YYYY-MM-DD). If not provided, defaults based on report_type.
            end_date (str, optional): End date for the report (YYYY-MM-DD). If not provided, defaults based on report_type.
            metrics (list, optional): List of cost metrics to aggregate (e.g., ["Cost"]).
            group_by (list, optional): List of dimensions to group by (e.g., ["ServiceName"]).
            filter_ (dict, optional): Additional filter criteria for the query.

        Returns:
            Dict[str, Any]: Cost report, including summary for quarterly/annual types and raw cost data as returned by Azure Cost Management API.
        """
        return self.analytics_client.generate_cost_report(
            scope=scope,
            report_type=kwargs.get('report_type', 'monthly'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            metrics=kwargs.get('metrics'),
            group_by=kwargs.get('group_by'),
            filter_=kwargs.get('filter_')
        )
    
    def get_governance_policies(self, **kwargs) -> Dict[str, Any]:
        """
        Get Azure governance policies and compliance status for cost management.

        This method returns a dictionary containing:
            - cost allocation by tags (costs grouped by supported Azure dimensions and available tags)
            - policy compliance status (focused on cost-related policies)
            - cost-related governance policies (filtered for FinOps relevance)

        Args:
            scope (str): Azure scope (subscription, resource group, etc.).
                Example: "/subscriptions/{subscription-id}/"
            tag_names (List[str], optional): List of tag names to use for cost allocation analysis.
                If not provided, all available tags will be used.

        Returns:
            Dict[str, Any]: Dictionary with keys:
                - 'cost_allocation_by_tags': Cost allocation analysis grouped by tags/dimensions
                - 'policy_compliance': Compliance status for cost-related policies
                - 'cost_policies': List of cost-related governance policies

        Example:
            >>> azure.get_governance_policies(
            ...     scope="/subscriptions/your-subscription-id/",
            ...     tag_names=["Environment", "Project"]
            ... )
        """
        scope = kwargs.get('scope')
        tag_names = kwargs.get('tag_names')
        return {
            'cost_allocation_by_tags': self.governance_client.get_costs_by_tags(scope, tag_names),
            'policy_compliance': self.governance_client.get_policy_compliance(scope=scope),
            'cost_policies': self.governance_client.get_cost_policies(scope=scope)
        }
    
    def get_costs_by_tags(self, scope: str, tag_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get costs grouped by tags for cost allocation analysis.
        
        If tag_names is not provided, this method will automatically discover
        available tags for the scope and use them for cost allocation.

        Args:
            scope (str): Azure scope (subscription, resource group, etc.)
            tag_names (Optional[List[str]]): List of tag names to group by. 
                If None, will automatically discover available tags.

        Returns:
            Dict[str, Any]: Cost data grouped by tag values and available tags

        Example:
            >>> # Use specific tags
            >>> azure.get_costs_by_tags(
            ...     scope="/subscriptions/your-subscription-id/",
            ...     tag_names=["Environment", "Project"]
            ... )
            
            >>> # Auto-discover and use available tags
            >>> azure.get_costs_by_tags(
            ...     scope="/subscriptions/your-subscription-id/"
            ... )
        """
        return self.governance_client.get_costs_by_tags(scope, tag_names)
    
    def get_reservation_order_details(self, **kwargs) -> Dict[str, Any]:
        """
        Get Azure reservation order details.

        This method retrieves details for all reservation orders in the Azure account,
        including metadata and properties for each reservation order.

        Args:
            api_version (str, optional): API version for the Azure Reservation API.
                Defaults to "2022-11-01".

        Returns:
            Dict[str, Any]: Reservation order details as returned by the Azure API.
                If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> azure.get_reservation_order_details()
            >>> azure.get_reservation_order_details(api_version="2022-11-01")
        """
        api_version = kwargs.get('api_version', '2022-11-01')
        return self.reservation_client.get_azure_reservation_order_details(api_version=api_version)
    
    def list_budgets(self, 
                     scope: str,
                     **kwargs) -> Dict[str, Any]:
        """
        List Azure budgets for a scope.

        Args:
            scope (str): Azure scope (subscription, resource group, etc.)
            **kwargs: Additional parameters including:
                - api_version (str): API version to use (default: '2024-08-01')

        Returns:
            Dict[str, Any]: List of budgets for the specified scope

        Raises:
            requests.exceptions.RequestException: If Azure API call fails

        Example:
            >>> azure.list_budgets(scope="/subscriptions/your-subscription-id/")
            >>> azure.list_budgets(scope="/subscriptions/your-subscription-id/resourceGroups/your-rg/")
            >>> azure.list_budgets(scope="/providers/Microsoft.Billing/billingAccounts/<billing_account_id>")

        """
        return self.budget_client.list_budgets(
            scope,
            api_version=kwargs.get('api_version', '2024-08-01')
        )
    
    def create_budget(self, 
                    budget_name: str,
                    amount: float,
                    scope: str,
                    notifications: List[Dict[str, Any]],
                    time_grain: str = "Monthly",
                    **kwargs) -> Dict[str, Any]:
        """
        Create a new Azure budget with notifications and thresholds.

        Args:
            budget_name (str): Name of the budget
            amount (float): Budget amount in the specified currency
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            notifications (List[Dict[str, Any]]): List of notification configurations
                Each dict must contain:
                - enabled (bool): Whether the notification is enabled
                - operator (str): Comparison operator (GreaterThan, GreaterThanOrEqualTo, LessThan, LessThanOrEqualTo)
                - threshold (float): Threshold percentage (0-100)
                - contactEmails (List[str]): List of email addresses to notify
                - contactRoles (Optional[List[str]]): List of contact roles (Owner, Contributor, Reader)
                - contactGroups (Optional[List[str]]): List of action group resource IDs
                - locale (Optional[str]): Locale for notifications (default: "en-us")
                - thresholdType (Optional[str]): Type of threshold (default: "Actual")
            time_grain (str): Time grain for the budget (Monthly, Quarterly, Annually)
            **kwargs: Additional parameters including:
                - start_date (Optional[str]): Start date for the budget in YYYY-MM-DD format. 
                  Will be automatically adjusted to the first day of the month if not already.
                - end_date (Optional[str]): End date for the budget in YYYY-MM-DD format.
                  Defaults to 5 years from start date if not provided.
                - api_version (str): API version to use for the Azure Budget API (default: '2024-08-01')

        Returns:
            Dict[str, Any]: Budget creation response from Azure

        Raises:
            requests.exceptions.RequestException: If Azure API call fails
            ValueError: If notifications are not properly configured

        Example:
            >>> azure.create_budget(
            ...     budget_name="monthly-budget",
            ...     amount=1000.0,
            ...     scope="/subscriptions/your-subscription-id/",
            ...     time_grain="Monthly",
            ...     notifications=[
            ...         {
            ...             "enabled": True,
            ...             "operator": "GreaterThan",
            ...             "threshold": 80.0,
            ...             "contactEmails": ["admin@example.com", "finance@example.com"]
            ...         }
            ...     ]
            ... )
        """
        return self.budget_client.create_budget(
            budget_name,
            amount,
            scope,
            notifications,
            time_grain,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            api_version=kwargs.get('api_version', '2024-08-01')
        )
    
    def get_budget(self, 
                   budget_name: str, 
                   scope: str, 
                   **kwargs) -> Dict[str, Any]:
        """
        Get a specific budget by name and scope.

        Args:
            budget_name (str): Name of the budget to retrieve
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            **kwargs: Additional parameters including:
                - api_version (str): API version to use (default: '2024-08-01')

        Returns:
            Dict[str, Any]: Budget details including notifications

        Raises:
            requests.exceptions.RequestException: If Azure API call fails

        Example:
            >>> azure.get_budget(budget_name="monthly-budget", scope="/subscriptions/your-subscription-id/")
        """
        return self.budget_client.get_budget(
            budget_name,
            scope,
            api_version=kwargs.get('api_version', '2024-08-01')
        )
    
    def get_advisor_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get Azure Advisor recommendations for cost optimization.

        Args:
            api_version (str, optional): API version for the Advisor API. Defaults to '2025-01-01'.
            filter (dict, optional): Filter dictionary to filter recommendations. Defaults to empty dict.

        Returns:
            Dict[str, Any]: Advisor recommendations
        """
        api_version = kwargs.get('api_version') or kwargs.get('api-version') or "2025-01-01"
        filter_arg = kwargs.get('filter', '')
        return self.optimization_client.get_advisor_recommendations(
            api_version=api_version,
            filter=filter_arg
        )
    
    def get_reserved_instance_recommendations(self, scope: str, **kwargs):
        """
        Get Azure Reserved Instance recommendations for a given scope.

        Args:
            scope (str): Azure scope string (e.g., "/subscriptions/{subscription-id}").
            api_version (str, optional): API version for the Reservation Recommendations API.
                Defaults to "2024-08-01" if not provided.
            filter (str, optional): OData filter string for server-side filtering
                (e.g., "ResourceGroup eq 'MyResourceGroup'").

        Returns:
            Dict[str, Any]: Reserved Instance recommendations (optionally filtered server-side).

        Example:
            >>> azure.get_reserved_instance_recommendations(
            ...     scope="/subscriptions/your-subscription-id",
            ...     filter="ResourceGroup eq 'MyResourceGroup'"
            ... )
        """
        api_version =kwargs.get('api_version') or kwargs.get('api-version') or "2024-08-01"
        filter_arg = kwargs.get('filter', '')
        return self.optimization_client.get_reserved_instance_recommendations(
            scope=scope,
            api_version=api_version,
            filter=filter_arg
        )
    
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations for Azure, including Advisor and Reserved Instance recommendations.

        Args:
            scope (str, required): Azure scope string (e.g., "/subscriptions/{subscription-id}").
            filter (str, optional): OData filter string to filter recommendations server-side (e.g., "Category eq 'Cost'").
                This filter will be applied to both Advisor and Reserved Instance recommendations.
            api_version (str, optional): (Not used directly, see below.)
                - Advisor recommendations always use API version '2025-01-01'.
                - Reserved Instance recommendations always use API version '2024-08-01'.

        Returns:
            Dict[str, Any]: Dictionary with keys:
                - 'advisor_recommendations': List of Azure Advisor recommendations (optionally filtered).
                - 'reserved_instance_recommendations': List of Reserved Instance recommendations (optionally filtered).

        Example:
            >>> azure.get_optimization_recommendations(
            ...     scope="/subscriptions/your-subscription-id",
            ...     filter="Category eq 'Cost'"
            ... )
        """
        return self.optimization_client.get_optimization_recommendations(**kwargs)


class GCPProvider(CloudProvider):
    def __init__(self, project_id: str, credentials_path: str):
        self.reservation_client = GCPReservationCost(project_id, credentials_path)
        self.budget_client = GCPBudgetManagement(project_id, credentials_path)
        self.cost_client = GCPCostManagement(project_id, credentials_path)
        self.optimization_client = GCPFinOpsOptimization(project_id, credentials_path)
        self.governance_client = GCPFinOpsGovernance(project_id, credentials_path)
        self.analytics_client = GCPFinOpsAnalytics(project_id, credentials_path)
    
    # Core FinOps Features
    def get_reservation_cost(self, **kwargs) -> Dict[str, Any]:
        """
        Get GCP reservation utilization and cost data.

        This method retrieves reservation utilization and cost data from GCP BigQuery,
        providing insights into how effectively your reservations are being used.

        Args:
            bq_project_id (str): BigQuery project ID for cost data analysis (required).
            bq_dataset (str): BigQuery dataset containing cost data (required).
            bq_table (str): BigQuery table containing cost data (required).
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to last day of current month.

        Returns:
            Dict[str, Any]: Reservation utilization data from GCP BigQuery including:
                - Reservation utilization metrics
                - Cost data for reservation period
                - Reservation order details
                - Individual reservation information
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> # Get reservation costs with BigQuery data
            >>> gcp.get_reservation_cost(
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data",
            ...     start_date="2024-06-01",
            ...     end_date="2024-06-30"
            ... )
        """
        return self.reservation_client.get_reservation_cost(
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
        )
    
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        """
        Get GCP reservation purchase recommendations.

        This method provides reservation purchase recommendations for various GCP services
        using BigQuery cost data, helping you identify cost optimization opportunities.

        Args:
            **kwargs: Additional parameters for reservation recommendations.

        Returns:
            Dict[str, Any]: Reservation purchase recommendations from GCP including:
                - Recommended reservation purchases
                - Potential savings estimates
                - Usage analysis data
                - Service-specific recommendations
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_reservation_recommendation()
        """
        return self.reservation_client.get_reservation_recommendation()
    
    def list_budgets(self, **kwargs) -> Dict[str, Any]:
        """
        List GCP budgets for a billing account.

        This method retrieves all budgets configured for the specified GCP billing account,
        including budget details and pagination information.

        Args:
            gcp_billing_account (str, optional): GCP billing account ID.
            gcp_max_results (int, optional): Maximum number of results to return.

        Returns:
            Dict[str, Any]: List of budgets and pagination information from GCP including:
                - Budgets: List of budget objects with details
                - NextPageToken: Token for pagination (if more results available)
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.list_budgets(
            ...     gcp_billing_account="012345-678901-ABCDEF",
            ...     gcp_max_results=10
            ... )
        """
        return self.budget_client.list_budgets(
            billing_account=kwargs.get('gcp_billing_account'),
            max_results=kwargs.get('gcp_max_results'),
        )
    
    def get_cost_data(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch GCP cost data for a given period and dimensions using BigQuery.

        This method retrieves cost data from GCP BigQuery for analysis and reporting.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            granularity (str, optional): Data granularity. One of "DAILY", "MONTHLY", or "HOURLY". Defaults to "MONTHLY".
            metrics (list, optional): List of cost metrics to aggregate. Defaults to ["cost"].
                Common values: "cost", "usage", "credits", etc.
            group_by (list, optional): List of grouping criteria for analysis.
            filter_ (dict, optional): Additional filter criteria for the query.
            bq_project_id (str): BigQuery project ID for cost data analysis.
            bq_dataset (str): BigQuery dataset containing cost data.
            bq_table (str): BigQuery table containing cost data.

        Returns:
            Dict[str, Any]: Cost data from GCP BigQuery. If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_cost_data(
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="MONTHLY",
            ...     metrics=["cost"],
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data"
            ... )
        """
        return self.cost_client.get_cost_data(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'Monthly'),
            metrics=kwargs.get('metrics'),
            group_by=kwargs.get('group_by'),
            filter_=kwargs.get('filter_'),
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table')
        )
    
    def get_cost_analysis(self, 
                        bq_project_id: str, 
                        bq_dataset: str, 
                        bq_table: str,
                        **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost analysis with insights and breakdowns for GCP.

        This method provides comprehensive cost analysis including cost breakdowns by service,
        top services by cost, cost trends, and actionable insights using BigQuery data.

        Args:
            bq_project_id (str): BigQuery project ID for cost data analysis (required).
            bq_dataset (str): BigQuery dataset containing cost data (required).
            bq_table (str): BigQuery table containing cost data (required).
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.

        Returns:
            Dict[str, Any]: Cost analysis with insights, breakdowns, and trends.
                {
                    "period": {"start": ..., "end": ...},
                    "total_cost": ...,
                    "cost_breakdown": {...},
                    "top_services": [...],
                    "cost_trends": [...],
                    "insights": [...]
                }
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_cost_analysis(
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31"
            ... )
        """
        return self.cost_client.get_cost_analysis(
            bq_project_id=bq_project_id,
            bq_dataset=bq_dataset,
            bq_table=bq_table,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
        )
    
    def get_cost_trends(self, 
                        bq_project_id: str, 
                        bq_dataset: str, 
                        bq_table: str,
                        **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost trends analysis with insights and patterns for GCP.

        This method provides comprehensive cost trend analysis including growth rates,
        peak periods, patterns, and actionable insights using BigQuery data.

        Args:
            bq_project_id (str): BigQuery project ID for cost data analysis (required).
            bq_dataset (str): BigQuery dataset containing cost data (required).
            bq_table (str): BigQuery table containing cost data (required).
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            granularity (str, optional): Data granularity. One of "DAILY", "MONTHLY", or "HOURLY". Defaults to "DAILY".

        Returns:
            Dict[str, Any]: Cost trends analysis with patterns, growth rates, and insights.
                {
                    "period": {"start": ..., "end": ...},
                    "granularity": ...,
                    "total_periods": ...,
                    "total_cost": ...,
                    "average_daily_cost": ...,
                    "cost_periods": [...],
                    "trend_direction": ...,
                    "growth_rate": ...,
                    "peak_periods": [...],
                    "low_periods": [...],
                    "patterns": [...],
                    "insights": [...]
                }
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_cost_trends(
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="DAILY"
            ... )
        """
        return self.cost_client.get_cost_trends(
            bq_project_id=bq_project_id,
            bq_dataset=bq_dataset,
            bq_table=bq_table,            
            **kwargs
        )
    
    def get_resource_costs(self, 
                           resource_name: str, 
                           bq_project_id: str, 
                           bq_dataset: str, 
                           bq_table: str,
                           **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost analysis for a specific GCP resource.

        This method provides comprehensive cost analysis for a specific resource including
        cost breakdowns, utilization insights, and optimization recommendations using BigQuery data.

        Args:
            resource_name (str): Name of the resource to get costs for (required).
            bq_project_id (str): BigQuery project ID for cost data analysis (required).
            bq_dataset (str): BigQuery dataset containing cost data (required).
            bq_table (str): BigQuery table containing cost data (required).
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            granularity (str, optional): Data granularity. One of "DAILY", "MONTHLY", or "HOURLY". Defaults to "DAILY".

        Returns:
            Dict[str, Any]: Detailed resource cost analysis with insights and breakdowns.
                {
                    "resource_name": ...,
                    "resource_type": ...,
                    "period": {"start": ..., "end": ...},
                    "granularity": ...,
                    "total_cost": ...,
                    "total_periods": ...,
                    "active_periods": ...,
                    "cost_periods": [...],
                    "cost_breakdown": {...},
                    "utilization_insights": [...],
                    "cost_trends": [...],
                    "recommendations": [...]
                }
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_resource_costs(
            ...     resource_name="instance-1",
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     granularity="DAILY"
            ... )
        """
        return self.cost_client.get_resource_costs(
            resource_name=resource_name,
            bq_project_id=bq_project_id,
            bq_dataset=bq_dataset,
            bq_table=bq_table,
            **kwargs
        )
    
    # Advanced FinOps Features
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations for GCP.

        This method provides optimization recommendations including machine type recommendations,
        idle resource recommendations, and other cost optimization suggestions.

        Args:
            **kwargs: Additional parameters for specific optimization types.

        Returns:
            Dict[str, Any]: Optimization recommendations including:
                - 'machine_type_recommendations': Machine type optimization recommendations
                - 'idle_resource_recommendations': Idle resource recommendations
                - 'cost_optimization_suggestions': General cost optimization suggestions
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_optimization_recommendations()
        """
        return self.optimization_client.get_optimization_recommendations()
    
    def get_cost_forecast(self, **kwargs) -> Dict[str, Any]:
        """
        Get cost forecast for the specified period using GCP BigQuery ML.

        This method provides cost forecasting capabilities using BigQuery ML with support for various
        parameters and ensures required parameters are present with sensible defaults.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            forecast_period (int, optional): Number of periods to forecast. Defaults to 12.
            bq_project_id (str): BigQuery project ID for cost data analysis.
            bq_dataset (str): BigQuery dataset containing cost data.
            bq_table (str): BigQuery table containing cost data.

        Returns:
            Dict[str, Any]: Cost forecast data from GCP BigQuery ML including:
                - Forecasted cost values
                - Confidence intervals
                - Forecast period details
                - Model performance metrics
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_cost_forecast(
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     forecast_period=12,
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data"
            ... )
        """
        return self.analytics_client.get_cost_forecast_bqml(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            forecast_period=kwargs.get('forecast_period', 12),
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table')
        )
    
    def get_cost_anomalies(self, **kwargs) -> Dict[str, Any]:
        """
        Get cost anomalies using GCP BigQuery ML.

        This method identifies cost anomalies using BigQuery ML with support for various parameters
        and ensures required parameters are present with sensible defaults.

        Args:
            bq_project_id (str): BigQuery project ID for cost data analysis.
            bq_dataset (str): BigQuery dataset containing cost data.
            bq_table (str): BigQuery table containing cost data.
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to 30 days ago.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            anomaly_prob_threshold (float, optional): Probability threshold for anomaly detection. Defaults to 0.95.

        Returns:
            Dict[str, Any]: Cost anomalies data from GCP BigQuery ML including:
                - Detected anomalies with timestamps
                - Anomaly scores and probabilities
                - Anomaly details and context
                - Model performance metrics
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_cost_anomalies(
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     anomaly_prob_threshold=0.95
            ... )
        """
        return self.analytics_client.get_cost_anomalies(
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            anomaly_prob_threshold=kwargs.get('anomaly_prob_threshold'),
        )
    
    def get_cost_efficiency_metrics(self, **kwargs) -> Dict[str, Any]:
        """
        Calculate cost efficiency metrics from GCP BigQuery.

        This method calculates real cost efficiency metrics with support for various
        parameters and ensures required parameters are present with sensible defaults.

        Args:
            bq_project_id (str): BigQuery project ID for cost data analysis.
            bq_dataset (str): BigQuery dataset containing cost data.
            bq_table (str): BigQuery table containing cost data.
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.
            use_ml (bool, optional): Whether to use ML for enhanced metrics calculation. Defaults to False.

        Returns:
            Dict[str, Any]: Cost efficiency metrics including:
                - 'total_cost': Total cost for the period
                - 'cost_by_service': Cost breakdown by service
                - 'waste_estimate': Estimated waste cost
                - 'efficiency_score': Overall cost efficiency score
                - 'optimization_opportunities': Identified optimization opportunities
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_cost_efficiency_metrics(
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     use_ml=True
            ... )
        """
        return self.analytics_client.get_cost_efficiency_metrics(
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            use_ml=kwargs.get('use_ml')
        )
    
    def generate_cost_report(self, **kwargs) -> Dict[str, Any]:
        """
        Generate comprehensive cost report using GCP BigQuery.

        This method generates comprehensive cost reports with support for various
        parameters and ensures required parameters are present with sensible defaults.

        Args:
            bq_project_id (str): BigQuery project ID for cost data analysis.
            bq_dataset (str): BigQuery dataset containing cost data.
            bq_table (str): BigQuery table containing cost data.
            report_type (str, optional): Type of report (monthly, quarterly, annual). Defaults to "monthly".
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today's date.

        Returns:
            Dict[str, Any]: Comprehensive cost report including:
                - 'report_type': Type of report generated
                - 'period': Time period covered
                - 'total_cost': Total cost for the period
                - 'cost_by_service': Cost breakdown by service
                - 'cost_trends': Cost trends over time
                - 'recommendations': Cost optimization recommendations
                - 'generated_at': Timestamp of report generation
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.generate_cost_report(
            ...     bq_project_id="your-project-id",
            ...     bq_dataset="billing_data",
            ...     bq_table="cost_data",
            ...     report_type="monthly",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31"
            ... )
        """
        return self.analytics_client.generate_cost_report(
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table'),
            report_type=kwargs.get('report_type', 'monthly'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
        )
    
    def get_governance_policies(self, **kwargs) -> Dict[str, Any]:
        """
        Get governance policies and compliance status for GCP.

        This method retrieves cost allocation labels, compliance status, and cost-related policies.

        Args:
            **kwargs: Additional parameters for governance policies.

        Returns:
            Dict[str, Any]: Governance policies and compliance information including:
                - 'cost_policies': Cost-related governance policies
                - 'compliance_status': Compliance status for cost policies
                - 'cost_allocation_labels': Cost allocation labels (if available)
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_governance_policies()
        """
        return {
            'cost_allocation_labels': self.governance_client.get_cost_allocation_tags(**kwargs),
            'policy_compliance': self.governance_client.get_policy_compliance(**kwargs),
            'cost_policies': self.governance_client.get_cost_policies(**kwargs)
        }
    
    def create_budget(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new GCP budget.

        This method creates a budget in GCP for the specified billing account, with support for
        custom budget amounts and currency codes.

        Args:
            billing_account (str, optional): GCP billing account ID.
            budget_name (str, optional): Name of the budget. Defaults to "pycloudmesh_budget".
            amount (float, optional): Budget amount. Defaults to 1.
            currency_code (str, optional): Currency code for the budget. Defaults to "USD".

        Returns:
            Dict[str, Any]: GCP response for budget creation. If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.create_budget(
            ...     billing_account="012345-678901-ABCDEF",
            ...     budget_name="monthly-budget",
            ...     amount=1000.0,
            ...     currency_code="USD"
            ... )
        """
        return self.budget_client.create_budget(
            billing_account=kwargs.get('billing_account'),
            budget_name=kwargs.get('budget_name', 'pycloudmesh_budget'),
            amount=kwargs.get('amount', 1),
            currency_code=kwargs.get('currency_code', 'USD')
        )
    
    def get_budget_alerts(self, **kwargs) -> Dict[str, Any]:
        """
        Get alerts for a specific GCP budget.

        This method retrieves all alerts configured for a specific budget.

        Args:
            billing_account (str, optional): GCP billing account ID.
            budget_display_name (str, optional): Display name of the budget.

        Returns:
            Dict[str, Any]: Budget alerts from GCP. If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_budget_alerts(
            ...     billing_account="012345-678901-ABCDEF",
            ...     budget_display_name="monthly-budget"
            ... )
        """
        return self.budget_client.get_budget_alerts(
            billing_account=kwargs.get('billing_account'),
            budget_display_name=kwargs.get('budget_display_name')
        )
    
    def get_machine_type_recommendations(self) -> Dict[str, Any]:
        """
        Get GCP machine type recommendations.

        This method provides machine type optimization recommendations for Compute Engine instances.

        Returns:
            Dict[str, Any]: Machine type recommendations from GCP.
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_machine_type_recommendations()
        """
        return self.optimization_client.get_machine_type_recommendations()
    
    def get_idle_resource_recommendations(self) -> Dict[str, Any]:
        """
        Get GCP idle resource recommendations.

        This method identifies idle or underutilized resources that could be stopped or downsized.

        Returns:
            Dict[str, Any]: Idle resource recommendations from GCP.
            If the API call fails, returns a dictionary with an "error" key and message.

        Example:
            >>> gcp.get_idle_resource_recommendations()
        """
        return self.optimization_client.get_idle_resource_recommendations()


class CloudMesh:
    """
    CloudMesh provides a unified interface for comprehensive FinOps features
    across AWS, Azure, and GCP.
    """
    
    PROVIDERS = {
        'aws': AWSProvider,
        'azure': AzureProvider,
        'gcp': GCPProvider
    }
    
    def __init__(self, provider: str, **kwargs):
        """
        Initializes CloudMesh based on the selected cloud provider.

        AWS requires access_key, secret_key, region
        Azure requires subscription_id and token
        GCP requires project_id, credentials_path

        :param provider: Cloud provider ("aws", "azure", or "gcp").
        :param kwargs: Provider-specific authentication details.
        :raises ValueError: If provider is not supported or required parameters are missing.
        """
        self.provider = provider.lower()
        
        if self.provider not in self.PROVIDERS:
            raise ValueError(f"Unsupported cloud provider: {provider}. Supported providers: {', '.join(self.PROVIDERS.keys())}")
        
        try:
            self._provider = self.PROVIDERS[self.provider](**kwargs)
        except TypeError as e:
            raise ValueError(f"Missing required parameters for {provider}: {str(e)}")
    
    # Core FinOps Features
    @lru_cache(maxsize=128)
    def get_reservation_cost(self, **kwargs) -> Dict[str, Any]:
        """Fetch reservation cost for the selected cloud provider."""
        return self._provider.get_reservation_cost(**kwargs)
    
    @lru_cache(maxsize=128)
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        """Fetch reservation recommendation for the selected cloud provider."""
        return self._provider.get_reservation_recommendation(**kwargs)
    
    def list_budgets(self, **kwargs) -> Dict[str, Any]:
        """Fetch budget details for the selected cloud provider."""
        return self._provider.list_budgets(**kwargs)
    
    def get_cost_data(self, **kwargs) -> Dict[str, Any]:
        """Fetch cost data for the selected cloud provider."""
        return self._provider.get_cost_data(**kwargs)
    
    def get_cost_analysis(self, **kwargs) -> Dict[str, Any]:
        """Fetch detailed cost analysis for the selected cloud provider."""
        return self._provider.get_cost_analysis(**kwargs)
    
    def get_cost_trends(self, **kwargs) -> Dict[str, Any]:
        """Fetch cost trends for the selected cloud provider."""
        return self._provider.get_cost_trends(**kwargs)
    
    def get_resource_costs(self, resource_id: str, **kwargs) -> Dict[str, Any]:
        """Fetch costs for a specific resource."""
        return self._provider.get_resource_costs(resource_id, **kwargs)
    
    # Advanced FinOps Features
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        """Get comprehensive optimization recommendations."""
        return self._provider.get_optimization_recommendations(**kwargs)
    
    def get_cost_forecast(self, **kwargs) -> Dict[str, Any]:
        """Get cost forecast for the specified period."""
        return self._provider.get_cost_forecast(**kwargs)
    
    def get_cost_anomalies(self, **kwargs) -> Dict[str, Any]:
        """Get cost anomalies."""
        return self._provider.get_cost_anomalies(**kwargs)
    
    def get_cost_efficiency_metrics(self, **kwargs) -> Dict[str, Any]:
        """Get cost efficiency metrics."""
        return self._provider.get_cost_efficiency_metrics(**kwargs)
    
    def generate_cost_report(self, **kwargs) -> Dict[str, Any]:
        """Generate comprehensive cost report."""
        return self._provider.generate_cost_report(**kwargs)
    
    def get_governance_policies(self, **kwargs) -> Dict[str, Any]:
        """Get governance policies and compliance status."""
        return self._provider.get_governance_policies(**kwargs)
    
    # Provider-specific methods
    def get_azure_reservation_order_details(self) -> Dict[str, Any]:
        """Fetch reservation order details (Only available for Azure)."""
        if not isinstance(self._provider, AzureProvider):
            raise AttributeError("get_azure_reservation_order_details() is only available for Azure.")
        return self._provider.get_reservation_order_details()


# Individual Client Factory Functions
def create_aws_client(access_key: str, secret_key: str, region: str):
    """
    Create an AWS client with all FinOps capabilities.
    
    Args:
        access_key (str): AWS access key ID
        secret_key (str): AWS secret access key
        region (str): AWS region name
    
    Returns:
        AWSProvider: AWS client with comprehensive FinOps features
    """
    return AWSProvider(access_key, secret_key, region)


def create_azure_client(subscription_id: str, token: str):
    """
    Create an Azure client with all FinOps capabilities.
    
    Args:
        subscription_id (str): Azure subscription ID
        token (str): Azure authentication token
    
    Returns:
        AzureProvider: Azure client with comprehensive FinOps features
    """
    return AzureProvider(subscription_id, token)


def create_gcp_client(project_id: str, credentials_path: str):
    """
    Create a GCP client with all FinOps capabilities.
    
    Args:
        project_id (str): GCP project ID
        credentials_path (str): Path to GCP service account credentials file
    
    Returns:
        GCPProvider: GCP client with comprehensive FinOps features
    """
    return GCPProvider(project_id, credentials_path)


# Convenience aliases for direct client access
def aws_client(access_key: str, secret_key: str, region: str):
    """
    Create an AWS client - alias for create_aws_client.
    
    Example:
        client = aws_client("your_access_key", "your_secret_key", "us-east-1")
        budgets = client.list_budgets(aws_account_id="123456789012")
        optimizations = client.get_optimization_recommendations()
    """
    return create_aws_client(access_key, secret_key, region)


def azure_client(subscription_id: str, token: str):
    """
    Create an Azure client - alias for create_azure_client.
    
    Example:
        client = azure_client("your_subscription_id", "your_token")
        budgets = client.list_budgets(azure_scope="subscriptions/your_subscription_id")
        optimizations = client.get_optimization_recommendations()
    """
    return create_azure_client(subscription_id, token)


def gcp_client(project_id: str, credentials_path: str):
    """
    Create a GCP client - alias for create_gcp_client.
    
    Example:
        client = gcp_client("your_project_id", "/path/to/credentials.json")
        budgets = client.list_budgets()
        optimizations = client.get_optimization_recommendations()
    """
    return create_gcp_client(project_id, credentials_path)
