import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dateutil.relativedelta import relativedelta

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
        self.base_url = f"https://management.azure.com"

    def get_reservation_cost(
        self,
        scope: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get Azure reservation utilization and cost data.

        This method first retrieves reservation order details to get specific reservation IDs,
        then fetches detailed reservation information for each reservation.

        Args:
            start_date (Optional[str]): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (Optional[str]): End date in YYYY-MM-DD format. Defaults to last day of current month.

        Returns:
            Dict[str, Any]: Reservation utilization data including order details and individual reservation information.

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
            
            # Step 1: Get reservation order details
            reservation_orders_url = f"{self.base_url}{scope}/providers/Microsoft.Capacity/reservationOrders"
            reservation_orders_params = {"api-version": "2022-11-01"}
            
            reservation_orders_response = requests.get(
                reservation_orders_url, 
                headers=headers, 
                params=reservation_orders_params
            )
            reservation_orders_response.raise_for_status()
            reservation_orders_data = reservation_orders_response.json()
            
            # Step 2: Get detailed information for each reservation
            reservations_details = []
            for order in reservation_orders_data.get("value", []):
                order_id = order.get("name")  # This is the reservationOrderId
                reservations = order.get("properties", {}).get("reservations", [])
                
                for reservation in reservations:
                    reservation_id = reservation.get("id", "").split("/")[-1]  # Extract reservation ID from full path
                    
                    # Get detailed reservation information
                    reservation_detail_url = f"{self.base_url}{scope}/providers/Microsoft.Capacity/reservationOrders/{order_id}/reservations/{reservation_id}"
                    reservation_detail_params = {"api-version": "2022-11-01"}
                    
                    reservation_detail_response = requests.get(
                        reservation_detail_url,
                        headers=headers,
                        params=reservation_detail_params
                    )
                    reservation_detail_response.raise_for_status()
                    reservation_detail = reservation_detail_response.json()
                    
                    reservations_details.append({
                        "reservation_order_id": order_id,
                        "reservation_id": reservation_id,
                        "reservation_details": reservation_detail,
                        "order_details": order
                    })
            
            # Step 3: Get cost data for the reservation period
            cost_url = f"{self.base_url}/providers/Microsoft.CostManagement/query"
            cost_payload = {
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
            
            cost_response = requests.post(cost_url, headers=headers, json=cost_payload)
            cost_response.raise_for_status()
            cost_data = cost_response.json()
            
            return {
                "reservation_orders": reservation_orders_data,
                "reservations_details": reservations_details,
                "cost_data": cost_data,
                "period": {
                    "start_date": start_date,
                    "end_date": end_date
                },
                "total_reservations": len(reservations_details)
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch reservation utilization: {str(e)}"}

    def get_reservation_recommendation(self, scope: str, api_version: str = "2024-08-01", filter_param: str = None) -> List[Dict[str, Any]]:
        """
        Get Azure reservation recommendations for various services.

        This method retrieves reservation purchase recommendations based on your usage patterns.
        You can filter recommendations by various criteria using OData filter syntax.

        Args:
            scope (str): Azure scope (subscription, resource group, etc.).
                Example: "/subscriptions/{subscription-id}/"
            api_version (str, optional): API version for the Consumption API. Defaults to "2024-08-01".
            filter_param (str, optional): OData filter string for server-side filtering.
                Common filter examples:
                - "ResourceGroup eq 'MyResourceGroup'"
                - "Location eq 'eastus'"
                - "Sku eq 'Standard_D2s_v3'"
                - "Term eq 'P1Y'" (1 year term)
                - "Term eq 'P3Y'" (3 year term)

        Returns:
            List[Dict[str, Any]]: List of reservation recommendations with details including:
                - Resource group, location, SKU information
                - Recommended quantity and term
                - Potential savings
                - Usage data used for recommendations

        Raises:
            requests.exceptions.RequestException: If Azure API call fails

        Example:
            >>> # Get all recommendations for a subscription
            >>> recommendations = azure.get_reservation_recommendation(
            ...     scope="/subscriptions/your-subscription-id/"
            ... )
            
            >>> # Filter by resource group
            >>> recommendations = azure.get_reservation_recommendation(
            ...     scope="/subscriptions/your-subscription-id/",
            ...     filter_param="ResourceGroup eq 'Production'"
            ... )
            
            >>> # Filter by location and term
            >>> recommendations = azure.get_reservation_recommendation(
            ...     scope="/subscriptions/your-subscription-id/",
            ...     filter_param="Location eq 'eastus' and Term eq 'P1Y'"
            ... )
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.Consumption/reservationRecommendations"
            params = {"api-version": api_version}
            if filter_param:
                params["$filter"] = filter_param
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get("value", [])
        except requests.exceptions.RequestException as e:
            return [{"error": f"Failed to fetch reservation recommendations: {str(e)}"}]

    def get_azure_reservation_order_details(self, api_version: str) -> Dict[str, Any]:
        """
        Get Azure reservation order details.

        Returns:
            Dict[str, Any]: Reservation order details.
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/providers/Microsoft.Capacity/reservationOrders"
            
            params = {"api-version": api_version}
            response = requests.get(url, headers=headers, params=params)
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
                metrics = ["Cost"]

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
        self.base_url = f"https://management.azure.com"
        self.cost_client = AzureCostManagement(subscription_id, token)

    def get_policy_compliance(self, scope: Optional[str] = None) -> Dict[str, Any]:
        """
        Get policy compliance status with focus on cost-related policies for FinOps governance.

        Args:
            scope (Optional[str]): Azure scope to check compliance for. 
                If not provided, checks at subscription level.

        Returns:
            Dict[str, Any]: Policy compliance status with cost governance focus
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # Use provided scope or default to subscription
            if not scope:
                scope = f"/subscriptions/{self.subscription_id}"
            
            url = f"{self.base_url}{scope}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults"
            
            # Only use api-version in params
            params = {
                "api-version": "2019-10-01"
            }
            
            response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()
            policy_data = response.json()
            
            # Process and structure the response for FinOps relevance
            compliance_summary = {
                "scope": scope,
                "total_policies": 0,
                "compliant_resources": 0,
                "non_compliant_resources": 0,
                "cost_related_policies": [],
                "compliance_score": 0.0,
                "cost_governance_insights": []
            }
            
            # Extract policy states and analyze for cost relevance
            policy_states = policy_data.get("value", [])
            cost_related_categories = [
                "Cost Management", "Tagging", "Resource Management", 
                "Budget", "Quota", "Sizing", "Reservation"
            ]
            
            for policy_state in policy_states:
                policy_name = policy_state.get("policyDefinitionName", "")
                policy_category = policy_state.get("policyDefinitionGroupNames", [])
                compliance_state = policy_state.get("complianceState", "")
                
                # Check if policy is cost-related (by name or group/category)
                is_cost_related = any(
                    category.lower() in policy_name.lower() or 
                    any(cat.lower() in str(policy_category).lower() for cat in cost_related_categories)
                    for category in cost_related_categories
                )
                
                if is_cost_related:
                    compliance_summary["cost_related_policies"].append({
                        "policy_name": policy_name,
                        "compliance_state": compliance_state,
                        "category": policy_category,
                        "resource_count": policy_state.get("resourceCount", 0)
                    })
                
                # Count compliance
                if compliance_state == "Compliant":
                    compliance_summary["compliant_resources"] += policy_state.get("resourceCount", 0)
                else:
                    compliance_summary["non_compliant_resources"] += policy_state.get("resourceCount", 0)
            
            compliance_summary["total_policies"] = len(compliance_summary["cost_related_policies"])
            
            # Calculate compliance score
            total_resources = compliance_summary["compliant_resources"] + compliance_summary["non_compliant_resources"]
            if total_resources > 0:
                compliance_summary["compliance_score"] = (
                    compliance_summary["compliant_resources"] / total_resources * 100
                )
            
            # Generate cost governance insights
            if compliance_summary["total_policies"] > 0:
                non_compliant_policies = [
                    p for p in compliance_summary["cost_related_policies"] 
                    if p["compliance_state"] != "Compliant"
                ]
                
                if non_compliant_policies:
                    compliance_summary["cost_governance_insights"].append(
                        f"Found {len(non_compliant_policies)} non-compliant cost policies that may impact cost management"
                    )
                
                if compliance_summary["compliance_score"] < 80:
                    compliance_summary["cost_governance_insights"].append(
                        f"Low compliance score ({compliance_summary['compliance_score']:.1f}%) may indicate cost governance issues"
                    )
                else:
                    compliance_summary["cost_governance_insights"].append(
                        f"Good compliance score ({compliance_summary['compliance_score']:.1f}%) indicates effective cost governance"
                    )
            
            return compliance_summary
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get policy compliance: {str(e)}"}

    def get_available_tags(self, scope: str) -> Dict[str, Any]:
        """
        Get available resource tags for a given scope.
        
        Args:
            scope (str): Azure scope (subscription, resource group, etc.)

        Returns:
            Dict[str, Any]: Available resource tags for the scope
        """
        try:
            api_version = '2024-08-01'
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.Consumption/tags"
            params = {"api-version": api_version}
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get available tags: {str(e)}"}

    def get_costs_by_tags(self, scope: str, tag_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get costs grouped by tags for cost allocation analysis.
        
        Note: Azure Cost Management API has limited support for grouping by custom tags.
        This method will return available tags and cost data grouped by supported dimensions.

        Args:
            scope (str): Azure scope (subscription, resource group, etc.)
            tag_names (Optional[List[str]]): List of tag names to group by. 
                Note: Custom tags are not directly supported by Azure Cost Management API.

        Returns:
            Dict[str, Any]: Cost data and available tags with explanation of limitations

        Example:
            >>> # Get available tags and cost data
            >>> azure.get_costs_by_tags(
            ...     scope="/subscriptions/your-subscription-id/"
            ... )
        """
        try:
            # Get available tags
            available_tags = self.get_available_tags(scope)
            if "error" in available_tags:
                return available_tags
            
            # Extract tag names from the response
            tag_data = available_tags.get("properties", {}).get("tags", [])
            discovered_tags = []
            for tag_item in tag_data:
                if "key" in tag_item:
                    discovered_tags.append(tag_item["key"])
            
            # Get cost data grouped by supported dimensions instead of custom tags
            # Azure supports: ResourceGroup, ResourceType, ServiceName, etc.
            supported_groupings = ["ResourceGroup", "ServiceName", "ResourceType"]
            
            cost_data = self.cost_client.get_cost_data(
                scope,
                group_by=supported_groupings
            )
            
            return {
                "cost_allocation_by_tags": cost_data,
                "available_tags": available_tags,
                "discovered_tags": discovered_tags,
                "tags_used": tag_names if tag_names else discovered_tags,
                "supported_groupings": supported_groupings,
                "scope": scope,
                "note": "Azure Cost Management API doesn't support direct grouping by custom tags. Using supported dimensions instead."
            }
            
        except Exception as e:
            return {"error": f"Failed to get costs by tags: {str(e)}"}

    def get_cost_policies(self, scope: str) -> Dict[str, Any]:
        """
        Get cost management policies (filtered for cost-related only).

        Returns:
            Dict[str, Any]: Cost policies
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.Authorization/policyDefinitions"
            params = {"api-version": "2023-04-01"}
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            all_policies = response.json().get("value", [])

            # Filter for cost-related policies
            cost_keywords = ["cost", "budget", "tag", "quota", "spend", "billing", "reservation"]
            cost_policies = []
            for policy in all_policies:
                display_name = policy.get("properties", {}).get("displayName", "").lower()
                description = policy.get("properties", {}).get("description", "").lower()
                if any(keyword in display_name or keyword in description for keyword in cost_keywords):
                    cost_policies.append(policy)

            return {
                "total_cost_policies": len(cost_policies),
                "cost_policies": cost_policies
            }
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
        self.base_url = f"https://management.azure.com"
        self.cost_client = AzureCostManagement(subscription_id, token)

    def get_cost_forecast(
        self,
        scope: str,
        api_version: str,
        start_date: str = None,
        end_date: str = None,
        forecast_period: int = 12,
        payload: dict = None
    ) -> Dict[str, Any]:
        """
        Get cost forecast for the specified period.
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.CostManagement/forecast"

            # Clean default date logic
            if not start_date or not end_date:
                today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                start_date_dt = (today.replace(day=1) - relativedelta(months=3))
                start_date = start_date_dt.strftime("%Y-%m-%dT00:00:00+00:00")
                end_date = today.strftime("%Y-%m-%dT00:00:00+00:00")

            if not payload:
                payload = {
                        "type": "Usage",
                    "timeframe": "Custom",
                    "timePeriod": {
                        "from": start_date,
                        "to": end_date
                    },
                    "dataset": {
                            "granularity": "Daily",
                        "aggregation": {
                            "totalCost": {
                                    "name": "Cost",
                                "function": "Sum"
                            }
                        }
                    }
                }
            
            params = {"api-version": api_version}
            response = requests.post(url, headers=headers, params=params, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "status code": getattr(e.response, 'status_code', None),
                "Response": getattr(e.response, 'text', str(e)),
                "error": f"Failed to get cost forecast: {str(e)}"
            }

    def get_cost_anomalies(
        self,
        scope: str,
        start_date: str = None,
        end_date: str = None,
        api_version: str = "2023-03-01",
        payload: dict = None
    ) -> Dict[str, Any]:
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
        try:
            # Set default dates if not provided
            if not start_date or not end_date:
                today = datetime.utcnow()
                end_date = today.strftime("%Y-%m-%d")
                start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")

            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.CostManagement/query"
            params = {"api-version": api_version}
            
            # Use custom payload if provided, otherwise use default
            if not payload:
                payload = {
                    "type": "Usage",
                    "timeframe": "Custom",
                    "timePeriod": {
                        "from": start_date,
                        "to": end_date
                    },
                    "dataset": {
                        "granularity": "Daily",
                        "aggregation": {
                            "totalCost": {
                                "name": "Cost",
                                "function": "Sum"
                            }
                        }
                    }
                }
            
            response = requests.post(url, headers=headers, params=params, json=payload)
            response.raise_for_status()
            cost_data = response.json()
            
            # Analyze the cost data for anomalies
            anomalies = self._detect_anomalies(cost_data, start_date, end_date)
            
            return {
                "scope": scope,
                "period": {"start": start_date, "end": end_date},
                "anomalies": anomalies,
                "total_records": len(anomalies),
                "cost_data": cost_data
            }
            
        except Exception as e:
            return {"error": f"Failed to get cost anomalies: {str(e)}"}

    def _detect_anomalies(self, cost_data: Dict[str, Any], start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Analyze cost data to detect anomalies based on statistical patterns.
        
        Args:
            cost_data (Dict[str, Any]): Cost data from Azure Cost Management API
            start_date (str): Start date of analysis period
            end_date (str): End date of analysis period

        Returns:
            List[Dict[str, Any]]: List of detected anomalies
        """
        anomalies = []
        
        try:
            # Extract cost values from the response
            properties = cost_data.get("properties", {})
            rows = properties.get("rows", [])
            columns = properties.get("columns", [])
            
            if not rows or not columns:
                return anomalies
            
            # Find cost column index
            cost_col_idx = None
            date_col_idx = None
            for idx, col in enumerate(columns):
                name = col.get("name", "").lower()
                if name in ["cost", "pretaxcost", "costusd"]:
                    cost_col_idx = idx
                elif "date" in name:
                    date_col_idx = idx
            
            if cost_col_idx is None:
                return anomalies
            
            # Extract daily costs
            daily_costs = []
            for row in rows:
                if len(row) > max(cost_col_idx, date_col_idx or 0):
                    cost = float(row[cost_col_idx]) if row[cost_col_idx] else 0.0
                    date = row[date_col_idx] if date_col_idx is not None else None
                    daily_costs.append({"date": date, "cost": cost})
            
            if len(daily_costs) < 3:
                return anomalies
            
            # Calculate statistical measures for anomaly detection
            costs = [day["cost"] for day in daily_costs]
            mean_cost = sum(costs) / len(costs)
            variance = sum((cost - mean_cost) ** 2 for cost in costs) / len(costs)
            std_dev = variance ** 0.5
            
            # Define anomaly threshold (2 standard deviations from mean)
            threshold = 2 * std_dev
            
            # Detect anomalies
            for day in daily_costs:
                cost = day["cost"]
                deviation = abs(cost - mean_cost)
                
                if deviation > threshold and cost > 0:
                    anomaly_type = "spike" if cost > mean_cost else "drop"
                    severity = "high" if deviation > 3 * std_dev else "medium"
                    
                    anomalies.append({
                        "date": day["date"],
                        "cost": cost,
                        "expected_cost": round(mean_cost, 2),
                        "deviation": round(deviation, 2),
                        "deviation_percentage": round((deviation / mean_cost * 100) if mean_cost > 0 else 0, 2),
                        "type": anomaly_type,
                        "severity": severity,
                        "threshold": round(threshold, 2)
                    })
            
            # Sort anomalies by deviation (highest first)
            anomalies.sort(key=lambda x: x["deviation"], reverse=True)
            
        except Exception as e:
            # If anomaly detection fails, return empty list
            pass
        
        return anomalies

    def get_cost_efficiency_metrics(
        self,
        scope: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        user_count: Optional[int] = None,
        transaction_count: Optional[int] = None,
        api_version: str = "2023-03-01"
    ) -> Dict[str, Any]:
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
        try:
            if not start_date or not end_date:
                today = datetime.today()
                start_date = today.replace(day=1).strftime("%Y-%m-%d")
                end_date = today.strftime("%Y-%m-%d")

            # Use the cost_client to get cost data
            cost_data = self.cost_client.get_cost_data(
                scope,
                start_date=start_date,
                end_date=end_date,
                granularity="Daily",
                metrics=["Cost"],
                group_by=["ServiceName"]
            )
            
            if isinstance(cost_data, dict) and "error" in cost_data:
                return cost_data
            
            # Process cost data
            total_cost = 0.0
            cost_by_service = {}
            daily_costs = []
            
            properties = cost_data.get("properties", {})
            rows = properties.get("rows", [])
            columns = properties.get("columns", [])
            
            # Find cost and service column indices
            cost_col_idx = None
            service_col_idx = None
            date_col_idx = None
            
            for idx, col in enumerate(columns):
                name = col.get("name", "").lower()
                if name in ["actualcost", "cost", "pretaxcost"]:
                    cost_col_idx = idx
                elif "service" in name:
                    service_col_idx = idx
                elif "date" in name:
                    date_col_idx = idx
            
            if cost_col_idx is None:
                return {"error": "Could not find cost column in response"}
            
            # Process rows to calculate metrics
            for row in rows:
                if len(row) > max(cost_col_idx, service_col_idx or 0, date_col_idx or 0):
                    cost = float(row[cost_col_idx]) if row[cost_col_idx] else 0.0
                    service = row[service_col_idx] if service_col_idx is not None else "Unknown"
                    date = row[date_col_idx] if date_col_idx is not None else None
                    
                    total_cost += cost
                    
                    # Track cost by service
                    if service not in cost_by_service:
                        cost_by_service[service] = 0.0
                    cost_by_service[service] += cost
                    
                    # Track daily costs for variance calculation
                    if date:
                        daily_costs.append({"date": date, "cost": cost})
            
            # Calculate efficiency metrics
            efficiency_metrics = {
                "total_cost": round(total_cost, 2),
                "cost_by_service": {k: round(v, 2) for k, v in cost_by_service.items()},
                "period": {"start": start_date, "end": end_date},
                "total_days_analyzed": len(daily_costs) if daily_costs else 0
            }
            
            # Calculate per-user and per-transaction metrics if provided
            if user_count and user_count > 0:
                efficiency_metrics["cost_per_user"] = round(total_cost / user_count, 2)
            
            if transaction_count and transaction_count > 0:
                efficiency_metrics["cost_per_transaction"] = round(total_cost / transaction_count, 4)
            
            # Calculate variance and efficiency score if we have daily data
            if daily_costs:
                costs = [day["cost"] for day in daily_costs]
                avg_daily_cost = sum(costs) / len(costs)
                variance = sum((cost - avg_daily_cost) ** 2 for cost in costs) / len(costs)
                std_dev = variance ** 0.5
                
                efficiency_metrics.update({
                    "avg_daily_cost": round(avg_daily_cost, 2),
                    "cost_stddev": round(std_dev, 2),
                    "cost_variance_ratio": round(std_dev / avg_daily_cost if avg_daily_cost > 0 else 0, 3)
                })
                
                # Calculate efficiency score (lower variance = higher efficiency)
                if avg_daily_cost > 0:
                    variance_ratio = std_dev / avg_daily_cost
                    efficiency_score = max(0, min(1, 1 - (variance_ratio * 0.5)))
                    efficiency_metrics["cost_efficiency_score"] = round(efficiency_score, 3)
                
                # Estimate waste (days with cost > 1.5x average)
                waste_days = len([cost for cost in costs if cost > avg_daily_cost * 1.5])
                waste_percentage = (waste_days / len(costs)) * 100 if costs else 0
                
                efficiency_metrics.update({
                    "waste_days": waste_days,
                    "waste_percentage": round(waste_percentage, 1)
                })
            
            return {"efficiency_metrics": efficiency_metrics}
            
        except Exception as e:
            return {"error": f"Failed to calculate cost efficiency metrics: {str(e)}"}

    def generate_cost_report(
        self,
        scope: str,
        report_type: str = "monthly",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        metrics: Optional[list] = None,
        group_by: Optional[list] = None,
        filter_: Optional[dict] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive cost report for a given Azure scope, with optional metrics, group_by, and filter parameters.
        The report_type parameter controls the default date range and aggregation:
            - 'monthly': current month (default)
            - 'quarterly': last 3 months
            - 'annual': last 12 months
        If start_date/end_date are provided, they override report_type defaults.
        For 'quarterly' and 'annual', a summary aggregation by quarter/year is included in the result.

        Args:
            scope (str): Azure scope (required). Examples:
                - Subscription: "/subscriptions/{subscription-id}/"
                - Resource Group: "/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/"
                - Billing Account: "/providers/Microsoft.Billing/billingAccounts/{billing-account-id}"
            report_type (str): Type of report (monthly, quarterly, annual)
            start_date (Optional[str]): Start date for report
            end_date (Optional[str]): End date for report
            metrics (Optional[list]): List of cost metrics to aggregate (e.g., ["Cost"])
            group_by (Optional[list]): List of dimensions to group by (e.g., ["ServiceName"])
            filter_ (Optional[dict]): Additional filter criteria for the query

        Returns:
            Dict[str, Any]: Cost report, including summary for quarterly/annual types
        """
        from collections import defaultdict
        try:
            today = datetime.today()
            if not start_date or not end_date:
                if report_type == "monthly":
                    start_date = today.replace(day=1).strftime("%Y-%m-%d")
                    end_date = today.strftime("%Y-%m-%d")
                elif report_type == "quarterly":
                    start_date = (today.replace(day=1) - relativedelta(months=2)).strftime("%Y-%m-%d")
                    end_date = today.strftime("%Y-%m-%d")
                elif report_type == "annual":
                    start_date = (today.replace(day=1) - relativedelta(months=11)).strftime("%Y-%m-%d")
                    end_date = today.strftime("%Y-%m-%d")
                else:
                    start_date = today.replace(day=1).strftime("%Y-%m-%d")
                    end_date = today.strftime("%Y-%m-%d")

            # Always use monthly granularity for summary reports
            granularity = "Monthly"

            cost_data = self.cost_client.get_cost_data(
                scope,
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                metrics=metrics,
                group_by=group_by,
                filter_=filter_
            )

            # Post-process for quarterly/annual summary
            summary = None
            if report_type in ("quarterly", "annual") and isinstance(cost_data, dict):
                # Azure returns columns/rows; find date and cost columns
                properties = cost_data.get("properties", {})
                columns = properties.get("columns", [])
                rows = properties.get("rows", [])
                date_col_idx = None
                cost_col_idx = None
                for idx, col in enumerate(columns):
                    name = col.get("name", "").lower()
                    if "date" in name or "billingmonth" in name:
                        date_col_idx = idx
                    if name in ["cost", "actualcost", "pretaxcost"]:
                        cost_col_idx = idx
                # Aggregate by quarter or year
                agg = defaultdict(float)
                for row in rows:
                    if date_col_idx is not None and cost_col_idx is not None:
                        date_str = row[date_col_idx]
                        cost = float(row[cost_col_idx]) if row[cost_col_idx] else 0.0
                        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
                        if report_type == "quarterly":
                            quarter = f"Q{((dt.month-1)//3)+1}-{dt.year}"
                            agg[quarter] += cost
                        elif report_type == "annual":
                            agg[str(dt.year)] += cost
                summary = dict(agg)

            result = {
                "report_type": report_type,
                "period": {"start": start_date, "end": end_date},
                "cost_data": cost_data,
                "generated_at": datetime.now().isoformat()
            }
            if summary is not None:
                result["summary"] = summary
            return result
        except Exception as e:
            return {"error": f"Failed to generate cost report: {str(e)}"}

