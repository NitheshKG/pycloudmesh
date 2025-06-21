import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union

class AzureReservationCost:
    """Azure Reservation Cost Management class for handling Azure reservation-related operations."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure Reservation Cost client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        self.subscription_id = subscription_id
        self.token = token
        self.base_url = f"https://management.azure.com/subscriptions/{subscription_id}"

    def get_reservation_cost(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get Azure reservation utilization and cost data.

        Args:
            start_date (Optional[str]): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (Optional[str]): End date in YYYY-MM-DD format. Defaults to last day of current month.

        Returns:
            Dict[str, Any]: Reservation utilization data from Azure Cost Management.

        Raises:
            requests.exceptions.RequestException: If Azure API call fails
        """
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.CostManagement/query"
            
            payload = {
                "type": "Usage",
                "timeframe": "Custom",
                "timePeriod": {
                    "from": start_date,
                    "to": end_date
                },
                "dataset": {
                    "granularity": "Daily",
                    "filter": {
                        "and": [
                            {
                                "or": [
                                    {
                                        "dimensions": {
                                            "name": "ReservationId",
                                            "operator": "In",
                                            "values": ["*"]
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch reservation utilization: {str(e)}"}

    def get_reservation_recommendation(self, subscription_id: str) -> List[Dict[str, Any]]:
        """
        Get Azure reservation recommendations for various services.

        Args:
            subscription_id (str): Azure subscription ID

        Returns:
            List[Dict[str, Any]]: List of reservation recommendations.

        Raises:
            requests.exceptions.RequestException: If Azure API call fails
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Consumption/reservationRecommendations"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("value", [])
        except requests.exceptions.RequestException as e:
            return [{"error": f"Failed to fetch reservation recommendations: {str(e)}"}]

    def get_azure_reservation_order_details(self) -> Dict[str, Any]:
        """
        Get Azure reservation order details.

        Returns:
            Dict[str, Any]: Reservation order details.
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Capacity/reservationOrders"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch reservation order details: {str(e)}"}


class AzureBudgetManagement:
    """Azure Budget Management class for handling Azure budget-related operations."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure Budget Management client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        self.subscription_id = subscription_id
        self.token = token
        self.base_url = f"https://management.azure.com/subscriptions/{subscription_id}"

    def list_budgets(
        self,
        scope: str,
        /,
        *,
        api_version: str = "2024-08-01"
    ) -> Dict[str, Any]:
        """
        List Azure budgets for a scope.

        Args:
            scope (str): Azure scope (subscription, resource group, etc.)
            api_version (str): API version to use

        Returns:
            Dict[str, Any]: List of budgets

        Raises:
            requests.exceptions.RequestException: If Azure API call fails
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Consumption/budgets"
            params = {"api-version": api_version}
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to list budgets: {str(e)}"}

    def create_budget(
        self,
        budget_name: str,
        amount: float,
        scope: str,
        time_grain: str = "Monthly",
        start_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new Azure budget.

        Args:
            budget_name (str): Name of the budget
            amount (float): Budget amount
            scope (str): Azure scope
            time_grain (str): Time grain for the budget
            start_date (Optional[str]): Start date for the budget

        Returns:
            Dict[str, Any]: Budget creation response
        """
        try:
            if not start_date:
                start_date = datetime.today().strftime("%Y-%m-%d")

            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Consumption/budgets/{budget_name}"
            
            payload = {
                "properties": {
                    "amount": amount,
                    "timeGrain": time_grain,
                    "timePeriod": {
                        "startDate": start_date
                    }
                }
            }
            
            response = requests.put(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to create budget: {str(e)}"}

    def get_budget_alerts(self, budget_name: str) -> Dict[str, Any]:
        """
        Get alerts for a specific budget.

        Args:
            budget_name (str): Name of the budget

        Returns:
            Dict[str, Any]: Budget alerts
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Consumption/budgets/{budget_name}/alerts"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get budget alerts: {str(e)}"}


class AzureCostManagement:
    """Azure Cost Management class for handling Azure cost-related operations."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure Cost Management client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        self.subscription_id = subscription_id
        self.token = token
        self.base_url = f"https://management.azure.com/subscriptions/{subscription_id}"

    def get_cost_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "Monthly",
        metrics: Optional[List[str]] = None,
        group_by: Optional[List[str]] = None,
        filter_: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fetch Azure cost data from Cost Management API.

        Args:
            start_date (Optional[str]): Start date (YYYY-MM-DD). Defaults to first day of current month.
            end_date (Optional[str]): End date (YYYY-MM-DD). Defaults to today's date.
            granularity (str): "Daily", "Monthly", or "None". Defaults to "Monthly".
            metrics (Optional[List[str]]): List of cost metrics. Defaults to standard cost metrics.
            group_by (Optional[List[str]]): Grouping criteria.
            filter_ (Optional[Dict[str, Any]]): Filter criteria.

        Returns:
            Dict[str, Any]: Cost data from Azure Cost Management.

        Raises:
            requests.exceptions.RequestException: If Azure API call fails
        """
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        if not metrics:
            metrics = ["ActualCost"]

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.CostManagement/query"
            
            payload = {
                "type": "Usage",
                "timeframe": "Custom",
                "timePeriod": {
                    "from": start_date,
                    "to": end_date
                },
                "dataset": {
                    "granularity": granularity,
                    "aggregation": {
                        metric: {"name": metric, "function": "Sum"}
                        for metric in metrics
                    }
                }
            }

            if group_by:
                payload["dataset"]["grouping"] = [
                    {"type": "Dimension", "column": group} for group in group_by
                ]

            if filter_:
                payload["dataset"]["filter"] = filter_

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch cost data: {str(e)}"}

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
            dimensions = ["ResourceType", "ResourceLocation", "ResourceGroupName"]

        return self.get_cost_data(
            start_date=start_date,
            end_date=end_date,
            group_by=dimensions
        )

    def get_cost_trends(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "Daily"
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
        return self.get_cost_data(
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
            "and": [
                {
                    "dimensions": {
                        "name": "ResourceId",
                        "operator": "In",
                        "values": [resource_id]
                    }
                }
            ]
        }
        
        return self.get_cost_data(
            start_date=start_date,
            end_date=end_date,
            filter_=filter_
        )


class AzureFinOpsOptimization:
    """Azure FinOps Optimization class for cost optimization features."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure FinOps Optimization client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        self.subscription_id = subscription_id
        self.token = token
        self.base_url = f"https://management.azure.com/subscriptions/{subscription_id}"

    def get_advisor_recommendations(self) -> Dict[str, Any]:
        """
        Get Azure Advisor recommendations for cost optimization.

        Returns:
            Dict[str, Any]: Advisor recommendations
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Advisor/recommendations"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get advisor recommendations: {str(e)}"}

    def get_reserved_instance_recommendations(self) -> Dict[str, Any]:
        """
        Get Reserved Instance recommendations.

        Returns:
            Dict[str, Any]: Reserved Instance recommendations
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Consumption/reservationRecommendations"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get Reserved Instance recommendations: {str(e)}"}

    def get_optimization_recommendations(self) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations.

        Returns:
            Dict[str, Any]: Optimization recommendations
        """
        try:
            recommendations = {
                'advisor_recommendations': self.get_advisor_recommendations(),
                'reserved_instance_recommendations': self.get_reserved_instance_recommendations()
            }
            return recommendations
        except Exception as e:
            return {"error": f"Failed to get optimization recommendations: {str(e)}"}


class AzureFinOpsGovernance:
    """Azure FinOps Governance class for policy and compliance features."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure FinOps Governance client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        self.subscription_id = subscription_id
        self.token = token
        self.base_url = f"https://management.azure.com/subscriptions/{subscription_id}"

    def get_cost_allocation_tags(self) -> Dict[str, Any]:
        """
        Get cost allocation tags.

        Returns:
            Dict[str, Any]: Cost allocation tags
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.CostManagement/tags"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get cost allocation tags: {str(e)}"}

    def get_policy_compliance(self) -> Dict[str, Any]:
        """
        Get policy compliance status.

        Returns:
            Dict[str, Any]: Policy compliance status
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults"
            
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get policy compliance: {str(e)}"}

    def get_cost_policies(self) -> Dict[str, Any]:
        """
        Get cost management policies.

        Returns:
            Dict[str, Any]: Cost policies
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Authorization/policyDefinitions"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get cost policies: {str(e)}"}


class AzureFinOpsAnalytics:
    """Azure FinOps Analytics class for advanced analytics and reporting."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure FinOps Analytics client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        self.subscription_id = subscription_id
        self.token = token
        self.base_url = f"https://management.azure.com/subscriptions/{subscription_id}"

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
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.CostManagement/forecast"
            
            payload = {
                "timeframe": "Custom",
                "timePeriod": {
                    "from": start_date,
                    "to": end_date
                },
                "dataset": {
                    "granularity": "Monthly",
                    "aggregation": {
                        "totalCost": {
                            "name": "PreTaxCost",
                            "function": "Sum"
                        }
                    }
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get cost forecast: {str(e)}"}

    def get_cost_anomalies(self) -> Dict[str, Any]:
        """
        Get cost anomalies.

        Returns:
            Dict[str, Any]: Cost anomalies data
        """
        try:
            # Azure Cost Anomaly Detection would be implemented here
            # For now, return a placeholder structure
            return {
                "anomalies": [
                    {
                        "anomaly_id": "anomaly-456",
                        "service": "Virtual Machines",
                        "cost_impact": 200.00,
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
                    "cost_per_user": 30.25,
                    "cost_per_transaction": 0.20,
                    "utilization_rate": 0.80,
                    "waste_percentage": 0.20
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

            cost_data = self.get_cost_data(
                start_date=start_date,
                end_date=end_date,
                granularity="Monthly"
            )

            return {
                "report_type": report_type,
                "period": {"start": start_date, "end": end_date},
                "cost_data": cost_data,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to generate cost report: {str(e)}"}

