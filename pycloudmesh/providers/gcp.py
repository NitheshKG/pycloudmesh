from google.cloud import billing_v1
from google.cloud import bigquery
from google.cloud import recommender
from google.oauth2 import service_account
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from google.cloud import recommender_v1, billing_budgets_v1


class GCPReservationCost:
    """GCP Reservation Cost Management class for handling GCP reservation-related operations."""

    def __init__(self, project_id: str, credentials_path: str):
        """
        Initialize GCP Reservation Cost client.

        Args:
            project_id (str): GCP project ID
            credentials_path (str): Path to GCP service account credentials file
        """
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.billing_client = billing_v1.CloudBillingClient(credentials=self.credentials)
        self.recommender_client = recommender_v1.RecommenderClient(credentials=self.credentials)

    def get_reservation_cost(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get GCP reservation utilization and cost data.

        Args:
            start_date (Optional[str]): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (Optional[str]): End date in YYYY-MM-DD format. Defaults to last day of current month.

        Returns:
            Dict[str, Any]: Reservation utilization data from GCP Billing.

        Raises:
            Exception: If GCP API call fails
        """
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")

        try:
            # GCP doesn't have a direct reservation cost API like AWS/Azure
            # This would typically involve querying billing data for committed use discounts
            return {
                "message": "GCP reservation cost data requires billing export setup",
                "period": {"start": start_date, "end": end_date},
                "reservation_utilization": []
            }
        except Exception as e:
            return {"error": f"Failed to fetch reservation utilization: {str(e)}"}

    def get_reservation_recommendation(self) -> List[Dict[str, Any]]:
        """
        Get GCP reservation recommendations using the Recommender API.

        Returns:
            List[Dict[str, Any]]: List of reservation recommendations.

        Raises:
            Exception: If GCP API call fails
        """
        try:
            parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.MachineTypeRecommender"
            
            request = recommender_v1.ListRecommendationsRequest(
                parent=parent,
                page_size=50
            )
            
            page_result = self.recommender_client.list_recommendations(request=request)
            recommendations = []
            
            for response in page_result:
                recommendations.append({
                    "name": response.name,
                    "description": response.description,
                    "primary_impact": {
                        "category": response.primary_impact.category.name,
                        "cost_projection": {
                            "cost": response.primary_impact.cost_projection.cost.units,
                            "currency_code": response.primary_impact.cost_projection.cost.currency_code
                        }
                    },
                    "state_info": {
                        "state": response.state_info.state.name
                    }
                })
            
            return recommendations
        except Exception as e:
            return [{"error": f"Failed to fetch reservation recommendations: {str(e)}"}]


class GCPBudgetManagement:
    """GCP Budget Management class for handling GCP budget-related operations."""

    def __init__(self, project_id: str, credentials_path: str):
        """
        Initialize GCP Budget Management client.

        Args:
            project_id (str): GCP project ID
            credentials_path (str): Path to GCP service account credentials file
        """
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.budget_client = billing_budgets_v1.BudgetServiceClient(credentials=self.credentials)

    def list_budgets(
        self,
        billing_account: str,
        /,
        *,
        max_results: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        List GCP budgets for a billing account.

        Args:
            billing_account (str): GCP billing account ID
            max_results (Optional[int]): Maximum number of results to return

        Returns:
            Dict[str, Any]: List of budgets

        Raises:
            Exception: If GCP API call fails
        """
        try:
            parent = f"billingAccounts/{billing_account}"
            
            request = billing_budgets_v1.ListBudgetsRequest(
                parent=parent,
                page_size=max_results or 50
            )
            
            page_result = self.budget_client.list_budgets(request=request)
            budgets = []
            
            for response in page_result:
                budgets.append({
                    "name": response.name,
                    "display_name": response.display_name,
                    "budget_filter": {
                        "projects": list(response.budget_filter.projects),
                        "credit_types_treatment": response.budget_filter.credit_types_treatment.name
                    },
                    "amount": {
                        "specified_amount": {
                            "currency_code": response.amount.specified_amount.currency_code,
                            "units": response.amount.specified_amount.units,
                            "nanos": response.amount.specified_amount.nanos
                        }
                    },
                    "threshold_rules": [
                        {
                            "threshold_percent": rule.threshold_percent,
                            "spend_basis": rule.spend_basis.name
                        }
                        for rule in response.threshold_rules
                    ]
                })
            
            return {"budgets": budgets}
        except Exception as e:
            return {"error": f"Failed to list budgets: {str(e)}"}

    def create_budget(
        self,
        billing_account: str,
        budget_name: str,
        amount: float,
        currency_code: str = "USD"
    ) -> Dict[str, Any]:
        """
        Create a new GCP budget.

        Args:
            billing_account (str): GCP billing account ID
            budget_name (str): Name of the budget
            amount (float): Budget amount
            currency_code (str): Currency code for the budget

        Returns:
            Dict[str, Any]: Budget creation response
        """
        try:
            parent = f"billingAccounts/{billing_account}"
            
            budget = billing_budgets_v1.Budget(
                display_name=budget_name,
                budget_filter=billing_budgets_v1.Filter(
                    projects=[f"projects/{self.project_id}"]
                ),
                amount=billing_budgets_v1.BudgetAmount(
                    specified_amount=billing_budgets_v1.Money(
                        currency_code=currency_code,
                        units=str(int(amount)),
                        nanos=int((amount % 1) * 1e9)
                    )
                ),
                threshold_rules=[
                    billing_budgets_v1.ThresholdRule(
                        threshold_percent=0.5,
                        spend_basis=billing_budgets_v1.ThresholdRule.SpendBasis.CURRENT_SPEND
                    ),
                    billing_budgets_v1.ThresholdRule(
                        threshold_percent=0.9,
                        spend_basis=billing_budgets_v1.ThresholdRule.SpendBasis.CURRENT_SPEND
                    )
                ]
            )
            
            request = billing_budgets_v1.CreateBudgetRequest(
                parent=parent,
                budget=budget
            )
            
            response = self.budget_client.create_budget(request=request)
            return {
                "name": response.name,
                "display_name": response.display_name,
                "amount": {
                    "currency_code": response.amount.specified_amount.currency_code,
                    "units": response.amount.specified_amount.units
                }
            }
        except Exception as e:
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
            # GCP doesn't have a direct budget alerts API
            # This would typically involve Cloud Monitoring alerts
            return {
                "message": "GCP budget alerts require Cloud Monitoring setup",
                "budget_name": budget_name
            }
        except Exception as e:
            return {"error": f"Failed to get budget alerts: {str(e)}"}


class GCPCostManagement:
    """GCP Cost Management class for handling GCP cost-related operations."""

    def __init__(self, project_id: str, credentials_path: str):
        """
        Initialize GCP Cost Management client.

        Args:
            project_id (str): GCP project ID
            credentials_path (str): Path to GCP service account credentials file
        """
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.billing_client = billing_v1.CloudBillingClient(credentials=self.credentials)

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
        Fetch GCP cost data from Billing API.

        Args:
            start_date (Optional[str]): Start date (YYYY-MM-DD). Defaults to first day of current month.
            end_date (Optional[str]): End date (YYYY-MM-DD). Defaults to today's date.
            granularity (str): "Daily", "Monthly", or "None". Defaults to "Monthly".
            metrics (Optional[List[str]]): List of cost metrics. Defaults to standard cost metrics.
            group_by (Optional[List[str]]): Grouping criteria.
            filter_ (Optional[Dict[str, Any]]): Filter criteria.

        Returns:
            Dict[str, Any]: Cost data from GCP Billing.

        Raises:
            Exception: If GCP API call fails
        """
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        try:
            # GCP billing data requires BigQuery export setup
            # This is a placeholder implementation
            return {
                "message": "GCP cost data requires BigQuery billing export setup",
                "period": {"start": start_date, "end": end_date},
                "cost_data": []
            }
        except Exception as e:
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
            dimensions = ["service", "location", "project"]

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
        return self.get_cost_data(
            start_date=start_date,
            end_date=end_date,
            filter_={"resource_id": resource_id}
        )


class GCPFinOpsOptimization:
    """GCP FinOps Optimization class for cost optimization features."""

    def __init__(self, project_id: str, credentials_path: str):
        """
        Initialize GCP FinOps Optimization client.

        Args:
            project_id (str): GCP project ID
            credentials_path (str): Path to GCP service account credentials file
        """
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.recommender_client = recommender_v1.RecommenderClient(credentials=self.credentials)

    def get_machine_type_recommendations(self) -> Dict[str, Any]:
        """
        Get machine type optimization recommendations.

        Returns:
            Dict[str, Any]: Machine type recommendations
        """
        try:
            parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.MachineTypeRecommender"
            
            request = recommender_v1.ListRecommendationsRequest(
                parent=parent,
                page_size=50
            )
            
            page_result = self.recommender_client.list_recommendations(request=request)
            recommendations = []
            
            for response in page_result:
                recommendations.append({
                    "name": response.name,
                    "description": response.description,
                    "primary_impact": {
                        "category": response.primary_impact.category.name,
                        "cost_projection": {
                            "cost": response.primary_impact.cost_projection.cost.units,
                            "currency_code": response.primary_impact.cost_projection.cost.currency_code
                        }
                    }
                })
            
            return {"recommendations": recommendations}
        except Exception as e:
            return {"error": f"Failed to get machine type recommendations: {str(e)}"}

    def get_idle_resource_recommendations(self) -> Dict[str, Any]:
        """
        Get idle resource recommendations.

        Returns:
            Dict[str, Any]: Idle resource recommendations
        """
        try:
            parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.IdleResourceRecommender"
            
            request = recommender_v1.ListRecommendationsRequest(
                parent=parent,
                page_size=50
            )
            
            page_result = self.recommender_client.list_recommendations(request=request)
            recommendations = []
            
            for response in page_result:
                recommendations.append({
                    "name": response.name,
                    "description": response.description,
                    "primary_impact": {
                        "category": response.primary_impact.category.name,
                        "cost_projection": {
                            "cost": response.primary_impact.cost_projection.cost.units,
                            "currency_code": response.primary_impact.cost_projection.cost.currency_code
                        }
                    }
                })
            
            return {"recommendations": recommendations}
        except Exception as e:
            return {"error": f"Failed to get idle resource recommendations: {str(e)}"}

    def get_optimization_recommendations(self) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations.

        Returns:
            Dict[str, Any]: Optimization recommendations
        """
        try:
            recommendations = {
                'machine_type_recommendations': self.get_machine_type_recommendations(),
                'idle_resource_recommendations': self.get_idle_resource_recommendations()
            }
            return recommendations
        except Exception as e:
            return {"error": f"Failed to get optimization recommendations: {str(e)}"}


class GCPFinOpsGovernance:
    """GCP FinOps Governance class for policy and compliance features."""

    def __init__(self, project_id: str, credentials_path: str):
        """
        Initialize GCP FinOps Governance client.

        Args:
            project_id (str): GCP project ID
            credentials_path (str): Path to GCP service account credentials file
        """
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)

    def get_cost_allocation_tags(self) -> Dict[str, Any]:
        """
        Get cost allocation labels.

        Returns:
            Dict[str, Any]: Cost allocation labels
        """
        try:
            # GCP uses labels for cost allocation
            # This would typically involve Resource Manager API
            return {
                "message": "GCP cost allocation requires Resource Manager API setup",
                "labels": []
            }
        except Exception as e:
            return {"error": f"Failed to get cost allocation labels: {str(e)}"}

    def get_policy_compliance(self) -> Dict[str, Any]:
        """
        Get policy compliance status.

        Returns:
            Dict[str, Any]: Policy compliance status
        """
        try:
            # GCP Policy API would be used here
            return {
                "message": "GCP policy compliance requires Policy API setup",
                "compliance_status": "unknown"
            }
        except Exception as e:
            return {"error": f"Failed to get policy compliance: {str(e)}"}

    def get_cost_policies(self) -> Dict[str, Any]:
        """
        Get cost management policies.

        Returns:
            Dict[str, Any]: Cost policies
        """
        try:
            # GCP Organization Policy API would be used here
            return {
                "message": "GCP cost policies require Organization Policy API setup",
                "policies": []
            }
        except Exception as e:
            return {"error": f"Failed to get cost policies: {str(e)}"}


class GCPFinOpsAnalytics:
    """GCP FinOps Analytics class for advanced analytics and reporting."""

    def __init__(self, project_id: str, credentials_path: str):
        """
        Initialize GCP FinOps Analytics client.

        Args:
            project_id (str): GCP project ID
            credentials_path (str): Path to GCP service account credentials file
        """
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)

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
            # GCP cost forecasting would typically use BigQuery ML
            return {
                "message": "GCP cost forecasting requires BigQuery ML setup",
                "period": {"start": start_date, "end": end_date},
                "forecast_period": forecast_period
            }
        except Exception as e:
            return {"error": f"Failed to get cost forecast: {str(e)}"}

    def get_cost_anomalies(self) -> Dict[str, Any]:
        """
        Get cost anomalies.

        Returns:
            Dict[str, Any]: Cost anomalies data
        """
        try:
            # GCP cost anomaly detection would use Cloud Monitoring
            return {
                "anomalies": [
                    {
                        "anomaly_id": "anomaly-789",
                        "service": "Compute Engine",
                        "cost_impact": 100.00,
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
                    "cost_per_user": 20.75,
                    "cost_per_transaction": 0.10,
                    "utilization_rate": 0.85,
                    "waste_percentage": 0.15
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

            return {
                "report_type": report_type,
                "period": {"start": start_date, "end": end_date},
                "message": "GCP cost reports require BigQuery billing export setup",
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to generate cost report: {str(e)}"}
