from typing import Optional, Dict, Any, Union
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
    def get_reservation_cost(self) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_cost()
    
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_recommendation()
    
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
        return self.cost_client.get_aws_cost_trends(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'DAILY')
        )
    
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
            'cost_allocation_tags': self.governance_client.get_cost_allocation_tags(),
            'compliance_status': self.governance_client.get_compliance_status(),
            'cost_policies': self.governance_client.get_cost_policies()
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
    
    def list_budgets(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.list_budgets(
            scope=kwargs.get('azure_scope'),
            api_version=kwargs.get('api_version', '2024-08-01')
        )
    
    def get_cost_data(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_cost_data(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'Monthly'),
            metrics=kwargs.get('metrics'),
            group_by=kwargs.get('group_by'),
            filter_=kwargs.get('filter_')
        )
    
    def get_cost_analysis(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_cost_analysis(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            dimensions=kwargs.get('dimensions')
        )
    
    def get_cost_trends(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_cost_trends(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'Daily')
        )
    
    def get_resource_costs(self, resource_id: str, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_resource_costs(
            resource_id=resource_id,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date')
        )
    
    # Advanced FinOps Features
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client.get_optimization_recommendations()
    
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
            'cost_allocation_tags': self.governance_client.get_cost_allocation_tags(),
            'policy_compliance': self.governance_client.get_policy_compliance(),
            'cost_policies': self.governance_client.get_cost_policies()
        }
    
    # Azure-specific additional methods
    def get_reservation_order_details(self) -> Dict[str, Any]:
        return self.reservation_client.get_azure_reservation_order_details()
    
    def create_budget(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.create_budget(
            budget_name=kwargs.get('budget_name'),
            amount=kwargs.get('budget_amount'),
            scope=kwargs.get('azure_scope'),
            time_grain=kwargs.get('time_grain', 'Monthly'),
            start_date=kwargs.get('start_date')
        )
    
    def get_budget_alerts(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.get_budget_alerts(
            budget_name=kwargs.get('budget_name')
        )
    
    def get_advisor_recommendations(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client.get_advisor_recommendations()


class GCPProvider(CloudProvider):
    def __init__(self, project_id: str, credentials_path: str):
        self.reservation_client = GCPReservationCost(project_id, credentials_path)
        self.budget_client = GCPBudgetManagement(project_id, credentials_path)
        self.cost_client = GCPCostManagement(project_id, credentials_path)
        self.optimization_client = GCPFinOpsOptimization(project_id, credentials_path)
        self.governance_client = GCPFinOpsGovernance(project_id, credentials_path)
        self.analytics_client = GCPFinOpsAnalytics(project_id, credentials_path)
    
    # Core FinOps Features
    def get_reservation_cost(self) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_cost()
    
    def get_reservation_recommendation(self, **kwargs) -> Dict[str, Any]:
        return self.reservation_client.get_reservation_recommendation()
    
    def list_budgets(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.list_budgets(
            billing_account=kwargs.get('gcp_billing_account'),
            max_results=kwargs.get('gcp_max_results')
        )
    
    def get_cost_data(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_cost_data(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'Monthly'),
            metrics=kwargs.get('metrics'),
            group_by=kwargs.get('group_by'),
            filter_=kwargs.get('filter_')
        )
    
    def get_cost_analysis(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_cost_analysis(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            dimensions=kwargs.get('dimensions')
        )
    
    def get_cost_trends(self, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_cost_trends(
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date'),
            granularity=kwargs.get('granularity', 'Daily')
        )
    
    def get_resource_costs(self, resource_id: str, **kwargs) -> Dict[str, Any]:
        return self.cost_client.get_resource_costs(
            resource_id=resource_id,
            start_date=kwargs.get('start_date'),
            end_date=kwargs.get('end_date')
        )
    
    # Advanced FinOps Features
    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        return self.optimization_client.get_optimization_recommendations()
    
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
            'cost_allocation_labels': self.governance_client.get_cost_allocation_tags(),
            'policy_compliance': self.governance_client.get_policy_compliance(),
            'cost_policies': self.governance_client.get_cost_policies()
        }
    
    # GCP-specific additional methods
    def create_budget(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.create_budget(
            billing_account=kwargs.get('gcp_billing_account'),
            budget_name=kwargs.get('budget_name'),
            amount=kwargs.get('budget_amount'),
            currency_code=kwargs.get('currency_code', 'USD')
        )
    
    def get_budget_alerts(self, **kwargs) -> Dict[str, Any]:
        return self.budget_client.get_budget_alerts(
            budget_name=kwargs.get('budget_name')
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
    def get_reservation_cost(self) -> Dict[str, Any]:
        """Fetch reservation cost for the selected cloud provider."""
        return self._provider.get_reservation_cost()
    
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
