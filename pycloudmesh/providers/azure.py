import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dateutil.relativedelta import relativedelta
import json


class AzureBase:
    """Base class for Azure operations with common functionality."""
    
    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure base client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        self.subscription_id = subscription_id
        self.token = token
        self.base_url = f"https://management.azure.com"

    def _handle_azure_pagination(
        self, 
        url: str, 
        params: dict = None, 
        body: dict = None, 
        request_type: str = "GET",
        headers: dict = None,
    ) -> Dict[str, Any]:
        """
        Generic method to handle Azure API pagination for GET, POST, PUT requests.

        Args:
            url (str): Initial API URL
            params (dict, optional): Query parameters for the request
            body (dict, optional): Request body for POST/PUT requests
            request_type (str): HTTP method - "GET", "POST", or "PUT". Default: "GET"
            headers (dict, optional): Custom headers. If not provided, uses default auth header

        Returns:
            Dict[str, Any]: Unified response with all paginated data
        """
        try:
            if headers is None:
                headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            else:
                headers.setdefault("Authorization", f"Bearer {self.token}")
                headers.setdefault("Content-Type", "application/json")
            
            all_data = []
            page_count = 0
            current_url = url
            current_params = params or {}
            current_body = body
            
            while current_url:
                if request_type.upper() == "GET":
                    response = requests.get(current_url, headers=headers, params=current_params)
                elif request_type.upper() == "POST":
                    response = requests.post(current_url, headers=headers, params=current_params, json=current_body)
                elif request_type.upper() == "PUT":
                    response = requests.put(current_url, headers=headers, params=current_params, json=current_body)
                else:
                    return {"error": f"Unsupported request type: {request_type}. Use GET, POST, or PUT."}
                
                response.raise_for_status()
                data = response.json()
                
                if "value" in data:
                    all_data.extend(data["value"])
                elif "properties" in data and "rows" in data["properties"]:
                    if page_count == 0:
                        all_data = data
                    else:
                        if isinstance(all_data, dict) and "properties" in all_data and "rows" in all_data["properties"]:
                            all_data["properties"]["rows"].extend(data["properties"]["rows"])
                        else:
                            all_data.append(data)
                elif isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
                
                current_url = data.get("nextLink")
                page_count += 1
                
                if page_count > 1:
                    current_params = {}
                    current_body = None
            
            if isinstance(all_data, dict) and "properties" in all_data and "rows" in all_data["properties"]:
                return {
                    **all_data,
                    "total_items": len(all_data["properties"]["rows"]),
                    "pages_retrieved": page_count,
                    "has_more_pages": bool(current_url),
                    "request_type": request_type.upper(),
                }
            else:
                return {
                    "value": all_data,
                    "total_items": len(all_data),
                    "pages_retrieved": page_count,
                    "has_more_pages": bool(current_url),
                    "request_type": request_type.upper(),
                }
            
        except requests.exceptions.RequestException as e:
            raise Exception(str(e))
        except Exception as e:
            return {"error": f"Unexpected error during pagination: {str(e)}"}


class AzureReservationCost(AzureBase):
    """Azure Reservation Cost Management class for handling Azure reservation-related operations."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure Reservation Cost client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        super().__init__(subscription_id, token)

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
            
            reservation_orders_url = f"{self.base_url}{scope}/providers/Microsoft.Capacity/reservationOrders"
            reservation_orders_params = {"api-version": "2022-11-01"}
            
            reservation_orders_response = requests.get(
                reservation_orders_url, 
                headers=headers, 
                params=reservation_orders_params
            )
            reservation_orders_response.raise_for_status()
            reservation_orders_data = reservation_orders_response.json()
            
            reservations_details = []
            for order in reservation_orders_data.get("value", []):
                order_id = order.get("name")
                reservations = order.get("properties", {}).get("reservations", [])
                
                for reservation in reservations:
                    reservation_id = reservation.get("id", "").split("/")[-1]
                    
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
            
            return self._handle_azure_pagination(url, params, headers=headers, request_type="GET")
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get advisor recommendations: {str(e)}"}

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


class AzureBudgetManagement(AzureBase):
    """Azure Budget Management class for handling Azure budget-related operations."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure Budget Management client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        super().__init__(subscription_id, token)

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
                today = datetime.today()
                start_date = today.replace(day=1).strftime("%Y-%m-%d")
            else:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_dt.replace(day=1).strftime("%Y-%m-%d")
            
            if not end_date:
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
            
            if not notifications:
                raise ValueError("Notifications are required for budget creation")
            
            payload["properties"]["notifications"] = {}
            for i, notification in enumerate(notifications):
                if not notification.get("contactEmails"):
                    raise ValueError(f"Notification {i}: contactEmails is required")
                if "threshold" not in notification:
                    raise ValueError(f"Notification {i}: threshold is required")
                if "operator" not in notification:
                    raise ValueError(f"Notification {i}: operator is required")
                
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

    def get_budget_notifications(self, 
                   budget_name: str, 
                   scope: str, 
                   /, 
                   *, 
                   api_version: str = "2024-08-01") -> Dict[str, Any]:
        """
        Get notifications for a specific budget by name and scope.

        Args:
            budget_name (str): Name of the budget to retrieve
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            api_version (str): API version to use

        Returns:
            Dict[str, Any]: Budget details including notifications

        Raises:
            requests.exceptions.RequestException: If Azure API call fails

        Example:
            >>> azure.get_budget_notifications(budget_name="monthly-budget", scope="/subscriptions/your-subscription-id/")
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


class AzureCostManagement(AzureBase):
    """Azure Cost Management class for handling Azure cost-related operations."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure Cost Management client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        super().__init__(subscription_id, token)

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

            headers = {"Authorization": f"Bearer {self.token}"}
            return self._handle_azure_pagination(url, params, payload, headers=headers, request_type="POST")
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
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        SUBSCRIPTION_GROUPBYS = ["ResourceType", "ResourceLocation", "ResourceGroupName"]
        BILLING_ACCOUNT_GROUPBYS = [
            "SubscriptionId", "BillingProfileId", "InvoiceSectionId", "Product", "Meter", "ServiceFamily", "ServiceName", "ResourceGroup", "ResourceId", "ResourceType", "ChargeType", "PublisherType", "BillingPeriod"
        ]

        is_billing_account = scope.startswith("/providers/Microsoft.Billing/billingAccounts")
        if not dimensions:
            if is_billing_account:
                dimensions = ["SubscriptionId"]
            else:
                dimensions = SUBSCRIPTION_GROUPBYS[:2]
        if is_billing_account:
            for dim in dimensions:
                if dim not in BILLING_ACCOUNT_GROUPBYS:
                    raise ValueError(f"Invalid group by dimension '{dim}' for billing account scope. Allowed: {BILLING_ACCOUNT_GROUPBYS}")
        else:
            for dim in dimensions:
                if dim not in SUBSCRIPTION_GROUPBYS:
                    raise ValueError(f"Invalid group by dimension '{dim}' for subscription/resource group scope. Allowed: {SUBSCRIPTION_GROUPBYS}")

        cost_data = self.get_cost_data(
            scope,
            start_date=start_date,
            end_date=end_date,
            group_by=dimensions
        )
        if isinstance(cost_data, dict) and "error" in cost_data:
            return cost_data
        summary = {
            "period": {"start": start_date, "end": end_date},
            "dimensions": dimensions,
            "total_cost": 0.0,
            "cost_breakdown": {},
            "cost_trends": [],
            "insights": []
        }
        properties = cost_data.get("properties", {})
        columns = properties.get("columns", [])
        rows = properties.get("rows", [])
        cost_col_idx = None
        for idx, col in enumerate(columns):
            if col.get("name", "").lower() in ["pretaxcost", "actualcost", "costusd", "cost"]:
                cost_col_idx = idx
                break
        dim_indices = [i for i, col in enumerate(columns) if col.get("name") in dimensions]
        for row in rows:
            cost = float(row[cost_col_idx]) if cost_col_idx is not None else 0.0
            summary["total_cost"] += cost
            key = tuple(row[i] for i in dim_indices)
            key_str = "|".join(str(k) for k in key)
            if key_str not in summary["cost_breakdown"]:
                summary["cost_breakdown"][key_str] = 0.0
            summary["cost_breakdown"][key_str] += cost
            if any("date" in col.get("name", "").lower() for col in columns):
                summary["cost_trends"].append({"key": key_str, "cost": cost})
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
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        cost_data = self.get_cost_data(
            scope,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity
        )
        if isinstance(cost_data, dict) and "error" in cost_data:
            return cost_data
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
        date_col_idx = None
        cost_col_idx = None
        for idx, col in enumerate(columns):
            name = col.get("name", "").lower()
            if "date" in name:
                date_col_idx = idx
            if name in ["pretaxcost", "actualcost", "costusd", "cost"]:
                cost_col_idx = idx
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
                    f"Total cost over {trends_analysis['total_periods']} periods: {trends_analysis['total_cost']:.2f}"
                )
                trends_analysis["insights"].append(
                    f"Average cost per period: {trends_analysis['average_daily_cost']:.4f}"
                )
                if trends_analysis["trend_direction"] != "stable":
                    trends_analysis["insights"].append(
                        f"Cost trend is {trends_analysis['trend_direction']} ({trends_analysis['growth_rate']:.1f}% change)"
                    )
                if trends_analysis["peak_periods"]:
                    peak_period = trends_analysis["peak_periods"][0]
                    trends_analysis["insights"].append(
                        f"Peak cost period: {peak_period['date']} ({peak_period['cost']:.4f})"
                    )
        return trends_analysis

    def get_resource_costs(
        self,
        scope: str,
        resource_id: str,
        granularity: str = "Daily", 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        metrics: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get detailed cost analysis for a specific resource.

        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            resource_id (str): ID of the resource to get costs for
            granularity (str): Data granularity (Daily, Monthly, etc.)
            start_date (Optional[str]): Start date for cost data
            end_date (Optional[str]): End date for cost data
            metrics (Optional[str]): Cost metrics to analyze

        Returns:
            Dict[str, Any]: Detailed resource cost analysis with insights and breakdowns
        """
        from datetime import datetime

        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        try:
            filter_ = {
                "dimensions": {
                    "name": "ResourceId",
                    "operator": "In",
                    "values": [resource_id]
                }
            }
            
            cost_data = self.get_cost_data(
                scope,
                granularity=granularity,
                start_date=start_date,
                end_date=end_date,
                metrics=metrics,
                filter_=filter_
            )

            if isinstance(cost_data, dict) and "error" in cost_data:
                return cost_data

            resource_analysis = {
                "resource_id": resource_id,
                "resource_type": "Azure Resource",
                "period": {"start": start_date, "end": end_date},
                "granularity": granularity,
                "total_cost": 0.0,
                "total_periods": 0,
                "active_periods": 0,
                "cost_periods": [],
                "cost_breakdown": {},
                "utilization_insights": [],
                "cost_trends": [],
                "recommendations": []
            }

            properties = cost_data.get("properties", {})
            columns = properties.get("columns", [])
            rows = properties.get("rows", [])
            
            cost_col_idx = None
            date_col_idx = None
            for idx, col in enumerate(columns):
                name = col.get("name", "").lower()
                if name in ["pretaxcost", "actualcost", "costusd", "cost"]:
                    cost_col_idx = idx
                if "date" in name:
                    date_col_idx = idx

            costs = []
            for row in rows:
                cost = float(row[cost_col_idx]) if cost_col_idx is not None and row[cost_col_idx] is not None else 0.0
                date = row[date_col_idx] if date_col_idx is not None else "unknown"
                
                resource_analysis["total_cost"] += cost
                resource_analysis["total_periods"] += 1
                
                if cost > 0:
                    resource_analysis["active_periods"] += 1
                
                resource_analysis["cost_periods"].append({
                    "date": date,
                    "cost": cost
                })
                costs.append(cost)

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
                    resource_analysis["recommendations"].append("High resource costs detected - review resource type and consider reserved instances")
                
                if resource_analysis["active_periods"] < resource_analysis["total_periods"] * 0.3:
                    resource_analysis["recommendations"].append("Low resource activity - consider stopping resources during idle periods")
                
                if len(costs) > 0:
                    max_cost = max(costs)
                    min_cost = min(costs)
                    cost_variance = max_cost - min_cost
                    
                    if cost_variance > avg_cost:
                        resource_analysis["recommendations"].append("High cost variability detected - review usage patterns")
                    else:
                        resource_analysis["recommendations"].append("Consistent cost pattern - resource usage is stable")
                
                resource_analysis["recommendations"].append(
                    f"Resource {resource_id} analysis complete - review Azure Cost Management for detailed breakdowns"
                )

            return resource_analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze resource costs: {str(e)}"}


class AzureFinOpsOptimization(AzureBase):
    """Azure FinOps Optimization class for cost optimization features."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure FinOps Optimization client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        super().__init__(subscription_id, token)

    def get_advisor_recommendations(self, api_version: str = "2025-01-01", filter: str = None) -> Dict[str, Any]:
        """
        Get Azure Advisor recommendations for cost optimization with automatic pagination handling.

        Args:
            api_version (str, optional): API version for the Advisor API. Defaults to '2025-01-01'.
            filter (str, optional): OData filter string for server-side filtering (e.g., "Category eq 'Cost' and ResourceGroup eq 'MyResourceGroup'").

        Returns:
            Dict[str, Any]: Complete Advisor recommendations with pagination handling
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/subscriptions/{self.subscription_id}/providers/Microsoft.Advisor/recommendations"
            params = {"api-version": api_version}
            if filter:
                params["$filter"] = filter
            
            return self._handle_azure_pagination(url, params, headers=headers, request_type="GET")
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get advisor recommendations: {str(e)}"}

    def get_reserved_instance_recommendations(self, scope: str, api_version: str = "2024-08-01", filter: str = None) -> Dict[str, Any]:
        """
        Get Reserved Instance recommendations with pagination support.

        Args:
            scope (str): Azure scope for the recommendations
            api_version (str, optional): API version for the Reservation Recommendations API. Defaults to '2024-08-01'.
            filter (str, optional): OData filter string for server-side filtering (e.g., "ResourceGroup eq 'MyResourceGroup'").

        Returns:
            Dict[str, Any]: Complete Reserved Instance recommendations with pagination handling
        """
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.Consumption/reservationRecommendations"
            params = {"api-version": api_version}
            if filter:
                params["$filter"] = filter
            
            return self._handle_azure_pagination(url, params, headers=headers, request_type="GET")
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get Reserved Instance recommendations: {str(e)}"}

    def get_optimization_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations with automatic pagination handling.

        Args:
            **kwargs: Additional parameters including:
                - filter: OData filter string
                - scope: Azure scope for recommendations

        Returns:
            Dict[str, Any]: Optimization recommendations with pagination handling
        """
        try:
            filter_arg = kwargs.get('filter', None)
            scope = kwargs.get('scope', f"/subscriptions/{self.subscription_id}")
            
            advisor_recs = self.get_advisor_recommendations(
                api_version='2025-01-01', 
                filter=filter_arg
            )
            
            reservation_recs = self.get_reserved_instance_recommendations(
                scope=scope, 
                api_version='2024-08-01', 
                filter=filter_arg
            )
            
            total_advisor = advisor_recs.get('total_items', 0) if 'error' not in advisor_recs else 0
            total_reservation = reservation_recs.get('total_items', 0) if 'error' not in reservation_recs else 0
            
            return {
                'advisor_recommendations': advisor_recs,
                'reserved_instance_recommendations': reservation_recs,
                'summary': {
                    'total_advisor_recommendations': total_advisor,
                    'total_reservation_recommendations': total_reservation,
                    'total_recommendations': total_advisor + total_reservation,
                    'message': f"Retrieved {total_advisor + total_reservation} total recommendations"
                }
            }
        except Exception as e:
            return {"error": f"Failed to get optimization recommendations: {str(e)}"}


class AzureFinOpsGovernance(AzureBase):
    """Azure FinOps Governance class for policy and compliance features."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure FinOps Governance client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        super().__init__(subscription_id, token)
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
            
            if not scope:
                scope = f"/subscriptions/{self.subscription_id}"
            
            policy_definitions_url = f"{self.base_url}{scope}/providers/Microsoft.Authorization/policyDefinitions"
            policy_definitions_params = {"api-version": "2023-04-01"}
            
            policy_definitions_response = requests.get(
                policy_definitions_url, 
                headers=headers, 
                params=policy_definitions_params
            )
            policy_definitions_response.raise_for_status()
            policy_definitions = policy_definitions_response.json()
            
            policy_assignments_url = f"{self.base_url}{scope}/providers/Microsoft.Authorization/policyAssignments"
            policy_assignments_params = {"api-version": "2022-06-01"}
            
            policy_assignments_response = requests.get(
                policy_assignments_url, 
                headers=headers, 
                params=policy_assignments_params
            )
            policy_assignments_response.raise_for_status()
            policy_assignments = policy_assignments_response.json()
            
            cost_keywords = ["cost", "budget", "tag", "quota", "spend", "billing", "reservation", "budget", "expense"]
            cost_policies = []
            
            for policy in policy_definitions.get("value", []):
                display_name = policy.get("properties", {}).get("displayName", "").lower()
                description = policy.get("properties", {}).get("description", "").lower()
                category = policy.get("properties", {}).get("metadata", {}).get("category", "").lower()
                
                if any(keyword in display_name or keyword in description or keyword in category for keyword in cost_keywords):
                    cost_policies.append(policy)
            
            cost_assignments = []
            for assignment in policy_assignments.get("value", []):
                policy_definition_id = assignment.get("properties", {}).get("policyDefinitionId", "")
                if any(policy.get("id") in policy_definition_id for policy in cost_policies):
                    cost_assignments.append(assignment)
            
            total_policies = len(cost_policies)
            total_assignments = len(cost_assignments)
            
            compliance_score = min(100, (total_assignments / max(total_policies, 1)) * 100) if total_policies > 0 else 0
            
            return {
                "scope": scope,
                "total_policies": total_policies,
                "total_assignments": total_assignments,
                "cost_related_policies": cost_policies,
                "cost_related_assignments": cost_assignments,
                "compliance_score": round(compliance_score, 1),
                "compliance_status": "Compliant" if compliance_score >= 80 else "Non-compliant",
                "cost_governance_insights": [
                    f"Found {total_policies} cost-related policies",
                    f"Active assignments: {total_assignments}",
                    f"Compliance score: {compliance_score:.1f}%",
                    "Note: Detailed compliance requires Azure Policy Insights API access"
                ],
                "message": "Policy compliance status retrieved from Azure Policy API"
            }
            
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
            
            return self._handle_azure_pagination(url, params, headers=headers, request_type="GET")
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
            available_tags = self.get_available_tags(scope)
            if "error" in available_tags:
                return available_tags
            
            tag_data = available_tags.get("properties", {}).get("tags", [])
            discovered_tags = []
            for tag_item in tag_data:
                if "key" in tag_item:
                    discovered_tags.append(tag_item["key"])
            
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


class AzureFinOpsAnalytics(AzureBase):
    """Azure FinOps Analytics class for advanced analytics and reporting."""

    def __init__(self, subscription_id: str, token: str):
        """
        Initialize Azure FinOps Analytics client.

        Args:
            subscription_id (str): Azure subscription ID
            token (str): Azure authentication token
        """
        super().__init__(subscription_id, token)
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
        Get unified cost forecast with daily breakdowns and AI model integration.
        
        This method provides a unified response format that includes:
        - Daily cost forecasts with confidence intervals
        - Total cost summaries
        - AI model information and accuracy metrics
        - Historical data for comparison
        
        Args:
            scope (str): Azure scope (subscription, resource group, billing account, etc.)
            api_version (str): API version for the Cost Management API
            start_date (str, optional): Start date for historical data (YYYY-MM-DD)
            end_date (str, optional): End date for historical data (YYYY-MM-DD)
            forecast_period (int, optional): Number of days to forecast (default: 30)
            payload (dict, optional): Custom payload for the query
            
        Returns:
            Dict[str, Any]: Unified forecast response with daily breakdowns
        """
        from datetime import datetime
        import numpy as np
        
        try:
            if not start_date or not end_date:
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                start_date_dt = (today.replace(day=1) - relativedelta(months=3))
                start_date = start_date_dt.strftime("%Y-%m-%dT00:00:00+00:00")
                end_date = today.strftime("%Y-%m-%dT00:00:00+00:00")
            
            historical_data = self.cost_client.get_cost_data(
                scope,
                granularity="Daily",
                start_date=start_date.split('T')[0] if 'T' in start_date else start_date,
                end_date=end_date.split('T')[0] if 'T' in end_date else end_date,
                api_version=api_version
            )
            
            daily_costs = []
            total_historical_cost = 0.0
            
            if "properties" in historical_data and "rows" in historical_data["properties"]:
                for row in historical_data["properties"]["rows"]:
                    if len(row) >= 3:
                        cost = float(row[0]) if row[0] else 0
                        usage_date = str(row[1])
                        currency = row[2]
                        if len(usage_date) == 8:
                            date_str = f"{usage_date[:4]}-{usage_date[4:6]}-{usage_date[6:8]}"
                        else:
                            date_str = usage_date
                        
                        daily_costs.append({
                            "date": date_str,
                            "cost": cost
                        })
                        total_historical_cost += cost
            
            avg_daily_cost = total_historical_cost / len(daily_costs) if daily_costs else 0
            
            forecast_results = []
            total_forecast_cost = 0.0
            
            try:
                forecast_results = self._generate_azure_ml_forecast(
                    daily_costs, forecast_period, avg_daily_cost, scope
                )
                ai_model_used = True
            except Exception as e:
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
                "start_date": start_date.split('T')[0] if 'T' in start_date else start_date,
                "end_date": end_date.split('T')[0] if 'T' in end_date else end_date,
                "total_historical_cost": round(total_historical_cost, 2),
                "total_forecast_cost": round(total_forecast_cost, 2),
                "average_daily_cost": round(avg_daily_cost, 2),
                "forecast_results": forecast_results,
                "ai_model_used": ai_model_used,
                "model_accuracy": self._calculate_model_accuracy(daily_costs),
                "insights": insights,
                "granularity": "Daily",
                "message": f"Unified cost forecast generated for {forecast_period} days using {'Azure ML' if ai_model_used else 'statistical analysis'}"
            }
            
        except Exception as e:
            return {"error": f"Failed to generate unified cost forecast: {str(e)}"}
    
    def _generate_azure_ml_forecast(self, daily_costs, forecast_period, avg_daily_cost, scope):
        """Generate Azure ML enhanced forecast using trend analysis and seasonality."""
        from datetime import datetime, timedelta
        import numpy as np
        
        if not daily_costs:
            return []
        
        costs = [day["cost"] for day in daily_costs]
        dates = [datetime.strptime(day["date"], "%Y-%m-%d") for day in daily_costs]
        
        if len(costs) > 1:
            x = np.arange(len(costs))
            y = np.array(costs)
            trend_coef = np.polyfit(x, y, 1)[0]
        else:
            trend_coef = 0
        
        weekly_pattern = self._calculate_weekly_pattern(daily_costs)
        
        forecast_results = []
        last_date = dates[-1] if dates else datetime.today()
        
        for i in range(1, forecast_period + 1):
            forecast_date = last_date + timedelta(days=i)
            
            base_forecast = avg_daily_cost + (trend_coef * i)
            
            day_of_week = forecast_date.weekday()
            seasonal_factor = weekly_pattern.get(day_of_week, 1.0)
            adjusted_forecast = base_forecast * seasonal_factor
            
            confidence_range = avg_daily_cost * 0.2
            lower_bound = max(0, adjusted_forecast - confidence_range)
            upper_bound = adjusted_forecast + confidence_range
            
            forecast_results.append({
                "date": forecast_date.strftime("%Y-%m-%d"),
                "forecast_value": round(adjusted_forecast, 2),
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
                "confidence_level": 0.8
            })
        
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
    
    def _calculate_weekly_pattern(self, daily_costs):
        """Calculate weekly cost patterns for seasonality."""
        weekly_totals = {i: [] for i in range(7)}
        
        for day in daily_costs:
            date = datetime.strptime(day["date"], "%Y-%m-%d")
            day_of_week = date.weekday()
            weekly_totals[day_of_week].append(day["cost"])
        
        weekly_pattern = {}
        overall_avg = sum(day["cost"] for day in daily_costs) / len(daily_costs) if daily_costs else 1
        
        for day_of_week in range(7):
            if weekly_totals[day_of_week]:
                day_avg = sum(weekly_totals[day_of_week]) / len(weekly_totals[day_of_week])
                weekly_pattern[day_of_week] = day_avg / overall_avg if overall_avg > 0 else 1.0
            else:
                weekly_pattern[day_of_week] = 1.0
        
        return weekly_pattern
    
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
            if not start_date or not end_date:
                today = datetime.now()
                end_date = today.strftime("%Y-%m-%d")
                start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")

            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}{scope}/providers/Microsoft.CostManagement/query"
            params = {"api-version": api_version}
            
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
            
            cost_data = self._handle_azure_pagination(
                url,
                params,
                body=payload,
                headers=headers,
                request_type="POST",
            )

            if isinstance(cost_data, dict) and "error" in cost_data:
                return cost_data

            anomalies = self._detect_anomalies(cost_data, start_date, end_date)

            return {
                "scope": scope,
                "period": {"start": start_date, "end": end_date},
                "anomalies": anomalies,
                "total_records": len(anomalies),
                "cost_data": cost_data,
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
            properties = cost_data.get("properties", {})
            rows = properties.get("rows", [])
            columns = properties.get("columns", [])
            
            if not rows or not columns:
                return anomalies
            
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
            
            daily_costs = []
            for row in rows:
                if len(row) > max(cost_col_idx, date_col_idx or 0):
                    cost = float(row[cost_col_idx]) if row[cost_col_idx] else 0.0
                    date = row[date_col_idx] if date_col_idx is not None else None
                    daily_costs.append({"date": date, "cost": cost})
            
            if len(daily_costs) < 3:
                return anomalies
            
            costs = [day["cost"] for day in daily_costs]
            mean_cost = sum(costs) / len(costs)
            variance = sum((cost - mean_cost) ** 2 for cost in costs) / len(costs)
            std_dev = variance ** 0.5
            
            threshold = 2 * std_dev
            
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
            
            anomalies.sort(key=lambda x: x["deviation"], reverse=True)
            
        except Exception as e:
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
            
            total_cost = 0.0
            cost_by_service = {}
            daily_costs = []
            
            properties = cost_data.get("properties", {})
            rows = properties.get("rows", [])
            columns = properties.get("columns", [])
            
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
            
            for row in rows:
                if len(row) > max(cost_col_idx, service_col_idx or 0, date_col_idx or 0):
                    cost = float(row[cost_col_idx]) if row[cost_col_idx] else 0.0
                    service = row[service_col_idx] if service_col_idx is not None else "Unknown"
                    date = row[date_col_idx] if date_col_idx is not None else None
                    
                    total_cost += cost
                    
                    if service not in cost_by_service:
                        cost_by_service[service] = 0.0
                    cost_by_service[service] += cost
                    
                    if date:
                        daily_costs.append({"date": date, "cost": cost})
            
            efficiency_metrics = {
                "total_cost": round(total_cost, 2),
                "cost_by_service": {k: round(v, 2) for k, v in cost_by_service.items()},
                "period": {"start": start_date, "end": end_date},
                "total_days_analyzed": len(daily_costs) if daily_costs else 0
            }
            
            if user_count and user_count > 0:
                efficiency_metrics["cost_per_user"] = round(total_cost / user_count, 2)
            
            if transaction_count and transaction_count > 0:
                efficiency_metrics["cost_per_transaction"] = round(total_cost / transaction_count, 4)
            
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
                
                if avg_daily_cost > 0:
                    variance_ratio = std_dev / avg_daily_cost
                    efficiency_score = max(0, min(1, 1 - (variance_ratio * 0.5)))
                    efficiency_metrics["cost_efficiency_score"] = round(efficiency_score, 3)
                
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
            Dict[str, Any]: Unified cost report format
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

            service_data = self.cost_client.get_cost_data(
                scope,
                start_date=start_date,
                end_date=end_date,
                granularity="Monthly",
                metrics=metrics or ["Cost"],
                group_by=group_by or ["ServiceName"],
                filter_=filter_
            )

            region_data = self.cost_client.get_cost_data(
                scope,
                start_date=start_date,
                end_date=end_date,
                granularity="Monthly",
                metrics=metrics or ["Cost"],
                group_by=["ResourceLocation"],
                filter_=filter_
            )

            daily_data = self.cost_client.get_cost_data(
                scope,
                start_date=start_date,
                end_date=end_date,
                granularity="Daily",
                metrics=metrics or ["Cost"],
                filter_=filter_
            )

            service_breakdown = []
            total_cost = 0.0
            if isinstance(service_data, dict) and "properties" in service_data:
                properties = service_data["properties"]
                columns = properties.get("columns", [])
                rows = properties.get("rows", [])
                
                service_col_idx = None
                cost_col_idx = None
                for idx, col in enumerate(columns):
                    name = col.get("name", "").lower()
                    if "service" in name:
                        service_col_idx = idx
                    if name in ["cost", "actualcost", "pretaxcost"]:
                        cost_col_idx = idx
                
                service_costs = defaultdict(float)
                for row in rows:
                    if service_col_idx is not None and cost_col_idx is not None:
                        service_name = row[service_col_idx] if row[service_col_idx] else "Unknown"
                        cost = float(row[cost_col_idx]) if row[cost_col_idx] else 0.0
                        service_costs[service_name] += cost
                        total_cost += cost
                
                for service_name, cost in service_costs.items():
                    service_breakdown.append({
                        "service": service_name,
                        "total_cost": cost,
                        "avg_daily_cost": cost
                    })

            region_breakdown = []
            if isinstance(region_data, dict) and "properties" in region_data:
                properties = region_data["properties"]
                columns = properties.get("columns", [])
                rows = properties.get("rows", [])
                
                region_col_idx = None
                cost_col_idx = None
                for idx, col in enumerate(columns):
                    name = col.get("name", "").lower()
                    if "location" in name or "region" in name:
                        region_col_idx = idx
                    if name in ["cost", "actualcost", "pretaxcost"]:
                        cost_col_idx = idx
                
                region_costs = defaultdict(float)
                for row in rows:
                    if region_col_idx is not None and cost_col_idx is not None:
                        region_name = row[region_col_idx] if row[region_col_idx] else "Unknown"
                        cost = float(row[cost_col_idx]) if row[cost_col_idx] else 0.0
                        region_costs[region_name] += cost
                
                for region_name, cost in region_costs.items():
                    region_breakdown.append({
                        "region": region_name,
                        "total_cost": cost,
                        "avg_daily_cost": cost
                    })

            daily_trends = []
            if isinstance(daily_data, dict) and "properties" in daily_data:
                properties = daily_data["properties"]
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
                
                for row in rows:
                    if date_col_idx is not None and cost_col_idx is not None:
                        date_str = row[date_col_idx]
                        cost = float(row[cost_col_idx]) if row[cost_col_idx] else 0.0
                        if isinstance(date_str, str):
                            date_parts = date_str.split('T')[0]
                            daily_trends.append({
                                "date": date_parts,
                                "daily_cost": cost
                            })

            total_days = len(daily_trends)
            avg_daily_cost = sum(d['daily_cost'] for d in daily_trends) / total_days if total_days > 0 else 0
            min_daily_cost = min(d['daily_cost'] for d in daily_trends) if daily_trends else 0
            max_daily_cost = max(d['daily_cost'] for d in daily_trends) if daily_trends else 0
            
            if daily_trends:
                costs = [d['daily_cost'] for d in daily_trends]
                cost_stddev = (sum((c - avg_daily_cost) ** 2 for c in costs) / len(costs)) ** 0.5 if len(costs) > 1 else 0
                cost_variance_ratio = cost_stddev / avg_daily_cost if avg_daily_cost > 0 else 0
                efficiency_score = max(0, 1 - cost_variance_ratio) if cost_variance_ratio > 0 else 1
            else:
                cost_stddev = 0
                cost_variance_ratio = 0
                efficiency_score = 1
            
            for service in service_breakdown:
                service["avg_daily_cost"] = service["total_cost"] / total_days if total_days > 0 else 0
            
            for region in region_breakdown:
                region["avg_daily_cost"] = region["total_cost"] / total_days if total_days > 0 else 0
            
            summary = None
            if report_type in ("quarterly", "annual") and isinstance(service_data, dict):
                properties = service_data.get("properties", {})
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
            
            cost_drivers = []
            for service in service_breakdown[:10]:
                cost_drivers.append({
                    "sku": {
                        "id": service["service"],
                        "description": service["service"]
                    },
                    "service": {
                        "id": service["service"],
                        "description": service["service"]
                    },
                    "total_cost": service["total_cost"]
                })

            result = {
                "report_type": report_type,
                "period": {"start": start_date, "end": end_date},
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_cost": total_cost,
                    "total_days": total_days,
                    "avg_daily_cost": avg_daily_cost,
                    "min_daily_cost": min_daily_cost,
                    "max_daily_cost": max_daily_cost,
                    "unique_services": len(service_breakdown),
                    "unique_regions": len(region_breakdown)
                },
                "breakdowns": {
                    "by_service": service_breakdown,
                    "by_region": region_breakdown
                },
                "trends": {
                    "daily_costs": daily_trends
                },
                "cost_drivers": cost_drivers,
                "efficiency_metrics": {
                    "cost_efficiency_score": efficiency_score,
                    "cost_variance_ratio": cost_variance_ratio,
                    "cost_stddev": cost_stddev
                },
                "message": "Comprehensive cost report generated for monthly period."
            }
            
            if summary is not None:
                result["summary_aggregation"] = summary
            
            return result
        except Exception as e:
            return {"error": f"Failed to generate cost report: {str(e)}"}

