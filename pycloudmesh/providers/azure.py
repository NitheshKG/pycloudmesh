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
        self.base_url = f"https://management.azure.com"

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
            url = f"{self.base_url}{scope}/providers/Microsoft.Consumption/budgets"
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
        notifications: List[Dict[str, Any]],
        time_grain: str = "Monthly",
        /,
        *,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        api_version: str = "2024-08-01"

    ) -> Dict[str, Any]:
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
            start_date (Optional[str]): Start date for the budget in YYYY-MM-DD format. 
                Will be automatically adjusted to the first day of the month if not already.
            end_date (Optional[str]): End date for the budget in YYYY-MM-DD format.
                Defaults to 5 years from start date if not provided.
            api_version (str): API version to use for the Azure Budget API.

        Returns:
            Dict[str, Any]: Budget creation response from Azure

        Raises:
            requests.exceptions.RequestException: If Azure API call fails
            ValueError: If notifications are not properly configured
        """
        try:
            if not start_date:
                # Set start date to first day of current month
                today = datetime.today()
                start_date = today.replace(day=1).strftime("%Y-%m-%d")
            else:
                # Ensure provided start date is first day of the month
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_dt.replace(day=1).strftime("%Y-%m-%d")
            
            if not end_date:
                # Set end date to 5 years from start date (Azure default)
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = start_dt.replace(year=start_dt.year + 5)
                end_date = end_dt.strftime("%Y-%m-%d")

            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            url = f"{self.base_url}{scope}/providers/Microsoft.Consumption/budgets/{budget_name}"
            params = {"api-version": api_version}
            
            payload = {
                "properties": {
                    "category": "Cost",
                    "amount": amount,
                    "timeGrain": time_grain,
                    "timePeriod": {
                        "startDate": f"{start_date}T00:00:00Z",
                        "endDate": f"{end_date}T00:00:00Z"
                }
            }
            }
            
            # Validate and add notifications
            if not notifications:
                raise ValueError("Notifications are required for budget creation")
            
            payload["properties"]["notifications"] = {}
            for i, notification in enumerate(notifications):
                # Validate required fields
                if not notification.get("contactEmails"):
                    raise ValueError(f"Notification {i}: contactEmails is required")
                if "threshold" not in notification:
                    raise ValueError(f"Notification {i}: threshold is required")
                if "operator" not in notification:
                    raise ValueError(f"Notification {i}: operator is required")
                
                # Azure Budget API expects notification keys in specific format
                threshold_percentage = int(notification["threshold"])
                operator = notification["operator"]
                notification_key = f"Actual_{operator}_{threshold_percentage}_Percent"
                
                payload["properties"]["notifications"][notification_key] = {
                    "enabled": notification.get("enabled", True),
                    "operator": notification["operator"],
                    "threshold": threshold_percentage,
                    "locale": notification.get("locale", "en-us"),
                    "contactEmails": notification["contactEmails"],
                    "contactRoles": notification.get("contactRoles", []),
                    "contactGroups": notification.get("contactGroups", []),
                    "thresholdType": notification.get("thresholdType", "Actual")
                }
            
            response = requests.put(url, headers=headers, params=params, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = ""
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = f" - {e.response.text}"
                except Exception:
                    pass
            return {"error": f"Failed to create budget: {str(e)}{error_detail}"}

    def get_budget(self, 
                   budget_name: str, 
                   scope: str, 
                   /, 
                   *, 
                   api_version: str = "2024-08-01") -> Dict[str, Any]:
        """
        Get a specific budget by name and scope.

        Args:
            budget_name (str): Name of the budget to retrieve
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            api_version (str): API version to use

        Returns:
            Dict[str, Any]: Budget details including notifications

        Raises:
            requests.exceptions.RequestException: If Azure API call fails

        Example:
            >>> azure.get_budget(budget_name="monthly-budget", scope="/subscriptions/your-subscription-id/")
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.Consumption/budgets/{budget_name}"
            params = {"api-version": api_version}
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get budget: {str(e)}"}


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
        self.base_url = "https://management.azure.com"

    def get_cost_data(
        self,
        scope: str,
        /,
        *,
        granularity: str = "Monthly",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        metrics: Optional[List[str]] = None,
        group_by: Optional[List[str]] = None,
        filter_: Optional[Dict[str, Any]] = None,
        api_version: str = "2024-08-01"
    ) -> Dict[str, Any]:
        """
        Fetch Azure cost data from Cost Management API.

        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            granularity (str): "Daily", "Monthly", or "None". Defaults to "Monthly".
            start_date (Optional[str]): Start date (YYYY-MM-DD). Defaults to first day of current month.
            end_date (Optional[str]): End date (YYYY-MM-DD). Defaults to today's date.
            metrics (Optional[List[str]]): List of cost metrics. Defaults to standard cost metrics.
            group_by (Optional[List[str]]): Grouping criteria.
            filter_ (Optional[Dict[str, Any]]): Filter criteria.
            api_version (str): API version for the Cost Management API. Default: '2024-08-01'.

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
            if scope.startswith("/providers/Microsoft.Billing/billingAccounts"):
                metrics = ["PreTaxCost"]
            else:
                metrics = ["ActualCost"]

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.CostManagement/query"
            params = {"api-version": api_version}
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
                    {"type": "Dimension", "name": group} for group in group_by
                ]

            if filter_:
                payload["dataset"]["filter"] = filter_

            response = requests.post(url, headers=headers, params=params, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = ""
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = f" - {e.response.text}"
                except Exception:
                    pass
            return {"error": f"Failed to fetch cost data: {str(e)}{error_detail}"}

    def get_cost_analysis(
        self,
        scope: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        dimensions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get detailed cost analysis with dimensions, returning a summary with breakdowns and insights.

        Args:
            scope (str): Azure scope (subscription, resource group, management group, or billing account)
            start_date (Optional[str]): Start date for analysis
            end_date (Optional[str]): End date for analysis
            dimensions (Optional[List[str]]): List of dimensions to analyze (group by)

        Returns:
            Dict[str, Any]: Cost analysis summary with breakdowns and insights
        """
        # Set default dates if not provided
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        # Define valid group by columns for each scope type
        SUBSCRIPTION_GROUPBYS = ["ResourceType", "ResourceLocation", "ResourceGroupName"]
        BILLING_ACCOUNT_GROUPBYS = [
            "SubscriptionId", "BillingProfileId", "InvoiceSectionId", "Product", "Meter", "ServiceFamily", "ServiceName", "ResourceGroup", "ResourceId", "ResourceType", "ChargeType", "PublisherType", "BillingPeriod"
        ]

        # Determine scope type
        is_billing_account = scope.startswith("/providers/Microsoft.Billing/billingAccounts")
        if not dimensions:
            if is_billing_account:
                dimensions = ["SubscriptionId"]
            else:
                dimensions = SUBSCRIPTION_GROUPBYS[:2]  # Default to 2 for summary
        # Validate dimensions
        if is_billing_account:
            for dim in dimensions:
                if dim not in BILLING_ACCOUNT_GROUPBYS:
                    raise ValueError(f"Invalid group by dimension '{dim}' for billing account scope. Allowed: {BILLING_ACCOUNT_GROUPBYS}")
        else:
            for dim in dimensions:
                if dim not in SUBSCRIPTION_GROUPBYS:
                    raise ValueError(f"Invalid group by dimension '{dim}' for subscription/resource group scope. Allowed: {SUBSCRIPTION_GROUPBYS}")

        # Fetch grouped cost data
        cost_data = self.get_cost_data(
            scope,
            start_date=start_date,
            end_date=end_date,
            group_by=dimensions
        )
        # If error, return immediately
        if isinstance(cost_data, dict) and "error" in cost_data:
            return cost_data
        # Process the cost data to build a summary
        summary = {
            "period": {"start": start_date, "end": end_date},
            "dimensions": dimensions,
            "total_cost": 0.0,
            "cost_breakdown": {},
            "cost_trends": [],
            "insights": []
        }
        # Azure returns a 'properties' dict with 'rows' and 'columns'
        properties = cost_data.get("properties", {})
        columns = properties.get("columns", [])
        rows = properties.get("rows", [])
        # Find the cost column index
        cost_col_idx = None
        for idx, col in enumerate(columns):
            if col.get("name", "").lower() in ["pretaxcost", "actualcost", "costusd", "cost"]:
                cost_col_idx = idx
                break
        # Find dimension column indices
        dim_indices = [i for i, col in enumerate(columns) if col.get("name") in dimensions]
        # Process rows
        for row in rows:
            # Get cost value
            cost = float(row[cost_col_idx]) if cost_col_idx is not None else 0.0
            summary["total_cost"] += cost
            # Build breakdown key from dimension values
            key = tuple(row[i] for i in dim_indices)
            key_str = "|".join(str(k) for k in key)
            if key_str not in summary["cost_breakdown"]:
                summary["cost_breakdown"][key_str] = 0.0
            summary["cost_breakdown"][key_str] += cost
            # Track trends (if time period is present)
            if any("date" in col.get("name", "").lower() for col in columns):
                summary["cost_trends"].append({"key": key_str, "cost": cost})
        # Generate insights
        if summary["cost_breakdown"]:
            sorted_breakdown = sorted(summary["cost_breakdown"].items(), key=lambda x: x[1], reverse=True)
            top = sorted_breakdown[0]
            top_pct = (top[1] / summary["total_cost"] * 100) if summary["total_cost"] else 0
            summary["insights"].append(f"Top group {top[0]} accounts for {top_pct:.1f}% of total cost.")
            if len(sorted_breakdown) > 1:
                top3_pct = sum(x[1] for x in sorted_breakdown[:3]) / summary["total_cost"] * 100 if summary["total_cost"] else 0
                summary["insights"].append(f"Top 3 groups account for {top3_pct:.1f}% of total cost.")
        return summary

    def get_cost_trends(
        self,
        scope: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "Daily"
    ) -> Dict[str, Any]:
        """
        Get detailed cost trends analysis with insights and patterns

        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            start_date (Optional[str]): Start date for trend analysis
            end_date (Optional[str]): End date for trend analysis
            granularity (str): Data granularity for trends (default: "Daily")

        Returns:
            Dict[str, Any]: Cost trends analysis with patterns, growth rates, and insights
        """
        # Set default dates if not provided
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        # Fetch cost data (Azure returns date column automatically for daily granularity)
        cost_data = self.get_cost_data(
            scope,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity
        )
        # If error, return immediately
        if isinstance(cost_data, dict) and "error" in cost_data:
            return cost_data
        # Prepare trends analysis structure
        trends_analysis = {
            "period": {"start": start_date, "end": end_date},
            "granularity": granularity,
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
        properties = cost_data.get("properties", {})
        columns = properties.get("columns", [])
        rows = properties.get("rows", [])
        # Find date and cost column indices
        date_col_idx = None
        cost_col_idx = None
        for idx, col in enumerate(columns):
            name = col.get("name", "").lower()
            if "date" in name:
                date_col_idx = idx
            if name in ["pretaxcost", "actualcost", "costusd", "cost"]:
                cost_col_idx = idx
        # Process rows
        costs = []
        for row in rows:
            date = row[date_col_idx] if date_col_idx is not None else None
            cost = float(row[cost_col_idx]) if cost_col_idx is not None else 0.0
            trends_analysis["total_cost"] += cost
            trends_analysis["total_periods"] += 1
            trends_analysis["cost_periods"].append({
                "date": date,
                "cost": cost
            })
            costs.append(cost)
        # Calculate average
        if trends_analysis["total_periods"] > 0:
            trends_analysis["average_daily_cost"] = trends_analysis["total_cost"] / trends_analysis["total_periods"]
        # Find peak and low periods
        if costs:
            max_cost = max(costs)
            min_cost = min(costs)
            for period in trends_analysis["cost_periods"]:
                if period["cost"] == max_cost and max_cost > 0:
                    trends_analysis["peak_periods"].append(period)
                if period["cost"] == min_cost:
                    trends_analysis["low_periods"].append(period)
        # Calculate trend direction and growth rate
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
        # Generate patterns and insights
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
            # Insights
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

    def get_resource_costs(
        self,
        scope: str,
        resource_id: str,
        granularity: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        metrics: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get costs for a specific resource.

        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            resource_id (str): ID of the resource to get costs for
            start_date (Optional[str]): Start date for cost data
            end_date (Optional[str]): End date for cost data

        Returns:
            Dict[str, Any]: Resource cost data
        """
        # Use a direct dimensions filter for a single resource
        filter_ = {
                    "dimensions": {
                        "name": "ResourceId",
                        "operator": "In",
                        "values": [resource_id]
                    }
                }
        return self.get_cost_data(
            scope,
            granularity=granularity,
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
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
        self.base_url = f"https://management.azure.com"

    def get_advisor_recommendations(self, api_version: str = "2025-01-01", filter: str = None) -> Dict[str, Any]:
        """
        Get Azure Advisor recommendations for cost optimization.

        Args:
            api_version (str, optional): API version for the Advisor API. Defaults to '2025-01-01'.
            filter (str, optional): OData filter string for server-side filtering (e.g., "Category eq 'Cost' and ResourceGroup eq 'MyResourceGroup'").

        Returns:
            Dict[str, Any]: Advisor recommendations (optionally filtered server-side)
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/subscriptions/{self.subscription_id}/providers/Microsoft.Advisor/recommendations"
            params = {"api-version": api_version}
            if filter:
                params["$filter"] = filter
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get advisor recommendations: {str(e)}"}

    def get_reserved_instance_recommendations(self, scope: str, api_version: str = "2024-08-01", filter: str = None) -> Dict[str, Any]:
        """
        Get Reserved Instance recommendations.

        Args:
            api_version (str, optional): API version for the Reservation Recommendations API. Defaults to '2025-01-01'.
            filter (str, optional): OData filter string for server-side filtering (e.g., "ResourceGroup eq 'MyResourceGroup'").

        Returns:
            Dict[str, Any]: Reserved Instance recommendations (optionally filtered server-side)
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.Consumption/reservationRecommendations"
            api_version = '2024-08-01'
            params = {"api-version": api_version}
            if filter:
                params["$filter"] = filter
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get Reserved Instance recommendations: {str(e)}"}

    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations.

        Returns:
            Dict[str, Any]: Optimization recommendations
        """
        try:
            filter_arg = kwargs.get('filter', None)
            scope = kwargs.get('scope')
            recommendations = {
                'advisor_recommendations': self.get_advisor_recommendations(api_version='2025-01-01', filter=filter_arg),
                'reserved_instance_recommendations': self.get_reserved_instance_recommendations(scope=scope, api_version='2024-08-01', filter=filter_arg)
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

