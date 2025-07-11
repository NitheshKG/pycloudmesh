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
        return self.reservation_client.get_reservation_cost(**kwargs)
    
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_recommendation(**kwargs)
    
    def get_reservation_coverage(self, **kwargs) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_coverage(**kwargs)
    
    def list_budgets(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.list_budgets(
            kwargs.get('aws_account_id'),
            max_results=kwargs.get('aws_max_results'),
            next_token=kwargs.get('aws_next_token')
        )
    
    def get_cost_data(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_aws_cost_data(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'MONTHLY'),
            metrics=kwargs.get('metrics'),
            group_by=kwargs.get('group_by'),
            filter_=kwargs.get('filter_')
        )
    
    def get_cost_analysis(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_aws_cost_analysis(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            dimensions=kwargs.get('dimensions')
        )
    
    def get_cost_trends(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_aws_cost_trends(**kwargs)
    
    def get_resource_costs(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_aws_resource_costs(
            resource_id=kwargs.get('resource_id'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'DAILY')
        )
    
    # Advanced FinOps Features
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client.get_optimization_recommendations()
    
    def get_cost_forecast(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_forecast(**kwargs)
    
    def get_cost_anomalies(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_anomalies(**kwargs)
    
    def get_cost_efficiency_metrics(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_efficiency_metrics(**kwargs)
    
    def generate_cost_report(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.generate_cost_report(**kwargs)
    
    def get_governance_policies(self, **kwargs) -> Dict[str, Any]:
        return {
            'cost_allocation_tags': self.governance_client.get_cost_allocation_tags(**kwargs),
            'compliance_status': self.governance_client.get_compliance_status(**kwargs),
            'cost_policies': self.governance_client.get_cost_policies(**kwargs)
        }
    
    # AWS-specific additional methods
    def create_budget(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.create_budget(
            account_id=kwargs.get('aws_account_id'),
            budget_name=kwargs.get('budget_name'),
            budget_amount=kwargs.get('budget_amount'),
            budget_type=kwargs.get('budget_type', 'COST'),
            time_unit=kwargs.get('time_unit', 'MONTHLY'),
            notifications_with_subscribers=kwargs.get('notifications_with_subscribers')
        )
    
    def get_budget_notifications(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.get_budget_notifications(
            account_id=kwargs.get('aws_account_id'),
            budget_name=kwargs.get('budget_name')
        )
    
    def get_savings_plans_recommendations(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client._get_savings_plans_recommendations(**kwargs)
    
    def get_rightsizing_recommendations(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client._get_rightsizing_recommendations(**kwargs)
    
    def get_idle_resources(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client.get_idle_resources(**kwargs)
    
    def get_reservation_purchase_recommendations(self, **kwargs) -> Dict[str, Any]:
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
    def get_reservation_cost(self) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_cost()
    
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_recommendation(kwargs.get('subscription_id'))
    
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
    
    def get_cost_forecast(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_forecast(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            forecast_period=kwargs.get('forecast_period', 12)
        )
    
    def get_cost_anomalies(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_anomalies()
    
    def get_cost_efficiency_metrics(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_efficiency_metrics()
    
    def generate_cost_report(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.generate_cost_report(
            report_type=kwargs.get('report_type', 'monthly'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date')
        )
    
    def get_governance_policies(self, **kwargs) -> Dict[str, Any]:
        return {
            'cost_allocation_tags': self.governance_client.get_cost_allocation_tags(**kwargs),
            'policy_compliance': self.governance_client.get_policy_compliance(**kwargs),
            'cost_policies': self.governance_client.get_cost_policies(**kwargs)
        }
    
    # Azure-specific additional methods
    def get_reservation_order_details(self) -> Dict[str, Any]:
        return self.reservation_client.get_azure_reservation_order_details()
    
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
        return self.reservation_client.get_reservation_cost(
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
        )
    
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_recommendation()
    
    def list_budgets(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.list_budgets(
            billing_account=kwargs.get('gcp_billing_account'),
            max_results=kwargs.get('gcp_max_results'),
        )
    
    def get_cost_data(self, **kwargs) -> Dict[str, Any]:
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
        return self.cost_client.get_resource_costs(
            resource_name=resource_name,
            bq_project_id=bq_project_id,
            bq_dataset=bq_dataset,
            bq_table=bq_table,
            **kwargs
        )
    
    # Advanced FinOps Features
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client.get_optimization_recommendations()
    
    def get_cost_forecast(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_forecast_bqml(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            forecast_period=kwargs.get('forecast_period', 12),
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table')
        )
    
    def get_cost_anomalies(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_anomalies(
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            anomaly_prob_threshold=kwargs.get('anomaly_prob_threshold'),
        )
    
    def get_cost_efficiency_metrics(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.get_cost_efficiency_metrics(
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            use_ml=kwargs.get('use_ml')
        ) 
    
    def generate_cost_report(self, **kwargs) -> Dict[str, Any]:
        return self.analytics_client.generate_cost_report(
            bq_project_id=kwargs.get('bq_project_id'),
            bq_dataset=kwargs.get('bq_dataset'),
            bq_table=kwargs.get('bq_table'),
            report_type=kwargs.get('report_type', 'monthly'),
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
        )
    
    def get_governance_policies(self, **kwargs) -> Dict[str, Any]:
        return {
            # 'cost_allocation_labels': self.governance_client.get_cost_allocation_tags(**kwargs),
            # 'policy_compliance': self.governance_client.get_policy_compliance(**kwargs),
            'cost_policies': self.governance_client.get_cost_policies(**kwargs)
        }
    
    # GCP-specific additional methods
    def create_budget(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.create_budget(
            billing_account=kwargs.get('billing_account'),
            budget_name=kwargs.get('budget_name', 'pycloudmesh_budget'),
            amount=kwargs.get('amount', 1),
            currency_code=kwargs.get('currency_code', 'USD')
        )
    
    def get_budget_alerts(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.get_budget_alerts(
            billing_account=kwargs.get('billing_account'),
            budget_display_name=kwargs.get('budget_display_name')
        )
    
    def get_machine_type_recommendations(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client.get_machine_type_recommendations()
    
    def get_idle_resource_recommendations(self, **kwargs) -> Dict[str, Any]:
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
