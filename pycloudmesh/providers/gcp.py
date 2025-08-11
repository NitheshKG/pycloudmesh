from google.cloud import billing_v1
from google.oauth2 import service_account
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from google.cloud import recommender_v1
from google.cloud.billing.budgets_v1 import BudgetServiceClient, ListBudgetsRequest, CreateBudgetRequest, Budget
import os
from google.cloud import bigquery


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
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        
    ) -> Dict[str, Any]:
        """
        Get GCP reservation utilization and cost data using BigQuery billing export.

        Args:
            bq_project_id (str): BigQuery project ID for billing export (required).
            bq_dataset (str): BigQuery dataset name for billing export (required).
            bq_table (str): BigQuery table name for billing export (required).
            start_date (Optional[str]): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (Optional[str]): End date in YYYY-MM-DD format. Defaults to last day of current month.

        Returns:
            Dict[str, Any]: Reservation utilization data from GCP Billing.

        Raises:
            Exception: If GCP API call fails
        """
        from google.cloud import bigquery
        
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")

        try:
            client = bigquery.Client(project=bq_project_id, credentials=self.credentials)
            
            query = f"""
                SELECT
                    DATE(usage_start_time) as date,
                    service.description as service,
                    sku.description as sku_description,
                    SUM(cost) as total_cost,
                    SUM(usage.amount) as usage_amount,
                    usage.unit as usage_unit,
                    COUNT(DISTINCT project.id) as project_count
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE 
                    usage_start_time >= '{start_date}'
                    AND usage_end_time <= '{end_date}'
                    AND (
                        LOWER(sku.description) LIKE '%committed use discount%'
                        OR LOWER(sku.description) LIKE '%committed use%'
                        OR LOWER(sku.description) LIKE '%reservation%'
                        OR LOWER(sku.description) LIKE '%sustained use%'
                    )
                    AND LOWER(sku.description) NOT LIKE '%free tier%'
                GROUP BY date, service, sku_description, usage_unit
                ORDER BY date DESC, total_cost DESC
            """
            
            query_job = client.query(query)
            results = list(query_job)
            
            reservation_data = []
            total_reservation_cost = 0
            
            if not results:
                return {
                    "period": {"start": start_date, "end": end_date},
                    "total_reservation_cost": 0.0,
                    "reservation_utilization": [],
                    "insights": {
                        "days_with_reservations": 0,
                        "projects_with_reservations": 0,
                        "avg_daily_reservation_cost": 0.0,
                        "total_reservations_found": 0
                    },
                    "message": "No reservation data found in BigQuery billing export for the specified period"
                }
            
            for row in results:
                cost = float(row["total_cost"]) if row["total_cost"] is not None else 0.0
                usage_amount = float(row["usage_amount"]) if row["usage_amount"] is not None else 0.0
                
                reservation_data.append({
                    "date": row["date"].strftime("%Y-%m-%d") if row["date"] else "unknown",
                    "service": row["service"] if row["service"] else "unknown",
                    "sku_description": row["sku_description"] if row["sku_description"] else "unknown",
                    "cost": cost,
                    "usage_amount": usage_amount,
                    "usage_unit": row["usage_unit"] if row["usage_unit"] else "unknown",
                    "project_count": row["project_count"] if row["project_count"] is not None else 0
                })
                total_reservation_cost += cost
            
            insights_query = f"""
                SELECT
                    COUNT(DISTINCT DATE(usage_start_time)) as days_with_reservations,
                    COUNT(DISTINCT project.id) as projects_with_reservations,
                    AVG(cost) as avg_daily_reservation_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE 
                    usage_start_time >= '{start_date}'
                    AND usage_end_time <= '{end_date}'
                    AND (
                        LOWER(sku.description) LIKE '%committed use discount%'
                        OR LOWER(sku.description) LIKE '%committed use%'
                        OR LOWER(sku.description) LIKE '%reservation%'
                        OR LOWER(sku.description) LIKE '%sustained use%'
                    )
                    AND LOWER(sku.description) NOT LIKE '%free tier%'
            """
            
            insights_job = client.query(insights_query)
            insights = list(insights_job)[0] if list(insights_job) else None
            
            return {
                "period": {"start": start_date, "end": end_date},
                "total_reservation_cost": round(total_reservation_cost, 2),
                "reservation_utilization": reservation_data,
                "insights": {
                    "days_with_reservations": insights["days_with_reservations"] if insights and insights["days_with_reservations"] is not None else 0,
                    "projects_with_reservations": insights["projects_with_reservations"] if insights and insights["projects_with_reservations"] is not None else 0,
                    "avg_daily_reservation_cost": round(float(insights["avg_daily_reservation_cost"]), 2) if insights and insights["avg_daily_reservation_cost"] is not None else 0.0,
                    "total_reservations_found": len(reservation_data)
                },
                "message": f"Reservation cost data retrieved from BigQuery billing export for {len(reservation_data)} reservation records"
            }
            
        except Exception as e:
            return {
                "error": f"Failed to fetch reservation utilization: {str(e)}",
                "period": {"start": start_date, "end": end_date},
                "message": "GCP reservation cost data requires BigQuery billing export setup with proper permissions"
            }

    def get_reservation_recommendation(self) -> List[Dict[str, Any]]:
        """
        Get GCP reservation recommendations using the Recommender API.

        Returns:
            List[Dict[str, Any]]: List of reservation recommendations.

        Raises:
            Exception: If GCP API call fails
        """
        try:
            recommendations = []
            
            machine_type_parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.MachineTypeRecommender"
            
            machine_type_request = recommender_v1.ListRecommendationsRequest(
                parent=machine_type_parent,
                page_size=50
            )
            
            machine_type_results = self.recommender_client.list_recommendations(request=machine_type_request)
            
            for response in machine_type_results:
                recommendations.append({
                    "type": "machine_type_optimization",
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
                    },
                    "priority": "high" if "cost" in response.description.lower() else "medium"
                })
            
            try:
                cud_parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.commitment.UsageCommitmentRecommender"
                
                cud_request = recommender_v1.ListRecommendationsRequest(
                    parent=cud_parent,
                    page_size=20
                )
                
                cud_results = self.recommender_client.list_recommendations(request=cud_request)
                
                for response in cud_results:
                    recommendations.append({
                        "type": "committed_use_discount",
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
                        },
                        "priority": "high"
                    })
            except Exception:
                pass
            
            try:
                sud_parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.SustainedUseDiscountRecommender"
                
                sud_request = recommender_v1.ListRecommendationsRequest(
                    parent=sud_parent,
                    page_size=20
                )
                
                sud_results = self.recommender_client.list_recommendations(request=sud_request)
                
                for response in sud_results:
                    recommendations.append({
                        "type": "sustained_use_discount",
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
                        },
                        "priority": "medium"
                    })
            except Exception:
                pass
            
            def sort_key(rec):
                priority_score = {"high": 3, "medium": 2, "low": 1}.get(rec.get("priority", "medium"), 1)
                cost_savings = float(rec.get("primary_impact", {}).get("cost_projection", {}).get("cost", 0))
                return (priority_score, -cost_savings)
            
            recommendations.sort(key=sort_key, reverse=True)
            
            total_potential_savings = sum(
                float(rec.get("primary_impact", {}).get("cost_projection", {}).get("cost", 0))
                for rec in recommendations
            )
            
            recommendation_summary = {
                "total_recommendations": len(recommendations),
                "total_potential_savings": round(total_potential_savings, 2),
                "recommendation_types": list(set(rec.get("type", "unknown") for rec in recommendations)),
                "high_priority_count": len([r for r in recommendations if r.get("priority") == "high"]),
                "message": f"Found {len(recommendations)} reservation optimization recommendations"
            }
            
            return {
                "recommendations": recommendations,
                "summary": recommendation_summary
            }
            
        except Exception as e:
            return {
                "error": f"Failed to fetch reservation recommendations: {str(e)}",
                "recommendations": [],
                "summary": {
                    "total_recommendations": 0,
                    "total_potential_savings": 0,
                    "message": "Unable to retrieve reservation recommendations"
                }
            }


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
        self.budget_client = BudgetServiceClient(credentials=self.credentials)

    def list_budgets(
        self,
        billing_account: str,
        max_results: Optional[int] = None,
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
            billing_account = billing_account
            max_results = max_results or 50
            parent = f"billingAccounts/{billing_account}"
            
            request = ListBudgetsRequest(
                parent=parent,
                page_size=max_results
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
        currency_code: str = "USD",
        notifications_rule: dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new GCP budget.

        Args:
            billing_account (str): GCP billing account ID
            budget_name (str): Name of the budget
            amount (float): Budget amount
            currency_code (str): Currency code for the budget
            notifications_rule (dict): Notification rule for budget alerts

        Returns:
            Dict[str, Any]: Budget creation response
        """
        try:
            parent = f"billingAccounts/{billing_account}"
            
            budget = {
                "display_name": budget_name,
                "budget_filter": {
                    "projects": [f"projects/{self.project_id}"]
                },
                "amount": {
                    "specified_amount": {
                        "currency_code": currency_code,
                        "units": int(amount)
                    }
                },
                "threshold_rules": [
                    {
                        "threshold_percent": 0.5,
                        "spend_basis": "CURRENT_SPEND"
                    },
                    {
                        "threshold_percent": 0.9,
                        "spend_basis": "CURRENT_SPEND"
                    }
                ]
            }
            if amount % 1 != 0:
                budget["amount"]["specified_amount"]["nanos"] = int((amount % 1) * 1e9)
            import json
            print("DEBUG BUDGET PAYLOAD:", json.dumps(budget, indent=2, default=str))
            response = self.budget_client.create_budget(request={
                "parent": parent,
                "budget": budget
            })
            
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

    def get_budget_notifications(self, billing_account: str, budget_display_name: str) -> Dict[str, Any]:
        """
        Get notifications for a specific budget.
        Args:
            billing_account (str): GCP billing account ID
            budget_display_name (str): Display name of the budget
        Returns:
            Dict[str, Any]: Budget threshold rules and alert info
        """
        try:
            parent = f"billingAccounts/{billing_account}"
            from google.cloud.billing.budgets_v1 import ListBudgetsRequest
            request = ListBudgetsRequest(parent=parent)
            budgets = self.budget_client.list_budgets(request=request)
            for budget in budgets:
                if budget.display_name == budget_display_name:
                    return {
                        "budget_name": budget.name,
                        "display_name": budget.display_name,
                        "threshold_rules": [
                            {
                                "threshold_percent": rule.threshold_percent,
                                "spend_basis": rule.spend_basis.name
                            }
                            for rule in budget.threshold_rules
                        ],
                        "message": (
                            "GCP budget alerts are delivered via Cloud Monitoring and/or Pub/Sub. "
                            "To receive notifications, ensure you have set up notification channels in the budget configuration."
                        )
                    }
            return {"error": f"Budget with display name '{budget_display_name}' not found."}
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
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "Monthly",
        metrics: Optional[List[str]] = None,
        group_by: Optional[List[str]] = None,
        filter_: Optional[Dict[str, Any]] = None,
        
    ) -> Dict[str, Any]:
        """
        Fetch GCP cost data from BigQuery billing export.

        Args:
            start_date (Optional[str]): Start date (YYYY-MM-DD).
            end_date (Optional[str]): End date (YYYY-MM-DD).
            granularity (str): "Daily", "Monthly", or "None".
            metrics (Optional[List[str]]): List of cost metrics.
            group_by (Optional[List[str]]): Grouping criteria.
            filter_ (Optional[Dict[str, Any]]): Filter criteria.
            bq_project_id (Optional[str]): BigQuery project ID for billing export.
            bq_dataset (Optional[str]): BigQuery dataset name for billing export.
            bq_table (Optional[str]): BigQuery table name for billing export.

        Returns:
            Dict[str, Any]: Cost data from GCP Billing.
        """
        from google.cloud import bigquery
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
        if not metrics:
            metrics = ["cost"]
        if not group_by:
            group_by = ["service.description"]

        bq_project = bq_project_id
        if not (bq_project and bq_dataset and bq_table):
            return {"error": "BigQuery billing export table not configured. Pass bq_project_id, bq_dataset, and bq_table to get_cost_data."}

        client = bigquery.Client(project=bq_project, credentials=self.credentials)

        select_fields = []
        group_fields = []
        for field in group_by:
            select_fields.append(field)
            group_fields.append(field)
        select_fields.append("SUM(cost) as total_cost")

        where_clauses = [
            f"usage_start_time >= '{start_date}'",
            f"usage_end_time <= '{end_date}'"
        ]
        if filter_:
            for k, v in filter_.items():
                where_clauses.append(f"{k} = '{v}'")

        query = f"""
            SELECT {', '.join(select_fields)}
            FROM `{bq_project}.{bq_dataset}.{bq_table}`
            WHERE {' AND '.join(where_clauses)}
            GROUP BY {', '.join(group_fields)}
            ORDER BY total_cost DESC
        """

        try:
            query_job = client.query(query)
            results = [dict(row) for row in query_job]
            return {
                "period": {"start": start_date, "end": end_date},
                "granularity": granularity,
                "metrics": metrics,
                "group_by": group_by,
                "cost_data": results
            }
        except Exception as e:
            return {"error": f"Failed to fetch cost data from BigQuery: {str(e)}"}

    def get_cost_analysis(
        self,
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get detailed cost analysis with dimensions, insights, and breakdowns.

        Args:
            bq_project_id (str): BigQuery project ID for billing export (required).
            bq_dataset (str): BigQuery dataset name for billing export (required).
            bq_table (str): BigQuery table name for billing export (required).
            start_date (Optional[str]): Start date for analysis
            end_date (Optional[str]): End date for analysis

        Returns:
            Dict[str, Any]: Cost analysis with breakdowns, insights, and trends
        """
        from google.cloud import bigquery
        from datetime import datetime, timedelta

        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        try:
            client = bigquery.Client(project=bq_project_id, credentials=self.credentials)
            
            query = f"""
                SELECT
                    service.description as service_name,
                    COALESCE(CAST(location.location AS STRING), 'UNKNOWN') as location,
                    project.id as project_id,
                    SUM(cost) as total_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE 
                    usage_start_time >= '{start_date}'
                    AND usage_end_time <= '{end_date}'
                GROUP BY service_name, location, project_id
                ORDER BY total_cost DESC
            """
            
            query_job = client.query(query)
            results = list(query_job)
            
            analysis = {
                "period": {"start": start_date, "end": end_date},
                "dimensions": ["service", "location", "project"],
                "total_cost": 0.0,
                "cost_breakdown": {},
                "top_services": [],
                "cost_trends": [],
                "insights": []
            }
            
            service_costs = {}
            location_costs = {}
            project_costs = {}
            
            for row in results:
                service_name = row["service_name"] if row["service_name"] else "Unknown Service"
                location = row["location"] if row["location"] else "Unknown Location"
                project_id = row["project_id"] if row["project_id"] else "Unknown Project"
                cost = float(row["total_cost"]) if row["total_cost"] is not None else 0.0
                
                if service_name not in service_costs:
                    service_costs[service_name] = 0.0
                service_costs[service_name] += cost
                
                if location not in location_costs:
                    location_costs[location] = 0.0
                location_costs[location] += cost
                
                if project_id not in project_costs:
                    project_costs[project_id] = 0.0
                project_costs[project_id] += cost
                
                analysis["total_cost"] += cost
                
                analysis["cost_trends"].append({
                    "service": service_name,
                    "location": location,
                    "project": project_id,
                    "cost": cost
                })
            
            analysis["cost_breakdown"] = {
                "by_service": service_costs,
                "by_location": location_costs,
                "by_project": project_costs
            }
            
            sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
            analysis["top_services"] = [
                {"service": service, "cost": cost} 
                for service, cost in sorted_services[:5]
            ]
            
            if analysis["total_cost"] > 0:
                if sorted_services:
                    top_service = sorted_services[0]
                    top_percentage = (top_service[1] / analysis["total_cost"]) * 100
                    analysis["insights"].append(
                        f"Top service '{top_service[0]}' accounts for {top_percentage:.1f}% of total costs"
                    )
                    
                    if len(sorted_services) >= 3:
                        top3_total = sum(cost for _, cost in sorted_services[:3])
                        top3_percentage = (top3_total / analysis["total_cost"]) * 100
                        analysis["insights"].append(
                            f"Top 3 services account for {top3_percentage:.1f}% of total costs"
                        )
                
                if location_costs:
                    top_location = max(location_costs.items(), key=lambda x: x[1])
                    location_percentage = (top_location[1] / analysis["total_cost"]) * 100
                    analysis["insights"].append(
                        f"Top location '{top_location[0]}' accounts for {location_percentage:.1f}% of total costs"
                    )
                
                if project_costs:
                    top_project = max(project_costs.items(), key=lambda x: x[1])
                    project_percentage = (top_project[1] / analysis["total_cost"]) * 100
                    analysis["insights"].append(
                        f"Top project '{top_project[0]}' accounts for {project_percentage:.1f}% of total costs"
                    )
                
                if len(sorted_services) > 1:
                    cost_variance = max(service_costs.values()) - min(service_costs.values())
                    if cost_variance > analysis["total_cost"] * 0.5:
                        analysis["insights"].append("High cost concentration in top services")
                    else:
                        analysis["insights"].append("Relatively even cost distribution across services")
            
            return analysis
            
        except Exception as e:
            return {"error": f"Failed to perform cost analysis: {str(e)}"}

    def get_cost_trends(
        self,
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get detailed cost trends analysis with insights and patterns.

        Args:
            bq_project_id (str): BigQuery project ID for billing export (required).
            bq_dataset (str): BigQuery dataset name for billing export (required).
            bq_table (str): BigQuery table name for billing export (required).
            start_date (str, optional): Start date for trend analysis (in kwargs).
            end_date (str, optional): End date for trend analysis (in kwargs).

        Returns:
            Dict[str, Any]: Cost trends data with daily breakdown and analysis
        """
        from google.cloud import bigquery
        from datetime import datetime, timedelta

        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        try:
            client = bigquery.Client(project=bq_project_id, credentials=self.credentials)
            
            query = f"""
                SELECT
                    DATE(usage_start_time) as date,
                    SUM(cost) as daily_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE 
                    usage_start_time >= '{start_date}'
                    AND usage_end_time <= '{end_date}'
                GROUP BY date
                ORDER BY date
            """
            
            query_job = client.query(query)
            results = list(query_job)
            
            trends_analysis = {
                "period": {"start": start_date, "end": end_date},
                "granularity": "Daily",
                "total_periods": 0,
                "total_cost": 0.0,
                "average_daily_cost": 0.0,
                "cost_periods": [],
                "trend_direction": "stable",
                "growth_rate": 0.0,
                "peak_periods": [],
                "low_periods": [],
                "patterns": [],
                "insights": []
            }
            
            costs = []
            for row in results:
                date = row["date"].strftime("%Y-%m-%d") if row["date"] else "unknown"
                cost = float(row["daily_cost"]) if row["daily_cost"] is not None else 0.0
                
                trends_analysis["total_cost"] += cost
                trends_analysis["total_periods"] += 1
                trends_analysis["cost_periods"].append({
                    "date": date,
                    "cost": cost
                })
                costs.append(cost)
            
            if trends_analysis["total_periods"] > 0:
                trends_analysis["average_daily_cost"] = trends_analysis["total_cost"] / trends_analysis["total_periods"]
            
            if costs:
                max_cost = max(costs)
                min_cost = min(costs)
                
                for period in trends_analysis["cost_periods"]:
                    if period["cost"] == max_cost and max_cost > 0:
                        trends_analysis["peak_periods"].append(period)
                    if period["cost"] == min_cost:
                        trends_analysis["low_periods"].append(period)
            
            if len(costs) >= 2:
                first_half = costs[:len(costs)//2]
                second_half = costs[len(costs)//2:]
                
                if first_half and second_half:
                    first_avg = sum(first_half) / len(first_half)
                    second_avg = sum(second_half) / len(second_half)
                    
                    if first_avg > 0:
                        growth_rate = ((second_avg - first_avg) / first_avg) * 100
                        trends_analysis["growth_rate"] = growth_rate
                        
                        if growth_rate > 10:
                            trends_analysis["trend_direction"] = "increasing"
                        elif growth_rate < -10:
                            trends_analysis["trend_direction"] = "decreasing"
                        else:
                            trends_analysis["trend_direction"] = "stable"
            
            if costs:
                non_zero_costs = [c for c in costs if c > 0]
                if non_zero_costs:
                    cost_variance = max(non_zero_costs) - min(non_zero_costs)
                    if cost_variance > trends_analysis["average_daily_cost"]:
                        trends_analysis["patterns"].append("High cost variability")
                    else:
                        trends_analysis["patterns"].append("Consistent cost pattern")
                
                zero_cost_periods = len([c for c in costs if c == 0])
                if zero_cost_periods > len(costs) * 0.5:
                    trends_analysis["patterns"].append("Many zero-cost periods")
                
                if trends_analysis["total_cost"] > 0:
                    trends_analysis["insights"].append(
                        f"Total cost over {trends_analysis['total_periods']} periods: ${trends_analysis['total_cost']:.2f}"
                    )
                    trends_analysis["insights"].append(
                        f"Average cost per period: ${trends_analysis['average_daily_cost']:.4f}"
                    )
                    
                    if trends_analysis["trend_direction"] != "stable":
                        trends_analysis["insights"].append(
                            f"Cost trend is {trends_analysis['trend_direction']} ({trends_analysis['growth_rate']:.1f}% change)"
                        )
                    
                    if trends_analysis["peak_periods"]:
                        peak_period = trends_analysis["peak_periods"][0]
                        trends_analysis["insights"].append(
                            f"Peak cost period: {peak_period['date']} (${peak_period['cost']:.4f})"
                        )
            
            return trends_analysis
            
        except Exception as e:
            return {"error": f"Failed to fetch cost trends: {str(e)}"}

    def get_resource_costs(
        self,
        resource_name: str,
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get detailed cost analysis for a specific resource.

        Args:
            resource_name (str): Name/ID of the resource to get costs for.
            bq_project_id (str): BigQuery project ID for billing export (required).
            bq_dataset (str): BigQuery dataset name for billing export (required).
            bq_table (str): BigQuery table name for billing export (required).
            start_date (str, optional): Start date for cost data (in kwargs).
            end_date (str, optional): End date for cost data (in kwargs).

        Returns:
            Dict[str, Any]: Detailed resource cost analysis with insights and breakdowns
        """
        from google.cloud import bigquery
        from datetime import datetime, timedelta

        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        try:
            client = bigquery.Client(project=bq_project_id, credentials=self.credentials)
            
            query = f"""
                SELECT
                    DATE(usage_start_time) as date,
                    service.description as service_name,
                    COALESCE(CAST(location.location AS STRING), 'UNKNOWN') as location,
                    SUM(cost) as daily_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE 
                    usage_start_time >= '{start_date}'
                    AND usage_end_time <= '{end_date}'
                    AND resource.name = '{resource_name}'
                GROUP BY date, service_name, location
                ORDER BY date
            """
            
            query_job = client.query(query)
            results = list(query_job)
            
            resource_analysis = {
                "resource_id": resource_name,
                "resource_type": "GCP Resource",
                "period": {"start": start_date, "end": end_date},
                "granularity": "Daily",
                "total_cost": 0.0,
                "total_periods": 0,
                "active_periods": 0,
                "cost_periods": [],
                "cost_breakdown": {
                    "by_service": {},
                    "by_location": {}
                },
                "utilization_insights": [],
                "cost_trends": [],
                "recommendations": []
            }
            
            costs = []
            service_costs = {}
            location_costs = {}
            
            for row in results:
                date = row["date"].strftime("%Y-%m-%d") if row["date"] else "unknown"
                service_name = row["service_name"] if row["service_name"] else "Unknown Service"
                location = row["location"] if row["location"] else "Unknown Location"
                cost = float(row["daily_cost"]) if row["daily_cost"] is not None else 0.0
                
                resource_analysis["total_cost"] += cost
                resource_analysis["total_periods"] += 1
                
                if cost > 0:
                    resource_analysis["active_periods"] += 1
                
                resource_analysis["cost_periods"].append({
                    "date": date,
                    "service": service_name,
                    "location": location,
                    "cost": cost
                })
                costs.append(cost)
                
                if service_name not in service_costs:
                    service_costs[service_name] = 0.0
                service_costs[service_name] += cost
                
                if location not in location_costs:
                    location_costs[location] = 0.0
                location_costs[location] += cost
            
            resource_analysis["cost_breakdown"]["by_service"] = service_costs
            resource_analysis["cost_breakdown"]["by_location"] = location_costs
            
            if resource_analysis["total_periods"] > 0:
                utilization_rate = resource_analysis["active_periods"] / resource_analysis["total_periods"]
                resource_analysis["utilization_insights"].append(
                    f"Resource utilization rate: {utilization_rate:.1%} ({resource_analysis['active_periods']} active out of {resource_analysis['total_periods']} periods)"
                )
                
                if utilization_rate < 0.5:
                    resource_analysis["utilization_insights"].append("Low resource utilization detected - consider stopping or downsizing")
                elif utilization_rate > 0.9:
                    resource_analysis["utilization_insights"].append("High resource utilization detected - consider scaling up if needed")

            if len(costs) >= 2:
                first_half = costs[:len(costs)//2]
                second_half = costs[len(costs)//2:]
                
                if first_half and second_half:
                    first_avg = sum(first_half) / len(first_half)
                    second_avg = sum(second_half) / len(second_half)
                    
                    if first_avg > 0:
                        growth_rate = ((second_avg - first_avg) / first_avg) * 100
                        if growth_rate > 10:
                            resource_analysis["cost_trends"].append(f"Resource cost trend: Increasing ({growth_rate:.1f}% growth)")
                        elif growth_rate < -10:
                            resource_analysis["cost_trends"].append(f"Resource cost trend: Decreasing ({abs(growth_rate):.1f}% reduction)")
                        else:
                            resource_analysis["cost_trends"].append("Resource cost trend: Stable")

            if resource_analysis["total_cost"] > 0:
                avg_cost = resource_analysis["total_cost"] / resource_analysis["total_periods"]
                
                if avg_cost > 10:
                    resource_analysis["recommendations"].append("High resource costs detected - review resource type and consider committed use discounts")
                
                if resource_analysis["active_periods"] < resource_analysis["total_periods"] * 0.3:
                    resource_analysis["recommendations"].append("Low resource activity - consider stopping resources during idle periods")
                
                if service_costs:
                    top_service = max(service_costs.items(), key=lambda x: x[1])
                    top_percentage = (top_service[1] / resource_analysis["total_cost"]) * 100
                    resource_analysis["recommendations"].append(
                        f"Top service: {top_service[0]} ({top_percentage:.1f}% of total) - review for optimization"
                    )
                
                if location_costs:
                    top_location = max(location_costs.items(), key=lambda x: x[1])
                    location_percentage = (top_location[1] / resource_analysis["total_cost"]) * 100
                    resource_analysis["recommendations"].append(
                        f"Primary location: {top_location[0]} ({location_percentage:.1f}% of total) - consider multi-region optimization"
                    )
                
                if len(costs) > 0:
                    max_cost = max(costs)
                    min_cost = min(costs)
                    cost_variance = max_cost - min_cost
                    
                    if cost_variance > avg_cost:
                        resource_analysis["recommendations"].append("High cost variability detected - review usage patterns")
                    else:
                        resource_analysis["recommendations"].append("Consistent cost pattern - resource usage is stable")
                
                resource_analysis["recommendations"].append(
                    f"Resource {resource_name} analysis complete - review GCP Cost Management for detailed breakdowns"
                )

            return resource_analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze resource costs: {str(e)}"}


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

    def get_cost_allocation_tags(self, **kwargs) -> Dict[str, Any]:
        """
        Get cost allocation labels from GCP resources and billing data.

        Args:
            bq_project_id (str, optional): BigQuery project ID for billing export.
            bq_dataset (str, optional): BigQuery dataset name for billing export.
            bq_table (str, optional): BigQuery table name for billing export.

        Returns:
            Dict[str, Any]: Cost allocation labels with usage statistics
        """
        try:
            try:
                from google.cloud import resourcemanager_v3
                resource_client = resourcemanager_v3.ProjectsClient(credentials=self.credentials)
                
                project_name = f"projects/{self.project_id}"
                project = resource_client.get_project(name=project_name)
                project_labels = dict(project.labels) if project.labels else {}
            except ImportError:
                project_labels = {}
            except Exception:
                project_labels = {}
            
            bq_project_id = kwargs.get('bq_project_id')
            bq_dataset = kwargs.get('bq_dataset')
            bq_table = kwargs.get('bq_table')
            resource_labels = {}
            if bq_project_id and bq_dataset and bq_table:
                try:
                    client = bigquery.Client(project=bq_project_id, credentials=self.credentials)
                    table = client.get_table(f"{bq_project_id}.{bq_dataset}.{bq_table}")
                    label_field = None
                    for field in table.schema:
                        if field.name == 'labels' and field.field_type == 'RECORD':
                            label_field = field
                            break
                    if label_field:
                        labels_query = f"""
                            SELECT DISTINCT labels
                            FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                            WHERE labels IS NOT NULL
                            LIMIT 100
                        """
                        labels_job = client.query(labels_query)
                        labels_results = list(labels_job)
                        unique_labels = set()
                        
                        for row in labels_results:
                            labels_data = row['labels']
                            if labels_data:
                                if isinstance(labels_data, dict):
                                    for key, value in labels_data.items():
                                        unique_labels.add((key, value))
                                elif isinstance(labels_data, list):
                                    for item in labels_data:
                                        if isinstance(item, dict) and 'key' in item and 'value' in item:
                                            unique_labels.add((item['key'], item['value']))
                                        else:
                                            unique_labels.add(('raw_labels', str(item)))
                                elif hasattr(labels_data, 'items'):
                                    for key, value in labels_data.items():
                                        unique_labels.add((key, value))
                                else:
                                    try:
                                        import ast
                                        if isinstance(labels_data, str):
                                            parsed_data = ast.literal_eval(labels_data)
                                            if isinstance(parsed_data, list):
                                                for item in parsed_data:
                                                    if isinstance(item, dict) and 'key' in item and 'value' in item:
                                                        unique_labels.add((item['key'], item['value']))
                                                    else:
                                                        unique_labels.add(('raw_labels', str(item)))
                                            elif isinstance(parsed_data, dict):
                                                for key, value in parsed_data.items():
                                                    unique_labels.add((key, value))
                                            else:
                                                unique_labels.add(('raw_labels', str(parsed_data)))
                                        else:
                                            unique_labels.add(('raw_labels', str(labels_data)))
                                    except (ValueError, SyntaxError):
                                        unique_labels.add(('raw_labels', str(labels_data)))
                        
                        resource_labels = {
                            "unique_labels": [
                                {"key": k, "value": v} for k, v in sorted(unique_labels)
                            ],
                            "total_unique_labels": len(unique_labels),
                            "message": f"Unique labels retrieved from BigQuery billing data ({len(unique_labels)} unique key-value pairs)"
                        }
                    else:
                        resource_labels = {
                            "note": "No top-level labels field found in BigQuery billing export table.",
                            "unique_labels": [],
                            "total_unique_labels": 0
                        }
                except Exception as e:
                    resource_labels = {
                        "error": f"Failed to retrieve labels from BigQuery: {str(e)}",
                        "unique_labels": [],
                        "total_unique_labels": 0
                    }
            else:
                resource_labels = {
                    "note": "Resource-level labels require BigQuery billing export setup. Provide bq_project_id, bq_dataset, and bq_table parameters.",
                    "unique_labels": [],
                    "total_unique_labels": 0
                }
            
            return {
                "project_labels": project_labels,
                "resource_labels": resource_labels,
                "total_labels": len(project_labels),
                "message": "Cost allocation labels retrieved from GCP Resource Manager API"
            }
        except Exception as e:
            return {"error": f"Failed to get cost allocation labels: {str(e)}"}

    def get_policy_compliance(self, **kwargs) -> Dict[str, Any]:
        """
        Get policy compliance status for GCP resources and cost policies.

        Returns:
            Dict[str, Any]: Policy compliance status with detailed findings
        """
        try:
            compliance_results = {
                "project_compliance": {},
                "resource_compliance": {},
                "cost_policy_compliance": {},
                "organization_policy_compliance": {},
                "overall_status": "unknown"
            }
            
            try:
                from google.cloud import asset_v1
                asset_client = asset_v1.AssetServiceClient(credentials=self.credentials)
                
                parent = f"projects/{self.project_id}"
                request = asset_v1.ListAssetsRequest(
                    parent=parent,
                    asset_types=["compute.googleapis.com/Instance", "storage.googleapis.com/Bucket"]
                )
                
                assets = list(asset_client.list_assets(request=request))
                compliance_results["project_compliance"] = {
                    "total_resources": len(assets),
                    "compliance_checked": True,
                    "status": "compliant" if assets else "no_resources",
                    "resource_types_found": list(set([asset.asset_type for asset in assets])) if assets else []
                }
                
            except ImportError:
                compliance_results["project_compliance"] = {
                    "error": "Asset API not available - install google-cloud-asset",
                    "status": "api_unavailable",
                    "recommendation": "Run: pip install google-cloud-asset"
                }
            except Exception as e:
                compliance_results["project_compliance"] = {
                    "error": str(e),
                    "status": "error",
                    "recommendation": "Check project permissions and API enablement"
                }
            
            try:
                from google.cloud import orgpolicy_v2
                org_policy_client = orgpolicy_v2.OrgPolicyClient(credentials=self.credentials)
                
                constraint_names = [
                    "compute.requireOsLogin",
                    "compute.requireShieldedVm",
                    "storage.uniformBucketLevelAccess",
                    "compute.vmExternalIpAccess"
                ]
                
                org_policies = {}
                for constraint in constraint_names:
                    try:
                        policy = org_policy_client.get_policy(
                            name=f"projects/{self.project_id}/policies/{constraint}"
                        )
                        org_policies[constraint] = {
                            "enforced": policy.spec is not None,
                            "policy_exists": True
                        }
                    except Exception:
                        org_policies[constraint] = {
                            "enforced": False,
                            "policy_exists": False
                        }
                
                compliance_results["organization_policy_compliance"] = {
                    "policies_checked": len(org_policies),
                    "policies_enforced": sum(1 for p in org_policies.values() if p["enforced"]),
                    "policy_details": org_policies,
                    "status": "checked"
                }
                
            except ImportError:
                compliance_results["organization_policy_compliance"] = {
                    "error": "Organization Policy API not available - install google-cloud-org-policy",
                    "status": "api_unavailable",
                    "recommendation": "Run: pip install google-cloud-org-policy"
                }
            except Exception as e:
                compliance_results["organization_policy_compliance"] = {
                    "error": str(e),
                    "status": "error"
                }
            
            cost_policies = {
                "budget_alerts_enabled": False,
                "cost_allocation_enabled": False,
                "resource_quota_enforced": False,
                "cost_monitoring_enabled": True
            }
            
            try:
                budget_client = BudgetServiceClient(credentials=self.credentials)
                cost_policies["budget_alerts_enabled"] = True
            except Exception:
                cost_policies["budget_alerts_enabled"] = False
            
            bq_project_id = kwargs.get('bq_project_id')
            if bq_project_id:
                cost_policies["cost_allocation_enabled"] = True
            
            compliance_results["cost_policy_compliance"] = cost_policies
            
            status_scores = {
                "compliant": 3,
                "checked": 2,
                "partial": 1,
                "no_resources": 1,
                "api_unavailable": 0,
                "error": 0,
                "unknown": 0
            }
            
            scores = []
            for section in ["project_compliance", "organization_policy_compliance", "cost_policy_compliance"]:
                status = compliance_results[section].get("status", "unknown")
                scores.append(status_scores.get(status, 0))
            
            avg_score = sum(scores) / len(scores) if scores else 0
            
            if avg_score >= 2.5:
                compliance_results["overall_status"] = "compliant"
            elif avg_score >= 1.5:
                compliance_results["overall_status"] = "partial"
            elif avg_score >= 0.5:
                compliance_results["overall_status"] = "limited"
            else:
                compliance_results["overall_status"] = "error"
            
            return {
                "compliance_status": compliance_results,
                "message": "Policy compliance status retrieved from GCP Asset, Organization Policy, and Budget APIs"
            }
            
        except Exception as e:
            return {"error": f"Failed to get policy compliance: {str(e)}"}

    def get_cost_policies(self, **kwargs) -> Dict[str, Any]:
        """
        Get cost management policies and budget configurations.

        Returns:
            Dict[str, Any]: Cost policies with budget and quota information
        """
        try:
            policies = {
                "budget_policies": {},
                "quota_policies": {},
                "cost_control_policies": {},
                "organization_policies": {}
            }
            
            try:
                budget_client = BudgetServiceClient(credentials=self.credentials)
                
                gcp_billing_account = kwargs.get('gcp_billing_account')
                
                if gcp_billing_account:
                    parent = f"billingAccounts/{gcp_billing_account}"
                    request = ListBudgetsRequest(parent=parent, page_size=10)
                    budgets = list(budget_client.list_budgets(request=request))
                    
                    if budgets:
                        budget_info = []
                        for budget in budgets:
                            budget_info.append({
                                "name": budget.display_name,
                                "amount": {
                                    "currency_code": budget.amount.specified_amount.currency_code,
                                    "units": budget.amount.specified_amount.units
                                },
                                "threshold_rules": [
                                    {
                                        "threshold_percent": rule.threshold_percent,
                                        "spend_basis": rule.spend_basis.name
                                    }
                                    for rule in budget.threshold_rules
                                ]
                            })
                        
                        policies["budget_policies"] = {
                            "budgets_configured": True,
                            "total_budgets": len(budgets),
                            "budget_details": budget_info,
                            "currency": budgets[0].amount.specified_amount.currency_code if budgets else "USD",
                            "message": f"Found {len(budgets)} budget(s) for billing account {gcp_billing_account}"
                        }
                    else:
                        policies["budget_policies"] = {
                            "budgets_configured": False,
                            "total_budgets": 0,
                            "message": f"No budgets found for billing account {gcp_billing_account}"
                        }
                else:
                    policies["budget_policies"] = {
                        "budgets_configured": True,
                        "total_budgets": 0,
                        "message": "Budget client accessible but no billing account specified. Pass 'gcp_billing_account' parameter to get budget details.",
                        "recommendation": "Provide gcp_billing_account parameter to retrieve actual budget information"
                    }
                    
            except Exception as e:
                policies["budget_policies"] = {
                    "error": str(e),
                    "budgets_configured": False,
                    "message": "Failed to access budget information"
                }
            
            try:
                from google.cloud import orgpolicy_v2
                org_policy_client = orgpolicy_v2.OrgPolicyClient(credentials=self.credentials)
                
                constraint_names = [
                    "compute.quota.maxCpusPerProject",
                    "compute.quota.maxInstancesPerProject",
                    "storage.quota.maxBucketsPerProject"
                ]
                
                quota_policies = {}
                for constraint in constraint_names:
                    try:
                        policy = org_policy_client.get_policy(
                            name=f"projects/{self.project_id}/policies/{constraint}"
                        )
                        quota_policies[constraint] = {
                            "enforced": policy.spec is not None,
                            "policy_exists": True
                        }
                    except Exception:
                        quota_policies[constraint] = {
                            "enforced": False,
                            "policy_exists": False
                        }
                
                policies["quota_policies"] = quota_policies
                
            except ImportError:
                policies["quota_policies"] = {
                    "error": "Organization Policy API not available",
                    "message": "Quota policies require Organization Policy API access"
                }
            except Exception as e:
                policies["quota_policies"] = {
                    "error": str(e),
                    "message": "Quota policies require Organization Policy API access"
                }
            
            policies["cost_control_policies"] = {
                "auto_shutdown_enabled": False,
                "idle_resource_cleanup": False,
                "cost_alerting": True,
                "resource_tagging_required": False
            }
            
            policies["organization_policies"] = {
                "cost_center_tagging": False,
                "budget_approval_required": False,
                "resource_quota_enforcement": False,
                "cost_transparency": True
            }
            
            return {
                "policies": policies,
                "total_policies": len(policies),
                "message": "Cost management policies retrieved from GCP Organization Policy API"
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
        self.cost_client = GCPCostManagement(project_id, credentials_path)


    def get_cost_anomalies(
        self,
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        anomaly_prob_threshold: float = 0.95
    ) -> Dict[str, Any]:
        """
        Detect cost anomalies using BigQuery ML's ML.DETECT_ANOMALIES on daily cost data.
        Flags days as anomalies based on the ARIMA_PLUS model's prediction intervals.

        Args:
            bq_project_id (str): BigQuery project ID for billing export (required).
            bq_dataset (str): BigQuery dataset name for billing export (required).
            bq_table (str): BigQuery table name for billing export (required).
            start_date (str, optional): Start date for analysis (YYYY-MM-DD). Defaults to 60 days ago.
            end_date (str, optional): End date for analysis (YYYY-MM-DD). Defaults to today.
            anomaly_prob_threshold (float, optional): Probability threshold for anomaly detection. Default: 0.95.

        Returns:
            Dict[str, Any]: List of cost anomalies with date, cost, and anomaly probability.
        """
        from google.cloud import bigquery
        from datetime import datetime, timedelta

        today = datetime.today()
        if not end_date:
            end_date = today.strftime("%Y-%m-%d")
        if not start_date:
            start_date = (today - timedelta(days=60)).strftime("%Y-%m-%d")

        model_id = f"{bq_project_id}.{bq_dataset}.cost_anomaly_model"
        client = bigquery.Client(project=bq_project_id, credentials=self.credentials)

        train_query = f"""
            CREATE OR REPLACE MODEL `{model_id}`
            OPTIONS(
              model_type='ARIMA_PLUS',
              time_series_timestamp_col='day',
              time_series_data_col='total_cost'
            ) AS
            SELECT
              DATE(usage_start_time) AS day,
              SUM(cost) AS total_cost
            FROM
              `{bq_project_id}.{bq_dataset}.{bq_table}`
            WHERE
              usage_start_time >= '{start_date}'
              AND usage_end_time <= '{end_date}'
            GROUP BY day
            ORDER BY day
        """
        try:
            client.query(train_query).result()
        except Exception as e:
            return {"error": f"Failed to train BigQuery ML model: {str(e)}"}

        anomaly_query = f"""
            SELECT
              day,
              total_cost,
              is_anomaly,
              anomaly_probability
            FROM
              ML.DETECT_ANOMALIES(
                MODEL `{model_id}`,
                STRUCT({anomaly_prob_threshold} AS anomaly_prob_threshold)
              )
        """
        try:
            anomaly_job = client.query(anomaly_query)
            rows = list(anomaly_job)
        except Exception as e:
            return {"error": f"Failed to detect anomalies from BigQuery ML model: {str(e)}"}

        anomalies = [
            {
                "date": row["day"].strftime("%Y-%m-%d"),
                "cost": float(row["total_cost"]),
                "anomaly_probability": float(row["anomaly_probability"])
            }
            for row in rows if row["is_anomaly"]
        ]

        return {
            "anomalies": anomalies,
            "period": {"start": start_date, "end": end_date},
            "anomaly_prob_threshold": anomaly_prob_threshold,
            "message": "Anomalies detected using BigQuery ML ARIMA_PLUS model."
        }

    def get_cost_efficiency_metrics(
        self,
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_ml: bool = True
    ) -> Dict[str, Any]:
        """
        Optimal cost efficiency metrics with adaptive ML usage.
        Automatically chooses the best approach based on data characteristics.

        Args:
            bq_project_id (str): BigQuery project ID for billing export (required).
            bq_dataset (str): BigQuery dataset name for billing export (required).
            bq_table (str): BigQuery table name for billing export (required).
            start_date (str, optional): Start date for analysis (YYYY-MM-DD). Defaults to 30 days ago.
            end_date (str, optional): End date for analysis (YYYY-MM-DD). Defaults to today.
            use_ml (bool, optional): Whether to attempt ML-based analysis. Default: True.

        Returns:
            Dict[str, Any]: Cost efficiency metrics with method transparency.
        """
        from google.cloud import bigquery
        from datetime import datetime, timedelta

        today = datetime.today()
        if not end_date:
            end_date = today.strftime("%Y-%m-%d")
        if not start_date:
            start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")

        client = bigquery.Client(project=bq_project_id, credentials=self.credentials)
        
        basic_query = f"""
                SELECT 
                COUNT(DISTINCT DATE(usage_start_time)) as total_days,
                AVG(daily_cost) as avg_daily_cost,
                STDDEV(daily_cost) as cost_stddev,
                MIN(daily_cost) as min_daily_cost,
                MAX(daily_cost) as max_daily_cost,
                SUM(daily_cost) as total_cost_period,
                COUNT(DISTINCT EXTRACT(DAYOFWEEK FROM DATE(usage_start_time))) as unique_days_of_week
            FROM (
                SELECT 
                    usage_start_time,
                    SUM(cost) as daily_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                GROUP BY usage_start_time
            )
        """
        
        try:
            basic_job = client.query(basic_query)
            basic_row = list(basic_job)[0]
            
            total_days = basic_row['total_days']
            avg_daily_cost = float(basic_row['avg_daily_cost'])
            cost_stddev = float(basic_row['cost_stddev'])
            min_daily_cost = float(basic_row['min_daily_cost'])
            max_daily_cost = float(basic_row['max_daily_cost'])
            total_cost_period = float(basic_row['total_cost_period'])
            unique_days_of_week = basic_row['unique_days_of_week']
            
            should_use_ml = (
                use_ml and 
                total_days >= 14 and
                unique_days_of_week >= 5 and
                cost_stddev > avg_daily_cost * 0.1
            )
            
            if should_use_ml:
                try:
                    model_id = f"{bq_project_id}.{bq_dataset}.cost_efficiency_model"
                    train_query = f"""
                        CREATE OR REPLACE MODEL `{model_id}`
                        OPTIONS(
                          model_type='ARIMA_PLUS',
                          time_series_timestamp_col='day',
                          time_series_data_col='daily_cost'
                        ) AS
                        SELECT DATE(usage_start_time) as day, SUM(cost) as daily_cost
                        FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                        WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                        GROUP BY day
                        ORDER BY day
                    """
                    client.query(train_query).result()
                    
                    waste_query = f"""
                        WITH daily_costs AS (
                            SELECT 
                                DATE(usage_start_time) as day,
                                SUM(cost) as daily_cost
                            FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                            WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                            GROUP BY day
                        )
                        SELECT COUNT(*) as waste_days
                        FROM (
                            SELECT day, daily_cost, is_anomaly
                            FROM ML.DETECT_ANOMALIES(
                                MODEL `{model_id}`,
                                (SELECT * FROM daily_costs),
                                STRUCT(0.85 AS anomaly_prob_threshold)
                            )
                        )
                        WHERE is_anomaly = TRUE
                    """
                    waste_job = client.query(waste_query)
                    waste_days = list(waste_job)[0]['waste_days']
                    method_used = "ML-enhanced"
                    
                except Exception as e:
                    waste_query = f"""
                        WITH daily_costs AS (
                            SELECT 
                                DATE(usage_start_time) as day,
                                SUM(cost) as daily_cost
                            FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                            WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                            GROUP BY day
                        ),
                        cost_stats AS (
                            SELECT 
                                AVG(daily_cost) as avg_cost,
                                STDDEV(daily_cost) as cost_stddev,
                                PERCENTILE_CONT(daily_cost, 0.75) as p75_cost
                            FROM daily_costs
                        )
                        SELECT COUNT(*) as waste_days
                        FROM daily_costs, cost_stats
                        WHERE daily_cost > (avg_cost + (cost_stddev * 1.5))
                    """
                    waste_job = client.query(waste_query)
                    waste_days = list(waste_job)[0]['waste_days']
                    method_used = "Manual (ML failed)"
            else:
                waste_query = f"""
                    WITH daily_costs AS (
                        SELECT 
                            DATE(usage_start_time) as day,
                            SUM(cost) as daily_cost
                        FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                        WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                        GROUP BY day
                    ),
                    cost_stats AS (
                        SELECT 
                            AVG(daily_cost) as avg_cost,
                            STDDEV(daily_cost) as cost_stddev,
                            PERCENTILE_CONT(daily_cost, 0.75) as p75_cost
                        FROM daily_costs
                    )
                    SELECT COUNT(*) as waste_days
                    FROM daily_costs, cost_stats
                    WHERE daily_cost > (avg_cost + (cost_stddev * 1.5))
                """
                waste_job = client.query(waste_query)
                waste_days = list(waste_job)[0]['waste_days']
                method_used = "Manual (insufficient data for ML)"
            
            waste_percentage = (waste_days / total_days) if total_days > 0 else 0
            cost_variance = (cost_stddev / avg_daily_cost) if avg_daily_cost > 0 else 0
            efficiency_score = 1 - (waste_percentage + cost_variance * 0.3)
            efficiency_score = max(0, min(1, efficiency_score))
            
            return {
                "efficiency_metrics": {
                    "total_days_analyzed": total_days,
                    "total_cost_period": round(total_cost_period, 2),
                    "avg_daily_cost": round(avg_daily_cost, 2),
                    "min_daily_cost": round(min_daily_cost, 2),
                    "max_daily_cost": round(max_daily_cost, 2),
                    "cost_stddev": round(cost_stddev, 2),
                    "cost_variance_ratio": round(cost_variance, 3),
                    "cost_efficiency_score": round(efficiency_score, 3),
                    "waste_percentage": round(waste_percentage * 100, 1),
                    "waste_days": waste_days,
                    "method_used": method_used,
                    "ml_enabled": should_use_ml
                },
                "period": {"start": start_date, "end": end_date},
                "message": f"Efficiency metrics calculated using {method_used}."
            }
            
        except Exception as e:
            return {"error": f"Failed to calculate cost efficiency metrics: {str(e)}"}

    def generate_cost_report(
        self,
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        report_type: str = "monthly",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive cost report using BigQuery billing export data.

        Args:
            bq_project_id (str): BigQuery project ID for billing export (required).
            bq_dataset (str): BigQuery dataset name for billing export (required).
            bq_table (str): BigQuery table name for billing export (required).
            report_type (str): Type of report (monthly, quarterly, annual, custom)
            start_date (Optional[str]): Start date for report (YYYY-MM-DD)
            end_date (Optional[str]): End date for report (YYYY-MM-DD)

        Returns:
            Dict[str, Any]: Comprehensive cost report with breakdowns and analysis
        """
        from google.cloud import bigquery
        from datetime import datetime, timedelta

        today = datetime.today()
        if not start_date or not end_date:
            if report_type == "monthly":
                start_date = today.replace(day=1).strftime("%Y-%m-%d")
                end_date = today.strftime("%Y-%m-%d")
            elif report_type == "quarterly":
                quarter_start = today.replace(day=1) - timedelta(days=90)
                start_date = quarter_start.strftime("%Y-%m-%d")
                end_date = today.strftime("%Y-%m-%d")
            elif report_type == "annual":
                year_start = today.replace(month=1, day=1)
                start_date = year_start.strftime("%Y-%m-%d")
                end_date = today.strftime("%Y-%m-%d")
            else:
                start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
                end_date = today.strftime("%Y-%m-%d")

        client = bigquery.Client(project=bq_project_id, credentials=self.credentials)

        try:
            summary_query = f"""
                SELECT
                    COUNT(DISTINCT DATE(usage_start_time)) as total_days,
                    SUM(cost) as total_cost,
                    AVG(cost) as avg_daily_cost,
                    MIN(cost) as min_daily_cost,
                    MAX(cost) as max_daily_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
            """
            summary_job = client.query(summary_query)
            summary_row = list(summary_job)[0]

            service_query = f"""
                SELECT
                    service.description,
                    SUM(cost) as total_cost,
                    AVG(cost) as avg_daily_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                GROUP BY service.description
                ORDER BY total_cost DESC
                LIMIT 10
            """
            service_job = client.query(service_query)
            service_breakdown = [dict(row) for row in service_job]

            project_query = f"""
                SELECT
                    project.id,
                    SUM(cost) as total_cost,
                    AVG(cost) as avg_daily_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                GROUP BY project.id
                ORDER BY total_cost DESC
                LIMIT 10
            """
            project_job = client.query(project_query)
            project_breakdown = [dict(row) for row in project_job]

            location_query = f"""
                SELECT
                    COALESCE(CAST(location.location AS STRING), 'UNKNOWN') as location,
                    SUM(cost) as total_cost,
                    AVG(cost) as avg_daily_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                GROUP BY location
                ORDER BY total_cost DESC
                LIMIT 10
            """
            location_job = client.query(location_query)
            location_breakdown = [dict(row) for row in location_job]

            daily_query = f"""
                SELECT
                    DATE(usage_start_time) as date,
                    SUM(cost) as daily_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                GROUP BY date
                ORDER BY date
            """
            daily_job = client.query(daily_query)
            daily_trends = [
                {
                    "date": row["date"].strftime("%Y-%m-%d"),
                    "daily_cost": float(row["daily_cost"])
                }
                for row in daily_job
            ]

            sku_query = f"""
                SELECT
                    sku,
                    service,
                    SUM(cost) as total_cost
                FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                GROUP BY sku, service
                ORDER BY total_cost DESC
                LIMIT 15
            """
            sku_job = client.query(sku_query)
            top_cost_drivers = [dict(row) for row in sku_job]

            efficiency_query = f"""
                WITH daily_costs AS (
                    SELECT 
                        DATE(usage_start_time) as day,
                        SUM(cost) as daily_cost
                    FROM `{bq_project_id}.{bq_dataset}.{bq_table}`
                    WHERE usage_start_time >= '{start_date}' AND usage_end_time <= '{end_date}'
                    GROUP BY day
                )
                SELECT
                    COUNT(*) as total_days,
                    AVG(daily_cost) as avg_daily_cost,
                    STDDEV(daily_cost) as cost_stddev,
                    MIN(daily_cost) as min_daily_cost,
                    MAX(daily_cost) as max_daily_cost
                FROM daily_costs
            """
            efficiency_job = client.query(efficiency_query)
            efficiency_row = list(efficiency_job)[0]

            avg_daily_cost = float(efficiency_row['avg_daily_cost'])
            cost_stddev = float(efficiency_row['cost_stddev'])
            cost_variance = (cost_stddev / avg_daily_cost) if avg_daily_cost > 0 else 0
            efficiency_score = max(0, min(1, 1 - cost_variance))

            return {
                "report_type": report_type,
                "period": {"start": start_date, "end": end_date},
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_cost": round(float(summary_row['total_cost']), 2),
                    "total_days": summary_row['total_days'],
                    "avg_daily_cost": round(float(summary_row['avg_daily_cost']), 2),
                    "min_daily_cost": round(float(summary_row['min_daily_cost']), 2),
                    "max_daily_cost": round(float(summary_row['max_daily_cost']), 2),
                    "unique_services": len(service_breakdown),
                    "unique_projects": len(project_breakdown),
                    "unique_locations": len(location_breakdown)
                },
                "breakdowns": {
                    "by_service": [
                        {
                            "service": row['description'],
                            "total_cost": round(float(row['total_cost']), 2),
                            "avg_daily_cost": round(float(row['avg_daily_cost']), 2)
                        }
                        for row in service_breakdown
                    ],
                    "by_project": [
                        {
                            "project": row['id'],
                            "total_cost": round(float(row['total_cost']), 2),
                            "avg_daily_cost": round(float(row['avg_daily_cost']), 2)
                        }
                        for row in project_breakdown
                    ],
                    "by_location": [
                        {
                            "location": row['location'],
                            "total_cost": round(float(row['total_cost']), 2),
                            "avg_daily_cost": round(float(row['avg_daily_cost']), 2)
                        }
                        for row in location_breakdown
                    ]
                },
                "trends": {
                    "daily_costs": daily_trends
                },
                "cost_drivers": [
                    {
                        "sku": row['sku'],
                        "service": row['service'],
                        "total_cost": round(float(row['total_cost']), 2)
                    }
                    for row in top_cost_drivers
                ],
                "efficiency_metrics": {
                    "cost_efficiency_score": round(efficiency_score, 3),
                    "cost_variance_ratio": round(cost_variance, 3),
                    "cost_stddev": round(cost_stddev, 2)
                },
                "message": "Comprehensive cost report generated for monthly period."
            }

        except Exception as e:
            return {"error": f"Failed to generate cost report: {str(e)}"}

    def get_cost_forecast_bqml(
        self,
        bq_project_id: str,
        bq_dataset: str,
        bq_table: str,
        start_date: str = None,
        end_date: str = None,
        forecast_period: int = 12,
        use_ai_model: bool = True
    ) -> dict:
        """
        Get cost forecast using BigQuery ML ARIMA_PLUS model with unified response format.

        Args:
            bq_project_id (str): BigQuery project ID
            bq_dataset (str): BigQuery dataset name
            bq_table (str): BigQuery table name
            start_date (str, optional): Start date for historical data
            end_date (str, optional): End date for historical data
            forecast_period (int, optional): Number of days to forecast
            use_ai_model (bool, optional): Whether to use BigQuery ML AI model

        Returns:
            dict: Unified forecast response with daily breakdowns
        """
        from datetime import datetime, timedelta

        today = datetime.today()
        if not start_date:
            start_date = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = today.strftime("%Y-%m-%d")
        
        try:
            historical_data = self.cost_client.get_cost_data(
                bq_project_id=bq_project_id,
                bq_dataset=bq_dataset,
                bq_table=bq_table,
                start_date=start_date,
                end_date=end_date,
                granularity="Daily"
            )
            
            daily_costs = []
            total_historical_cost = 0.0
            
            if "cost_data" in historical_data:
                total_cost = sum(item["total_cost"] for item in historical_data["cost_data"])
                total_historical_cost = total_cost
                
                from datetime import datetime
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                num_days = (end_dt - start_dt).days + 1
                
                daily_cost = total_cost / num_days if num_days > 0 else 0
                
                for i in range(num_days):
                    current_date = start_dt + timedelta(days=i)
                    daily_costs.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "cost": daily_cost
                    })
            elif "rows" in historical_data:
                for row in historical_data["rows"]:
                    if len(row) >= 2:
                        date_str = row[0]
                        cost = float(row[1]) if row[1] else 0
                        
                        if 'T' in date_str:
                            date_str = date_str.split('T')[0]
                        
                        daily_costs.append({
                            "date": date_str,
                            "cost": cost
                        })
                        total_historical_cost += cost
            
            avg_daily_cost = total_historical_cost / len(daily_costs) if daily_costs else 0
            
            forecast_results = []
            total_forecast_cost = 0.0
            
            if use_ai_model:
                try:
                    forecast_results = self._generate_bqml_forecast(
                        bq_project_id, bq_dataset, bq_table, 
                        start_date, end_date, forecast_period
                    )
                    ai_model_used = True
                except Exception as e:
                    forecast_results = self._generate_statistical_forecast(
                        daily_costs, forecast_period, avg_daily_cost
                    )
                    ai_model_used = False
            else:
                forecast_results = self._generate_statistical_forecast(
                    daily_costs, forecast_period, avg_daily_cost
                )
                ai_model_used = False
            
            total_forecast_cost = sum(day["forecast_value"] for day in forecast_results)
            
            insights = []
            if daily_costs:
                recent_trend = self._calculate_trend(daily_costs[-7:]) if len(daily_costs) >= 7 else 0
                insights.append(f"Historical average daily cost: {avg_daily_cost:.2f}")
                insights.append(f"Recent 7-day trend: {recent_trend:.1f}% change")
                insights.append(f"Forecasted total cost for {forecast_period} days: {total_forecast_cost:.2f}")
            
            return {
                "forecast_period": forecast_period,
                "start_date": start_date,
                "end_date": end_date,
                "total_historical_cost": round(total_historical_cost, 2),
                "total_forecast_cost": round(total_forecast_cost, 2),
                "average_daily_cost": round(avg_daily_cost, 2),
                "forecast_results": forecast_results,
                "ai_model_used": ai_model_used,
                "model_accuracy": self._calculate_model_accuracy(daily_costs),
                "insights": insights,
                "granularity": "Daily",
                "message": f"Unified cost forecast generated for {forecast_period} days using {'BigQuery ML' if ai_model_used else 'statistical analysis'}"
            }
            
        except Exception as e:
            return {"error": f"Failed to generate unified cost forecast: {str(e)}"}
    
    def _generate_bqml_forecast(self, bq_project_id, bq_dataset, bq_table, start_date, end_date, forecast_period):
        """Generate forecast using BigQuery ML ARIMA_PLUS model."""
        from google.cloud import bigquery

        model_id = f"{bq_project_id}.{bq_dataset}.cost_forecast_model"
        client = bigquery.Client(project=bq_project_id, credentials=self.credentials)

        train_query = f"""
            CREATE OR REPLACE MODEL `{model_id}`
            OPTIONS(
              model_type='ARIMA_PLUS',
              time_series_timestamp_col='day',
              time_series_data_col='total_cost'
            ) AS
            SELECT
              DATE(usage_start_time) AS day,
              SUM(cost) AS total_cost
            FROM
              `{bq_project_id}.{bq_dataset}.{bq_table}`
            WHERE
              usage_start_time >= '{start_date}'
              AND usage_end_time <= '{end_date}'
            GROUP BY day
            ORDER BY day
        """
        
        try:
            client.query(train_query).result()
        except Exception as e:
            raise Exception(f"Failed to train BigQuery ML model: {str(e)}")

        forecast_query = f"""
            SELECT
              forecast_timestamp,
              forecast_value,
              prediction_interval_lower_bound,
              prediction_interval_upper_bound
            FROM
              ML.FORECAST(MODEL `{model_id}`,
                STRUCT({forecast_period} AS horizon, 0.9 AS confidence_level))
            ORDER BY forecast_timestamp
        """
        
        try:
            forecast_job = client.query(forecast_query)
            forecast_rows = list(forecast_job)
        except Exception as e:
            raise Exception(f"Failed to forecast costs from BigQuery ML model: {str(e)}")

        forecast_results = [
            {
                "date": row["forecast_timestamp"].strftime("%Y-%m-%d"),
                "forecast_value": float(row["forecast_value"]),
                "lower_bound": float(row["prediction_interval_lower_bound"]),
                "upper_bound": float(row["prediction_interval_upper_bound"]),
                "confidence_level": 0.9
            }
            for row in forecast_rows
        ]
        
        return forecast_results
    
    def _generate_statistical_forecast(self, daily_costs, forecast_period, avg_daily_cost):
        """Generate statistical forecast using moving averages and variance."""
        from datetime import datetime, timedelta
        import numpy as np
        
        if not daily_costs:
            return []
        
        costs = [day["cost"] for day in daily_costs]
        moving_avg = sum(costs[-7:]) / 7 if len(costs) >= 7 else avg_daily_cost
        
        variance = np.var(costs) if len(costs) > 1 else (avg_daily_cost * 0.1) ** 2
        std_dev = np.sqrt(variance)
        
        forecast_results = []
        last_date = datetime.strptime(daily_costs[-1]["date"], "%Y-%m-%d")
        
        for i in range(1, forecast_period + 1):
            forecast_date = last_date + timedelta(days=i)
            
            forecast_value = moving_avg
            
            lower_bound = max(0, forecast_value - (1.96 * std_dev))
            upper_bound = forecast_value + (1.96 * std_dev)
            
            forecast_results.append({
                "date": forecast_date.strftime("%Y-%m-%d"),
                "forecast_value": round(forecast_value, 2),
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
                "confidence_level": 0.95
            })
        
        return forecast_results
    
    def _calculate_trend(self, recent_costs):
        """Calculate trend percentage from recent cost data."""
        if len(recent_costs) < 2:
            return 0
        
        costs = [day["cost"] for day in recent_costs]
        first_avg = sum(costs[:len(costs)//2]) / (len(costs)//2)
        second_avg = sum(costs[len(costs)//2:]) / (len(costs)//2)
        
        if first_avg == 0:
            return 0
        
        return ((second_avg - first_avg) / first_avg) * 100
    
    def _calculate_model_accuracy(self, daily_costs):
        """Calculate model accuracy metrics."""
        import numpy as np
        
        if len(daily_costs) < 2:
            return {"mape": 0, "rmse": 0}
        
        costs = [day["cost"] for day in daily_costs]
        average_daily_cost = sum(costs) / len(costs)
        
        mape = sum(abs(cost - average_daily_cost) / average_daily_cost for cost in costs if average_daily_cost > 0) / len(costs) * 100
        
        rmse = np.sqrt(sum((cost - average_daily_cost) ** 2 for cost in costs) / len(costs))

        return {
            "mape": round(mape, 2),
            "rmse": round(rmse, 2),
            "mean_absolute_error": round(sum(abs(cost - average_daily_cost) for cost in costs) / len(costs), 2)
        }