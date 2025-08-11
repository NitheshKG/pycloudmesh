# Azure FinOps API Documentation

## 1. Cost Management

### get_cost_data
Fetches raw cost and usage data from Azure Cost Management API.

**Signature:**
```python
def get_cost_data(
    self,
    scope: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "Monthly",
    metrics: Optional[List[str]] = None,
    group_by: Optional[List[str]] = None,
    filter_: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.)
- `start_date` (str, optional): Start date (YYYY-MM-DD). Defaults to first day of current month.
- `end_date` (str, optional): End date (YYYY-MM-DD). Defaults to today.
- `granularity` (str): "Daily", "Monthly", or "None". Defaults to "Monthly".
- `metrics` (list, optional): List of cost metrics. Defaults to standard cost metrics.
- `group_by` (list, optional): Grouping criteria. **Required for breakdowns by service, resource, etc.**
- `filter_` (dict, optional): Filter criteria.

**Valid group_by fields by scope:**

| Scope Type         | Example Scope String                                               | Valid group_by fields                                                                                       |
|--------------------|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Subscription/Resource Group | `/subscriptions/{subscription-id}/`<br>`/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/` | `ResourceType`, `ResourceLocation`, `ResourceGroupName`                                                     |
| Billing Account    | `/providers/Microsoft.Billing/billingAccounts/{billing-account-id}`| `SubscriptionId`, `BillingProfileId`, `InvoiceSectionId`, `Product`, `Meter`, `ServiceFamily`, `ServiceName`, `ResourceGroup`, `ResourceId`, `ResourceType`, `ChargeType`, `PublisherType`, `BillingPeriod` |

**Common group_by use cases:**

| Use Case                | group_by Example                | granularity Example | Description                                      |
|-------------------------|---------------------------------|--------------------|--------------------------------------------------|
| By service              | `["ServiceName"]`              | "Monthly"         | Cost per service for each month                  |
| By resource             | `["ResourceId"]`               | "Monthly"         | Cost per resource for each month                 |
| By resource group       | `["ResourceGroup"]`            | "Monthly"         | Cost per resource group for each month           |
| By date (trend)         | `None`                          | "Daily"           | Total cost per day (no breakdown)                |
| By date and service     | `["ServiceName"]`              | "Daily"           | Cost per service per day                         |
| By subscription         | `["SubscriptionId"]`           | "Monthly"         | Cost per subscription for each month (billing account scope) |

**Returns:**
- Cost data from Azure Cost Management.

**Examples:**
```python
# Cost per service per month
costs = azure.get_cost_data(
    "/providers/Microsoft.Billing/billingAccounts/your-billing-account-id",
    start_date="2024-01-01",
    end_date="2024-03-31",
    granularity="Monthly",
    group_by=["ServiceName"]
)
print(costs)
```

**Sample Response:**
```json
{
    "id": "subscriptions/your-subscription-id/providers/Microsoft.CostManagement/query/abc123",
    "name": "abc123",
    "type": "Microsoft.CostManagement/query",
    "properties": {
        "columns": [
            {"name": "Cost", "type": "Number"},
            {"name": "BillingMonth", "type": "Datetime"},
            {"name": "ServiceName", "type": "String"}
        ],
        "rows": [
            [125.50, "2024-01-01T00:00:00", "Virtual Machines"],
            [85.25, "2024-01-01T00:00:00", "Storage"],
            [45.75, "2024-01-01T00:00:00", "SQL Database"]
        ]
    },
    "total_items": 3,
    "pages_retrieved": 1,
    "has_more_pages": false,
    "request_type": "POST"
}
```

**Note:**
- If you do not specify `group_by`, you will only get the total cost for the period, not a breakdown by service/resource/etc.
- For a full list of valid group_by fields for your scope, see the Azure documentation or the table above.

---

### get_cost_analysis
Provides summarized cost analysis with Azure-specific dimensions.

**Signature:**
```python
def get_cost_analysis(
    self,
    scope: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    dimensions: Optional[List[str]] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.)
- `start_date` (str, optional): Start date for analysis.
- `end_date` (str, optional): End date for analysis.
- `dimensions` (list, optional): List of dimensions to analyze (e.g., ["ResourceType", "ResourceLocation", "ResourceGroupName"]).

**Returns:**
- Dictionary with cost analysis data including:
  - `period`: Start and end dates
  - `dimensions`: List of analyzed dimensions
  - `total_cost`: Total cost for the period
  - `cost_breakdown`: Cost breakdown by dimension combinations
  - `cost_trends`: Cost trends over time
  - `insights`: Generated insights about cost patterns

**Example:**
```python
analysis = azure.get_cost_analysis(
    "/subscriptions/your-subscription-id/",
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["ResourceType", "ResourceLocation"]
)
print(analysis)
```

**Sample Response:**
```json
{
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "dimensions": ["ResourceType", "ResourceLocation"],
    "total_cost": 1250.75,
    "cost_breakdown": {
        "Microsoft.Compute/virtualMachines": 650.50,
        "Microsoft.Storage/storageAccounts": 350.25,
        "Microsoft.Sql/servers": 250.00
    },
    "cost_trends": [
        {"date": "2024-01-01", "cost": 40.25},
        {"date": "2024-01-02", "cost": 42.50}
    ],
    "insights": [
        "Virtual Machines represent 52% of total costs",
        "Consider reserved instances for cost optimization",
        "Storage costs are within expected range"
    ]
}
```

---

### get_cost_trends
Analyzes cost trends over time with detailed patterns, growth rates, and insights.

**Signature:**
```python
def get_cost_trends(
    self,
    scope: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "Daily"
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.)
- `start_date` (str, optional): Start date for trend analysis.
- `end_date` (str, optional): End date for trend analysis.
- `granularity` (str, optional): Data granularity for trends. Defaults to "Daily".

**Returns:**
- Dictionary with comprehensive cost trends analysis including:
  - `period`: Analysis period (start and end dates)
  - `granularity`: Data granularity used
  - `total_periods`: Number of time periods analyzed
  - `total_cost`: Total cost over the period
  - `average_daily_cost`: Average cost per period
  - `cost_periods`: List of cost data points with dates and costs
  - `trend_direction`: Overall trend direction ("increasing", "decreasing", "stable")
  - `growth_rate`: Percentage change in cost over the period
  - `peak_periods`: Periods with highest costs
  - `low_periods`: Periods with lowest costs
  - `patterns`: Identified cost patterns (e.g., "High cost variability", "Consistent cost pattern")
  - `insights`: Generated insights about trends and patterns

**Example:**
```python
trends = azure.get_cost_trends(
    "/subscriptions/your-subscription-id/",
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily"
)
print(trends)
```

**Sample Response:**
```json
{
  "period": {"start": "2024-01-01", "end": "2024-01-31"},
  "granularity": "Daily",
  "total_periods": 31,
    "total_cost": 1250.75,
    "average_daily_cost": 40.35,
    "trend_direction": "increasing",
    "growth_rate": 8.5,
    "patterns": ["weekend_spikes", "monthly_cycle"],
    "insights": [
        "Costs are trending upward by 8.5%",
        "Peak usage occurs on weekends",
        "Consider optimization for cost reduction"
    ],
    "peak_periods": ["2024-01-15", "2024-01-22"],
    "low_periods": ["2024-01-05", "2024-01-12"],
    "cost_periods": [
        {"date": "2024-01-01", "cost": 38.25},
        {"date": "2024-01-02", "cost": 42.50},
        {"date": "2024-01-03", "cost": 41.75}
    ]
}
```
  "total_cost": 1250.75,
  "average_daily_cost": 40.35,
  "trend_direction": "increasing",
  "growth_rate": 15.2,
  "peak_periods": [{"date": "2024-01-15", "cost": 85.50}],
  "low_periods": [{"date": "2024-01-01", "cost": 12.25}],
  "patterns": ["High cost variability", "Weekend cost reduction"],
  "insights": [
    "Total cost over 31 periods: $1250.75",
    "Average cost per period: $40.35",
    "Cost trend is increasing (15.2% change)",
    "Peak cost period: 2024-01-15 ($85.50)"
  ]
}
```

### get_resource_costs
Provides comprehensive resource cost analysis with utilization insights and optimization recommendations.

**Signature:**
```python
def get_resource_costs(
    self,
    scope: str,
    resource_id: str,
    granularity: str = "Daily", 
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metrics: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.)
- `resource_id` (str): ID of the resource to get costs for
- `granularity` (str): Data granularity (Daily, Monthly). Default: "Daily"
- `start_date` (str, optional): Start date for cost data
- `end_date` (str, optional): End date for cost data
- `metrics` (str, optional): Cost metrics to include

**Returns:**
- Dictionary with comprehensive resource cost analysis including:
  - `resource_id`: Resource identifier
  - `resource_type`: Resource type classification
  - `period`: Time period covered
  - `granularity`: Data granularity
  - `total_cost`: Total cost calculation
  - `total_periods`: Number of periods analyzed
  - `active_periods`: Periods with costs > 0
  - `cost_periods`: Detailed daily cost breakdown
  - `cost_breakdown`: Usage type breakdown
  - `utilization_insights`: Utilization analysis and recommendations
  - `cost_trends`: Cost trend analysis
  - `recommendations`: Optimization recommendations

**Example:**
```python
resource_costs = azure.get_resource_costs(
    scope="/subscriptions/your-subscription-id/",
    resource_id="/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.Compute/virtualMachines/your-vm",
    start_date="2024-06-01",
    end_date="2024-06-30"
)
print(resource_costs)
```

**Sample Response:**
```json
{
   "resource_id": "/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.Compute/virtualMachines/your-vm",
   "resource_type": "Microsoft.Compute/virtualMachines",
   "period": {"start": "2024-06-01", "end": "2024-06-30"},
   "granularity": "Daily",
   "total_cost": 150.75,
   "total_periods": 30,
   "active_periods": 28,
   "cost_periods": [
      {"date": "2024-06-01", "cost": 5.25},
      {"date": "2024-06-02", "cost": 5.25}
   ],
   "cost_breakdown": {
      "compute": 140.50,
      "storage": 10.25
   },
   "utilization_insights": {
      "utilization_score": 0.85,
      "idle_days": 2,
      "recommendations": ["Consider stopping during off-hours"]
   },
   "cost_trends": {
      "trend_direction": "stable",
      "daily_average": 5.38
   },
   "recommendations": [
      "Consider reserved instances for cost savings",
      "Review idle periods for optimization opportunities"
   ]
}
```

## 2. Budget Management

### list_budgets
Lists Azure budgets for a scope (subscription, resource group, etc.).

**Signature:**
```python
def list_budgets(
    self,
    scope: str,
    api_version: str = "2024-08-01"
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.).
- `api_version` (str, optional): API version to use. Defaults to "2024-08-01".

**Returns:**
- List of budgets.

**Example:**
```python
budgets = azure.list_budgets(scope="/subscriptions/your-subscription-id/")
print(budgets)
```

**Sample Response:**
```json
{
    "value": [
        {
            "id": "/subscriptions/your-subscription-id/providers/Microsoft.Consumption/budgets/Monthly Budget",
            "name": "Monthly Budget",
            "type": "Microsoft.Consumption/budgets",
            "properties": {
                "amount": 1000.0,
                "timeGrain": "Monthly",
                "timePeriod": {
                    "startDate": "2024-01-01T00:00:00Z",
                    "endDate": "2024-12-31T23:59:59Z"
                },
                "currentSpend": {
                    "amount": 750.25,
                    "unit": "USD"
                },
                "notifications": {
                    "actual_80": {
                        "enabled": true,
                        "operator": "GreaterThan",
                        "threshold": 80.0,
                        "contactEmails": ["admin@example.com"]
                    }
                }
            }
        },
        {
            "id": "/subscriptions/your-subscription-id/providers/Microsoft.Consumption/budgets/Quarterly Budget",
            "name": "Quarterly Budget",
            "type": "Microsoft.Consumption/budgets",
            "properties": {
                "amount": 3000.0,
                "timeGrain": "Quarterly",
                "timePeriod": {
                    "startDate": "2024-01-01T00:00:00Z",
                    "endDate": "2024-12-31T23:59:59Z"
                },
                "currentSpend": {
                    "amount": 2250.75,
                    "unit": "USD"
                }
            }
        }
    ]
}
```

**Error Response (Authentication):**
```json
{
    "error": "Failed to list budgets: 401 Client Error: Unauthorized for url: https://management.azure.com/subscriptions/your-subscription-id/providers/Microsoft.Consumption/budgets?api-version=2024-08-01 - {\"error\":{\"code\":\"ExpiredAuthenticationToken\",\"message\":\"The access token has expired.\"}}"
}
```

---

### create_budget
Creates a new Azure budget with notifications and thresholds.

**Signature:**
```python
def create_budget(
    self,
    budget_name: str,
    amount: float,
    scope: str,
    notifications: List[Dict[str, Any]],
    time_grain: str = "Monthly",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    api_version: str = "2024-08-01"
) -> Dict[str, Any]:
```

**Parameters:**
- `budget_name` (str): Name of the budget.
- `amount` (float): Budget amount in the specified currency.
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.).
- `notifications` (List[Dict[str, Any]]): List of notification configurations
  - `enabled` (bool): Whether the notification is enabled
  - `operator` (str): Comparison operator (GreaterThan, GreaterThanOrEqualTo, LessThan, LessThanOrEqualTo)
  - `threshold` (float): Threshold percentage (0-100)
  - `contactEmails` (List[str]): List of email addresses to notify
  - `contactRoles` (Optional[List[str]]): List of contact roles (Owner, Contributor, Reader)
  - `contactGroups` (Optional[List[str]]): List of action group resource IDs
  - `locale` (Optional[str]): Locale for notifications (default: "en-us")
  - `thresholdType` (Optional[str]): Type of threshold (default: "Actual")
- `time_grain` (str): Time grain for the budget (Monthly, Quarterly, Annually).
- `start_date` (Optional[str]): Start date for the budget in YYYY-MM-DD format. Will be automatically adjusted to the first day of the month if not already.
- `end_date` (Optional[str]): End date for the budget in YYYY-MM-DD format. Defaults to 5 years from start date if not provided.
- `api_version` (str): API version to use for the Azure Budget API.

**Returns:**
- Budget creation response from Azure.

**Example:**
```python
budget = azure.create_budget(
    budget_name="Monthly Azure Budget",
    amount=3000.0,
    scope="/subscriptions/your-subscription-id/",
    notifications=[
        {
            "enabled": True,
            "operator": "GreaterThan",
            "threshold": 80.0,
            "contactEmails": ["admin@example.com", "finance@example.com"]
        },
        {
            "enabled": True,
            "operator": "GreaterThanOrEqualTo",
            "threshold": 100.0,
            "contactEmails": ["emergency@example.com"]
        }
    ],
    time_grain="Monthly"
)
print(budget)
```

**Sample Response:**
```json
{
    "id": "/subscriptions/your-subscription-id/providers/Microsoft.Consumption/budgets/Monthly Azure Budget",
    "name": "Monthly Azure Budget",
    "type": "Microsoft.Consumption/budgets",
    "properties": {
        "amount": 3000.0,
        "timeGrain": "Monthly",
        "timePeriod": {
            "startDate": "2024-01-01T00:00:00Z",
            "endDate": "2024-12-31T23:59:59Z"
        },
        "notifications": {
            "actual_80": {
                "enabled": true,
                "operator": "GreaterThan",
                "threshold": 80.0,
                "contactEmails": ["admin@example.com", "finance@example.com"]
            },
            "actual_100": {
                "enabled": true,
                "operator": "GreaterThanOrEqualTo",
                "threshold": 100.0,
                "contactEmails": ["emergency@example.com"]
            }
        }
    }
}
```

**Error Response (Authentication):**
```json
{
    "error": "Failed to create budget: 401 Client Error: Unauthorized for url: https://management.azure.com/subscriptions/your-subscription-id/providers/Microsoft.Consumption/budgets/Monthly%20Azure%20Budget?api-version=2024-08-01 - {\"error\":{\"code\":\"ExpiredAuthenticationToken\",\"message\":\"The access token has expired.\"}}"
}
```

---

### get_budget_notifications
Get notifications for a specific budget by name and scope.

**Signature:**
```python
def get_budget_notifications(
    self,
    budget_name: str,
    scope: str,
    api_version: str = "2024-08-01"
) -> Dict[str, Any]:
```

**Parameters:**
- `budget_name` (str): Name of the budget to retrieve.
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.).
- `api_version` (str, optional): API version to use. Defaults to "2024-08-01".

**Returns:**
- Budget details including notifications.

**Example:**
```python
budget = azure.get_budget_notifications(
    budget_name="Monthly Azure Budget",
    scope="/subscriptions/your-subscription-id/"
)
print(budget)
```

**Sample Response:**
```json
{
    "id": "/subscriptions/your-subscription-id/providers/Microsoft.Consumption/budgets/Monthly Azure Budget",
    "name": "Monthly Azure Budget",
    "type": "Microsoft.Consumption/budgets",
    "properties": {
        "amount": 1000.0,
        "timeGrain": "Monthly",
        "timePeriod": {
            "startDate": "2024-01-01T00:00:00Z",
            "endDate": "2024-12-31T23:59:59Z"
        },
        "currentSpend": {
            "amount": 750.25,
            "unit": "USD"
        },
        "notifications": {
            "actual_80": {
                "enabled": true,
                "operator": "GreaterThan",
                "threshold": 80.0,
                "contactEmails": ["admin@example.com", "finance@example.com"]
            },
            "actual_100": {
                "enabled": true,
                "operator": "GreaterThanOrEqualTo",
                "threshold": 100.0,
                "contactEmails": ["emergency@example.com"]
            }
        }
    }
}
```

**Error Response (Not Found):**
```json
{
    "error": "Failed to get budget: 404 Client Error: Not Found for url: https://management.azure.com/subscriptions/your-subscription-id/providers/Microsoft.Consumption/budgets/nonexistent-budget?api-version=2024-08-01"
}
```

## 3. Optimization & Recommendations

### get_advisor_recommendations
Get Azure Advisor recommendations for cost optimization.

**Signature:**
```python
def get_advisor_recommendations(
    self,
    api_version: str = "2025-01-01",
    filter: str = None
) -> Dict[str, Any]:
```

**Parameters:**
- `api_version` (str, optional): API version for the Advisor API. Defaults to "2025-01-01".
- `filter` (str, optional): OData filter string for server-side filtering (e.g., "Category eq 'Cost'").

**Returns:**
- Advisor recommendations (optionally filtered server-side).

**Example:**
```python
# All recommendations
advisor_recs = azure.get_advisor_recommendations()

# Only cost recommendations
advisor_recs = azure.get_advisor_recommendations(filter="Category eq 'Cost'")
```

**Sample Response:**
```json
{
    "value": [
        {
            "id": "/subscriptions/your-subscription-id/providers/Microsoft.Advisor/recommendations/12345678-1234-1234-1234-123456789012",
            "name": "12345678-1234-1234-1234-123456789012",
            "type": "Microsoft.Advisor/recommendations",
            "properties": {
                "category": "Cost",
                "impact": "Medium",
                "impactedField": "Microsoft.Compute/virtualMachines",
                "impactedValue": "your-vm-name",
                "lastUpdated": "2024-01-15T10:30:00Z",
                "recommendationTypeId": "e0754024-cd3b-4fa4-ac41-884e4caaa31f",
                "shortDescription": {
                    "problem": "Consider using Azure Reserved Instances",
                    "solution": "Purchase reserved instances to reduce costs"
                },
                "longDescription": {
                    "problem": "Your virtual machines are running on-demand pricing which is more expensive than reserved instances.",
                    "solution": "Purchase reserved instances for 1 or 3 years to save up to 72% on compute costs."
                },
                "resourceMetadata": {
                    "resourceId": "/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.Compute/virtualMachines/your-vm",
                    "source": "Azure Advisor"
                },
                "potentialSavings": {
                    "amount": 1200.00,
                    "currency": "USD"
                }
            }
        }
    ],
    "total_items": 1,
    "pages_retrieved": 1,
    "has_more_pages": false,
    "request_type": "GET"
}
```

---

### get_reserved_instance_recommendations
Get Azure Reserved Instance recommendations for a given scope.

**Signature:**
```python
def get_reserved_instance_recommendations(
    self,
    scope: str,
    api_version: str = "2024-08-01",
    filter: str = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope string (e.g., "/subscriptions/{subscription-id}").
- `api_version` (str, optional): API version for the Reservation Recommendations API. Defaults to "2024-08-01".
- `filter` (str, optional): OData filter string for server-side filtering (e.g., "ResourceGroup eq 'MyResourceGroup'").

**Returns:**
- Reserved Instance recommendations (optionally filtered server-side).

**Example:**
```python
reserved_recs = azure.get_reserved_instance_recommendations(
    scope="/subscriptions/your-subscription-id",
    filter="ResourceGroup eq 'MyResourceGroup'"
)
```

**Sample Response:**
```json
{
    "value": [
        {
            "id": "/subscriptions/your-subscription-id/providers/Microsoft.Consumption/reservationRecommendations/12345678-1234-1234-1234-123456789012",
            "name": "12345678-1234-1234-1234-123456789012",
            "type": "Microsoft.Consumption/reservationRecommendations",
            "properties": {
                "scope": "Shared",
                "region": "eastus",
                "lookBackPeriod": "Last30Days",
                "instanceFlexibilityRatio": 1,
                "instanceFlexibilityGroup": "DSv3 Series",
                "normalizedSize": "Standard_D2s_v3",
                "recommendedQuantity": 2,
                "meterId": "00000000-0000-0000-0000-000000000000",
                "term": "P1Y",
                "costWithNoReservedInstances": 175.20,
                "recommendedQuantityNormalized": 2,
                "totalCostWithReservedInstances": 87.60,
                "netSavings": 87.60,
                "firstUsageDate": "2024-01-01T00:00:00Z",
                "skuName": "Standard_D2s_v3",
                "resourceType": "virtualMachines"
            }
        }
    ],
    "total_items": 1,
    "pages_retrieved": 1,
    "has_more_pages": false,
    "request_type": "GET"
}
```

---

### get_optimization_recommendations
Get comprehensive optimization recommendations (advisor and reserved instance recommendations).

**Signature:**
```python
def get_optimization_recommendations(
    self,
    scope: str,
    filter: str = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope string (e.g., "/subscriptions/{subscription-id}").
- `filter` (str, optional): OData filter string to filter recommendations server-side (applies to both Advisor and Reserved Instance recommendations).

**Returns:**
- Dictionary with keys:
  - `'advisor_recommendations'`: List of Azure Advisor recommendations (optionally filtered).
  - `'reserved_instance_recommendations'`: List of Reserved Instance recommendations (optionally filtered).

**Example:**
```python
# All recommendations for a subscription
optimizations = azure.get_optimization_recommendations(
    scope="/subscriptions/your-subscription-id"
)

# Only cost recommendations for a subscription
optimizations = azure.get_optimization_recommendations(
    scope="/subscriptions/your-subscription-id",
    filter="Category eq 'Cost'"
)
```

## 4. Advanced Analytics

### get_cost_forecast
Get unified cost forecast for the specified period with AI/ML enhanced predictions and statistical analysis.

**Signature:**
```python
def get_cost_forecast(
    self,
    scope: str,
    api_version: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    forecast_period: int = 30,
    payload: Optional[dict] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.)
- `api_version` (str): API version for the Azure Cost Management API
- `start_date` (str, optional): Start date for historical data (YYYY-MM-DD). Defaults to 3 months ago.
- `end_date` (str, optional): End date for historical data (YYYY-MM-DD). Defaults to today.
- `forecast_period` (int, optional): Number of days to forecast. Default: 12.
- `payload` (dict, optional): Custom payload for the query. If not provided, uses default payload.

**Returns:**
- Dictionary with unified cost forecast data including:
  - `forecast_period`: Number of days forecasted
  - `start_date`: Historical data start date
  - `end_date`: Historical data end date
  - `total_historical_cost`: Total cost for historical period
  - `total_forecast_cost`: Total forecasted cost
  - `average_daily_cost`: Average daily cost
  - `forecast_results`: Daily forecast values with confidence intervals
  - `ai_model_used`: Whether AI model was used
  - `model_accuracy`: Accuracy metrics (MAPE, RMSE, MAE)
  - `insights`: Cost insights and trends
  - `granularity`: Data granularity
  - `message`: Status message

**Example:**
```python
forecast = azure.get_cost_forecast(
    scope="/subscriptions/your-subscription-id/",
    api_version="2025-03-01",
    start_date="2025-05-01",
    end_date="2025-07-31",
    forecast_period=30
)
print(forecast)
```

**Sample Response:**
```json
{
    "forecast_period": 30,
    "start_date": "2025-05-01",
    "end_date": "2025-07-31",
    "total_historical_cost": 326.84,
    "total_forecast_cost": 383.4,
    "average_daily_cost": 13.62,
    "forecast_results": [
        {
            "date": "2025-07-30",
            "forecast_value": 12.78,
            "lower_bound": 6.8,
            "upper_bound": 18.76,
            "confidence_level": 0.95
        },
        {
            "date": "2025-07-31",
            "forecast_value": 12.78,
            "lower_bound": 6.8,
            "upper_bound": 18.76,
            "confidence_level": 0.95
        }
    ],
    "ai_model_used": false,
    "model_accuracy": {
        "mape": 12.28,
        "rmse": 3.05,
        "mean_absolute_error": 1.67
    },
    "insights": [
        "Historical average daily cost: 13.62",
        "Recent 7-day trend: 5.1% change",
        "Forecasted total cost for 30 days: 383.40"
    ],
    "granularity": "Daily",
    "message": "Unified cost forecast generated for 30 days using statistical analysis"
}
```

---

#### Payload Structure

You can provide a custom `payload` dictionary to control the forecast query. If you do **not** provide a payload, a sensible default is used (see below).

**Payload keys:**

| Key                    | Type     | Description                                                                                  | Example/Options                |
|------------------------|----------|----------------------------------------------------------------------------------------------|-------------------------------|
| `type`                 | string   | Query type.                                                                                  | `"Usage"` (default)           |
| `timeframe`            | string   | Time window for the query.                                                                   | `"Custom"`, `"MonthToDate"`, `"YearToDate"`, `"BillingMonthToDate"`, `"TheLastMonth"` |
| `timePeriod`           | object   | Custom date range. Required if `timeframe` is `"Custom"`.                                   | `{ "from": ..., "to": ... }` |
| `dataset`              | object   | Dataset options (see below).                                                                 | See below                     |
| `includeActualCost`    | boolean  | Whether to include actual cost.                                                              | `False` (default)             |
| `includeFreshPartialCost` | boolean | Whether to include fresh partial cost.                                                      | `False` (default)             |

**Dataset keys:**

| Key           | Type     | Description                                         | Example/Options                |
|---------------|----------|-----------------------------------------------------|-------------------------------|
| `granularity` | string   | Data granularity                                    | `"Daily"`                     |
| `aggregation` | object   | Aggregation definition                              | See below                     |
| `filter`      | object   | (Optional) OData filter for advanced filtering      | See Azure docs                |

**Aggregation keys:**

| Key         | Type     | Description                        | Example/Options                |
|-------------|----------|------------------------------------|-------------------------------|
| `name`      | string   | Metric to aggregate                | `"Cost"`, `"ActualCost"`, `"PreTaxCost"` |
| `function`  | string   | Aggregation function               | `"Sum"`                       |

---

#### Example Payloads

**Default payload (used if you do not provide one):**
```python
{
    "type": "Usage",
    "timeframe": "Custom",
    "timePeriod": {
        "from": "<start_date>",
        "to": "<end_date>"
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
```
- `<start_date>`: First day of the month, three months ago (UTC, ISO 8601)
- `<end_date>`: Today at midnight UTC

**Custom payload with filter and daily granularity:**
```python
payload = {
    "type": "Usage",
    "timeframe": "Custom",
    "timePeriod": {
        "from": "2024-01-01T00:00:00+00:00",
        "to": "2024-03-31T00:00:00+00:00"
    },
    "dataset": {
        "granularity": "Daily",
        "aggregation": {
            "totalCost": {
                "name": "ActualCost",
                "function": "Sum"
            }
        },
        "filter": {
            "dimensions": {
                "name": "ResourceGroup",
                "operator": "In",
                "values": ["API", "WebApp"]
            }
        }
    },
    "includeActualCost": False,
    "includeFreshPartialCost": False
}
```

---

#### Usage Examples

**Using the default payload:**
```python
forecast = azure.get_cost_forecast(
    scope="/subscriptions/your-subscription-id",
    api_version="2023-08-01"
)
```

**Using a custom payload:**
```python
payload = {
    "type": "Usage",
    "timeframe": "Custom",
    "timePeriod": {
        "from": "2024-01-01T00:00:00+00:00",
        "to": "2024-03-31T00:00:00+00:00"
    },
    "dataset": {
        "granularity": "Daily",
        "aggregation": {
            "totalCost": {
                "name": "ActualCost",
                "function": "Sum"
            }
        }
    }
}
forecast = azure.get_cost_forecast(
    scope="/subscriptions/your-subscription-id",
    api_version="2023-08-01",
    payload=payload
)
```

---

#### Notes

- If you do **not** provide a payload, the default is a daily forecast for the last three months, aggregating by `"Cost"` and `"Sum"`.
- You can fully customize the payload to use any valid Azure Cost Management API options.
- For advanced filtering, see [Azure Cost Management API documentation](https://learn.microsoft.com/en-us/rest/api/cost-management/forecast/usage?tabs=HTTP).
- The `granularity` in the payload must be `"Daily"` for the forecast API.
- The `timeframe` in the payload must be `"Custom"` or one of the predefined options (`"MonthToDate"`, `"YearToDate"`, `"BillingMonthToDate"`, `"TheLastMonth"`).
- The `timePeriod` in the payload must be provided if `timeframe` is `"Custom"`.
- The `dataset` in the payload must include `"granularity": "Daily"` and `"aggregation": { ... }`.
- The `includeActualCost` and `includeFreshPartialCost` in the payload are boolean flags.
- The `filter` in the payload is an optional OData filter for advanced filtering.
- **Note:** The `granularity` in the payload must be `"Daily"` for the forecast API. If you need a monthly forecast, you must aggregate the daily results.

---

### get_cost_anomalies

Get cost anomalies using Azure Cost Management query API.

**Signature:**
```python
def get_cost_anomalies(
    self,
    scope: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    api_version: str = "2023-03-01",
    payload: Optional[dict] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.)
- `start_date` (str, optional): Start date for analysis (YYYY-MM-DD). Defaults to 30 days ago.
- `end_date` (str, optional): End date for analysis (YYYY-MM-DD). Defaults to today.
- `api_version` (str, optional): API version for the Cost Management API.
- `payload` (dict, optional): Custom payload for the query. If not provided, uses default payload.

**Returns:**
- Dictionary containing:
  - `scope`: The Azure scope used for analysis
  - `period`: Start and end dates of the analysis period
  - `anomalies`: List of detected anomalies with details
  - `total_records`: Number of anomalies found
  - `cost_data`: Raw cost data from Azure API

**Anomaly Detection Details:**
- Uses statistical analysis (mean and standard deviation)
- Identifies anomalies using 2-standard-deviation threshold
- Categorizes anomalies as "spike" or "drop"
- Assigns severity levels ("high" or "medium")
- Each anomaly includes:
  - Date of occurrence
  - Actual cost vs expected cost
  - Deviation amount and percentage
  - Anomaly type and severity
  - Statistical threshold used

**Example:**
```python
# Basic usage (last 30 days)
anomalies = azure.get_cost_anomalies(
    scope="/subscriptions/your-subscription-id"
)

# Custom date range
anomalies = azure.get_cost_anomalies(
    scope="/subscriptions/your-subscription-id",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# With custom payload
custom_payload = {
    "type": "Usage",
    "timeframe": "Custom",
    "timePeriod": {
        "from": "2024-01-01",
        "to": "2024-01-31"
    },
    "dataset": {
        "granularity": "Daily",
        "aggregation": {
            "totalCost": {
                "name": "Cost",
                "function": "Sum"
            }
        },
        "filter": {
            "dimensions": {
                "name": "ResourceGroup",
                "operator": "In",
                "values": ["Production", "Development"]
            }
        }
    }
}

anomalies = azure.get_cost_anomalies(
    scope="/subscriptions/your-subscription-id",
    payload=custom_payload
)
```

**Sample Response:**
```json
{
  "scope": "/subscriptions/your-subscription-id",
  "period": {"start": "2024-01-01", "end": "2024-01-31"},
  "anomalies": [
    {
      "date": "2024-01-15",
      "cost": 150.25,
      "expected_cost": 75.50,
      "deviation": 74.75,
      "deviation_percentage": 99.0,
      "type": "spike",
      "severity": "high",
      "threshold": 25.30
    }
  ],
  "total_records": 1,
  "cost_data": {
    "properties": {
      "nextLink": null,
      "columns": [
        {"name": "Cost", "type": "Number"},
        {"name": "UsageDate", "type": "Number"},
        {"name": "Currency", "type": "String"}
      ],
      "rows": [
        [150.25, "20240115", "USD"],
        [75.50, "20240116", "USD"]
      ]
    },
    "total_items": 2,
    "pages_retrieved": 1,
    "has_more_pages": false,
    "request_type": "POST"
  }
}
```

---

### get_cost_efficiency_metrics
Calculate real cost efficiency metrics from Azure Cost Management API.

**Signature:**
```python
def get_cost_efficiency_metrics(
    self,
    scope: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    user_count: Optional[int] = None,
    transaction_count: Optional[int] = None,
    api_version: str = "2023-03-01"
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.)
- `start_date` (str, optional): Start date for analysis (YYYY-MM-DD). Defaults to first day of current month.
- `end_date` (str, optional): End date for analysis (YYYY-MM-DD). Defaults to today.
- `user_count` (int, optional): Number of users for cost per user calculation
- `transaction_count` (int, optional): Number of transactions for cost per transaction calculation
- `api_version` (str, optional): API version for the Cost Management API

**Returns:**
- Dictionary containing comprehensive efficiency metrics:
  - `total_cost`: Total cost for the period
  - `cost_by_service`: Cost breakdown by Azure service
  - `period`: Analysis period (start and end dates)
  - `total_days_analyzed`: Number of days analyzed
  - `cost_per_user`: Cost per user (if user_count provided)
  - `cost_per_transaction`: Cost per transaction (if transaction_count provided)
  - `avg_daily_cost`: Average daily cost
  - `cost_stddev`: Standard deviation of daily costs
  - `cost_variance_ratio`: Variance ratio for efficiency scoring
  - `cost_efficiency_score`: Overall efficiency score (0-1)
  - `waste_days`: Number of days with high cost variance
  - `waste_percentage`: Percentage of days with waste

**Example:**
```python
# Basic usage
efficiency = azure.get_cost_efficiency_metrics(
    scope="/subscriptions/your-subscription-id"
)

# With custom parameters
efficiency = azure.get_cost_efficiency_metrics(
    scope="/subscriptions/your-subscription-id",
    start_date="2024-01-01",
    end_date="2024-01-31",
    user_count=100,
    transaction_count=10000
)
```

**Sample Response:**
```json
{
  "efficiency_metrics": {
    "total_cost": 329.41,
    "cost_by_service": {
      "Bandwidth": 0.0,
      "Storage": 95.38,
      "Virtual Machines": 0.0,
      "Virtual Network": 234.02
    },
    "period": {"start": "2025-07-01", "end": "2025-07-29"},
    "total_days_analyzed": 54,
    "avg_daily_cost": 6.1,
    "cost_stddev": 3.72,
    "cost_variance_ratio": 0.61,
    "cost_efficiency_score": 0.695,
    "waste_days": 22,
    "waste_percentage": 40.7
  }
}
```

---

## Cost Reports

### `generate_cost_report`

Generate comprehensive cost report for a given Azure scope with unified format across all cloud providers.

**Signature:**
```python
def generate_cost_report(
    self,
    scope: str,
    report_type: str = "monthly",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metrics: Optional[list] = None,
    group_by: Optional[list] = None,
    filter_: Optional[dict] = None
) -> Dict[str, Any]
```

**Parameters:**
- `scope` (str, required): Azure scope. Examples:
    - Subscription: `/subscriptions/{subscription-id}/`
    - Resource Group: `/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/`
    - Billing Account: `/providers/Microsoft.Billing/billingAccounts/{billing-account-id}`
- `report_type` (str, optional): Type of report (`"monthly"`, `"quarterly"`, `"annual"`). Controls default date range and summary aggregation. Defaults to `"monthly"`.
- `start_date` (str, optional): Start date for report (YYYY-MM-DD). If not provided, defaults based on `report_type`.
- `end_date` (str, optional): End date for report (YYYY-MM-DD). If not provided, defaults based on `report_type`.
- `metrics` (list, optional): List of cost metrics to aggregate (e.g., `["Cost"]`).
- `group_by` (list, optional): List of dimensions to group by (e.g., `["ServiceName"]`).
- `filter_` (dict, optional): Additional filter criteria for the query.

**Returns:**
- `Dict[str, Any]`: Unified cost report format with processed data
- For quarterly/annual reports, includes `summary_aggregation` with totals by quarter or year

**Example:**
```python
azure = AzureFinOpsAnalytics(subscription_id="your_subscription", token="your_token")

# Monthly report
monthly_report = azure.generate_cost_report(
    scope="/subscriptions/your-subscription-id/",
    report_type="monthly",
    start_date="2025-07-01",
    end_date="2025-07-31"
)

# Quarterly report with summary aggregation
quarterly_report = azure.generate_cost_report(
    scope="/subscriptions/your-subscription-id/",
    report_type="quarterly"
)
```

**Sample Response:**
```json
{
    "report_type": "monthly",
    "period": {
        "start": "2025-07-01",
        "end": "2025-07-31"
    },
    "generated_at": "2025-07-31T02:10:14.812717",
    "summary": {
        "total_cost": 342.262857396059,
        "total_days": 0,
        "avg_daily_cost": 0,
        "min_daily_cost": 0,
        "max_daily_cost": 0,
        "unique_services": 4,
        "unique_regions": 1
    },
    "breakdowns": {
        "by_service": [
            {
                "service": "Bandwidth",
                "total_cost": 6.59311298048125e-05,
                "avg_daily_cost": 0
            },
            {
                "service": "Storage",
                "total_cost": 95.3836169510402,
                "avg_daily_cost": 0
            },
            {
                "service": "Virtual Machines",
                "total_cost": 0.0,
                "avg_daily_cost": 0
            },
            {
                "service": "Virtual Network",
                "total_cost": 246.879174513889,
                "avg_daily_cost": 0
            }
        ],
        "by_region": [
            {
                "region": "us east",
                "total_cost": 342.26285739606,
                "avg_daily_cost": 0
            }
        ]
    },
    "trends": {
        "daily_costs": []
    },
    "cost_drivers": [
        {
            "sku": {
                "id": "Bandwidth",
                "description": "Bandwidth"
            },
            "service": {
                "id": "Bandwidth",
                "description": "Bandwidth"
            },
            "total_cost": 6.59311298048125e-05
        },
        {
            "sku": {
                "id": "Storage",
                "description": "Storage"
            },
            "service": {
                "id": "Storage",
                "description": "Storage"
            },
            "total_cost": 95.3836169510402
        }
    ],
    "efficiency_metrics": {
        "cost_efficiency_score": 1,
        "cost_variance_ratio": 0,
        "cost_stddev": 0
    },
    "message": "Comprehensive cost report generated for monthly period."
}
```

## 5. Governance & Compliance

### get_governance_policies
Get Azure governance policies and compliance status for cost management.

**Signature:**
```python
def get_governance_policies(self, scope: str, tag_names: Optional[List[str]] = None) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, etc.).
    - Example: "/subscriptions/{subscription-id}/"
- `tag_names` (List[str], optional): List of tag names to use for cost allocation analysis. If not provided, all available tags will be used.

**Returns:**
- `Dict[str, Any]`: Dictionary with unified structure:
    - `cost_allocation_labels`: Cost allocation analysis grouped by tags/dimensions (unified with AWS/GCP)
    - `policy_compliance`: Compliance status for cost-related policies (unified with AWS/GCP) 
    - `cost_policies`: List of cost-related governance policies

**Note:** This method is designed to return all three sections, but currently only the `policy_compliance` section is fully implemented. The `cost_allocation_labels` and `cost_policies` sections are available as separate methods but not yet integrated into this unified response.

**Example:**
```python
governance_data = azure.get_governance_policies(
    scope="/subscriptions/your-subscription-id/",
    tag_names=["Environment", "Project"]
)
```

**Sample Response:**
```json
{
    "cost_allocation_labels": {
        "tag_groups": [
            {
                "tag_name": "Environment",
                "costs": [
                    {
                        "tag_value": "Production",
                        "cost": 1250.50,
                        "percentage": 65.2
                    },
                    {
                        "tag_value": "Development",
                        "cost": 668.30,
                        "percentage": 34.8
                    }
                ]
            },
            {
                "tag_name": "Project",
                "costs": [
                    {
                        "tag_value": "FinOps",
                        "cost": 1918.80,
                        "percentage": 100.0
                    }
                ]
            }
        ],
        "total_cost": 1918.80,
        "available_tags": ["Environment", "Project", "Department"],
        "message": "Cost allocation analysis completed using Azure Cost Management API"
    },
    "policy_compliance": {
        "scope": "/subscriptions/your-subscription-id/",
        "total_policies": 14,
        "total_assignments": 0,
        "cost_related_policies": [
            {
                "properties": {
                    "displayName": "Azure Backup should be enabled for Virtual Machines",
                    "policyType": "BuiltIn",
                    "mode": "Indexed",
                    "description": "Ensure protection of your Azure Virtual Machines by enabling Azure Backup. Azure Backup is a secure and cost effective data protection solution for Azure.",
                    "metadata": {
                        "version": "3.0.0",
                        "category": "Backup"
                    },
                    "version": "3.0.0",
                    "parameters": {
                        "effect": {
                            "type": "String",
                            "metadata": {
                                "displayName": "Effect",
                                "description": "Enable or disable the execution of the policy"
                            },
                            "allowedValues": [
                                "AuditIfNotExists",
                                "Disabled"
                            ],
                            "defaultValue": "AuditIfNotExists"
                        }
                    }
                },
                "id": "/providers/Microsoft.Authorization/policyDefinitions/013e242c-8828-4970-87b3-ab247555486d",
                "type": "Microsoft.Authorization/policyDefinitions",
                "name": "013e242c-8828-4970-87b3-ab247555486d"
            }
        ],
        "cost_related_assignments": [],
        "compliance_score": 0.0,
        "compliance_status": "Non-compliant",
        "cost_governance_insights": [
            "Found 14 cost-related policies",
            "Active assignments: 0",
            "Compliance score: 0.0%",
            "Note: Detailed compliance requires Azure Policy Insights API access"
        ],
        "message": "Policy compliance status retrieved from Azure Policy API"
    },
    "cost_policies": {
        "policies": [
            {
                "id": "/subscriptions/your-subscription-id/providers/Microsoft.Authorization/policyDefinitions/12345678-1234-1234-1234-123456789012",
                "name": "Require cost center tag",
                "description": "Enforces cost center tagging for all resources",
                "category": "Cost Management",
                "effect": "Deny",
                "parameters": {
                    "tagName": "costCenter"
                }
            },
            {
                "id": "/subscriptions/your-subscription-id/providers/Microsoft.Authorization/policyDefinitions/87654321-4321-4321-4321-210987654321",
                "name": "Budget enforcement",
                "description": "Enforces budget limits for resource groups",
                "category": "Cost Management",
                "effect": "Audit",
                "parameters": {
                    "budgetAmount": 1000
                }
            }
        ],
        "total_policies": 2,
        "message": "Cost management policies retrieved from Azure Policy API"
    }
}
```

---

### get_cost_allocation_tags
Get cost allocation tags for Azure resources.

**Signature:**
```python
def get_cost_allocation_tags(self) -> Dict[str, Any]:
```

**Returns:**
- Cost allocation tags for Azure resources.

**Example:**
```python
tags = azure.get_cost_allocation_tags()
```

---

### get_policy_compliance
Get policy compliance status with focus on cost-related policies for FinOps governance.

**Signature:**
```python
def get_policy_compliance(self, scope: Optional[str] = None) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (Optional[str]): Azure scope to check compliance for. If not provided, checks at subscription level.

**Returns:**
- Dictionary containing:
  - `scope`: The scope being checked
  - `total_policies`: Number of cost-related policies found
  - `compliant_resources`: Number of compliant resources
  - `non_compliant_resources`: Number of non-compliant resources
  - `cost_related_policies`: List of cost-related policies with compliance status
  - `compliance_score`: Overall compliance percentage
  - `cost_governance_insights`: Insights about cost governance effectiveness

**Example:**
```python
# Check compliance at subscription level
compliance = azure.get_policy_compliance()

# Check compliance at resource group level
compliance = azure.get_policy_compliance(
    scope="/subscriptions/your-subscription-id/resourceGroups/your-rg/"
)

# Access compliance insights
print(f"Compliance Score: {compliance['compliance_score']:.1f}%")
for insight in compliance['cost_governance_insights']:
    print(f"Insight: {insight}")
```

## 6. Reservation Management

### get_reservation_cost
Get Azure reservation utilization and cost data.

**Signature:**
```python
def get_reservation_cost(
    self,
    scope: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, etc.).
    - Example: "/subscriptions/{subscription-id}/"
- `start_date` (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
- `end_date` (str, optional): End date in YYYY-MM-DD format. Defaults to last day of current month.

**Returns:**
- Reservation utilization data from Azure Cost Management.

**Example:**
```python
# Get reservation costs for a subscription with default date range
reservation_costs = azure.get_reservation_cost(
    scope="/subscriptions/your-subscription-id/"
)

# Get reservation costs for a specific date range
reservation_costs = azure.get_reservation_cost(
    scope="/subscriptions/your-subscription-id/",
    start_date="2024-06-01",
    end_date="2024-06-30"
)

# Get reservation costs for a resource group
reservation_costs = azure.get_reservation_cost(
    scope="/subscriptions/your-subscription-id/resourceGroups/your-rg/"
)
```

---

### get_reservation_recommendation
Get Azure reservation recommendations for various services.

This method retrieves reservation purchase recommendations based on your usage patterns.
You can filter recommendations by various criteria using OData filter syntax.

**Signature:**
```python
def get_reservation_recommendation(
    self,
    scope: str,
    filter: Optional[str] = None,
    api_version: str = "2024-08-01"
) -> List[Dict[str, Any]]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, etc.).
    - Example: "/subscriptions/{subscription-id}/"
- `filter` (str, optional): OData filter string for server-side filtering.
    - Common filter examples:
        - `"ResourceGroup eq 'MyResourceGroup'"` - Filter by resource group
        - `"Location eq 'eastus'"` - Filter by Azure region
        - `"Sku eq 'Standard_D2s_v3'"` - Filter by VM SKU
        - `"Term eq 'P1Y'"` - Filter by 1-year term
        - `"Term eq 'P3Y'"` - Filter by 3-year term
        - `"Location eq 'eastus' and Term eq 'P1Y'"` - Combine filters
- `api_version` (str, optional): API version for the Consumption API. Defaults to "2024-08-01".

**Returns:**
- `List[Dict[str, Any]]`: List of reservation recommendations with details including:
    - Resource group, location, SKU information
    - Recommended quantity and term
    - Potential savings
    - Usage data used for recommendations

**Example:**
```python
# Get all recommendations for a subscription
recommendations = azure.get_reservation_recommendation(
    scope="/subscriptions/your-subscription-id/"
)

# Filter by resource group
recommendations = azure.get_reservation_recommendation(
    scope="/subscriptions/your-subscription-id/",
    filter="ResourceGroup eq 'Production'"
)

# Filter by location and term
recommendations = azure.get_reservation_recommendation(
    scope="/subscriptions/your-subscription-id/",
    filter="Location eq 'eastus' and Term eq 'P1Y'"
)

# Filter by specific VM SKU
recommendations = azure.get_reservation_recommendation(
    scope="/subscriptions/your-subscription-id/",
    filter="Sku eq 'Standard_D2s_v3'"
)

# Complex filter with multiple conditions
recommendations = azure.get_reservation_recommendation(
    scope="/subscriptions/your-subscription-id/",
    filter="ResourceGroup eq 'Production' and Location eq 'eastus' and Term eq 'P3Y'"
)
```

**Sample Response:**
```json
{
    "value": [
        {
            "id": "/subscriptions/your-subscription-id/providers/Microsoft.Consumption/reservationRecommendations/12345678-1234-1234-1234-123456789012",
            "name": "12345678-1234-1234-1234-123456789012",
            "type": "Microsoft.Consumption/reservationRecommendations",
            "properties": {
                "scope": "Shared",
                "region": "eastus",
                "lookBackPeriod": "Last30Days",
                "instanceFlexibilityRatio": 1,
                "instanceFlexibilityGroup": "DSv3 Series",
                "normalizedSize": "Standard_D2s_v3",
                "recommendedQuantity": 2,
                "meterId": "00000000-0000-0000-0000-000000000000",
                "term": "P1Y",
                "costWithNoReservedInstances": 175.20,
                "recommendedQuantityNormalized": 2,
                "totalCostWithReservedInstances": 87.60,
                "netSavings": 87.60,
                "firstUsageDate": "2024-01-01T00:00:00Z",
                "scope": "Shared",
                "skuName": "Standard_D2s_v3",
                "resourceType": "virtualMachines"
            }
        },
        {
            "id": "/subscriptions/your-subscription-id/providers/Microsoft.Consumption/reservationRecommendations/87654321-4321-4321-4321-210987654321",
            "name": "87654321-4321-4321-4321-210987654321",
            "type": "Microsoft.Consumption/reservationRecommendations",
            "properties": {
                "scope": "Single",
                "region": "westus2",
                "lookBackPeriod": "Last30Days",
                "instanceFlexibilityRatio": 1,
                "instanceFlexibilityGroup": "ESv3 Series",
                "normalizedSize": "Standard_E2s_v3",
                "recommendedQuantity": 1,
                "meterId": "11111111-1111-1111-1111-111111111111",
                "term": "P3Y",
                "costWithNoReservedInstances": 262.80,
                "recommendedQuantityNormalized": 1,
                "totalCostWithReservedInstances": 131.40,
                "netSavings": 131.40,
                "firstUsageDate": "2024-01-15T00:00:00Z",
                "scope": "Single",
                "skuName": "Standard_E2s_v3",
                "resourceType": "virtualMachines"
            }
        }
    ],
    "total_items": 2,
    "pages_retrieved": 1,
    "has_more_pages": false,
    "request_type": "GET"
}
```

---

### get_reservation_order_details
Get Azure reservation order details.

**Signature:**
```python
def get_reservation_order_details(self, **kwargs) -> Dict[str, Any]:
```

**Parameters:**
- `api_version` (str, optional): API version for the Azure Reservation API. Defaults to "2022-11-01".

**Returns:**
- Reservation order details as returned by the Azure API. If the API call fails, returns a dictionary with an "error" key and message.

**Example:**
```python
# Get reservation order details with default API version
order_details = azure.get_reservation_order_details()

# Get reservation order details with specific API version
order_details = azure.get_reservation_order_details(api_version="2022-11-01")
```

## 📋 Azure Budget Management Examples

### Basic Budget Creation
```python
# Create a simple monthly budget with email notifications
budget = azure.create_budget(
    budget_name="monthly-budget",
    amount=1000.0,
    scope="/subscriptions/your-subscription-id/",
    notifications=[
        {
            "enabled": True,
            "operator": "GreaterThan",
            "threshold": 80.0,
            "contactEmails": ["admin@company.com", "finance@company.com"]
        }
    ]
)
```

### Advanced Budget with Multiple Notifications
```python
# Create a quarterly budget with multiple notification thresholds
budget = azure.create_budget(
    budget_name="quarterly-budget",
    amount=5000.0,
    scope="/subscriptions/your-subscription-id/",
    notifications=[
        {
            "enabled": True,
            "operator": "GreaterThan",
            "threshold": 75.0,
            "contactEmails": ["admin@company.com"],
            "contactRoles": ["Owner", "Contributor"],
            "locale": "en-us",
            "thresholdType": "Actual"
        },
        {
            "enabled": True,
            "operator": "GreaterThanOrEqualTo",
            "threshold": 100.0,
            "contactEmails": ["emergency@company.com"],
            "locale": "en-us",
            "thresholdType": "Actual"
        }
    ],
    time_grain="Quarterly",
    start_date="2024-01-01"
)
```

### Different Scope Types
```python
# Subscription-level budget
azure.create_budget(
    budget_name="subscription-budget",
    amount=2000.0,
    scope="/subscriptions/your-subscription-id/",
    notifications=[...]
)

# Resource Group-level budget
azure.create_budget(
    budget_name="rg-budget",
    amount=500.0,
    scope="/subscriptions/your-subscription-id/resourceGroups/your-rg/",
    notifications=[...]
)

# Billing Account-level budget
azure.create_budget(
    budget_name="billing-budget",
    amount=10000.0,
    scope="/providers/Microsoft.Billing/billingAccounts/your-billing-account-id",
    notifications=[...]
)
```

### Retrieving Budget Information
```python
# List all budgets for a scope
budgets = azure.list_budgets(scope="/subscriptions/your-subscription-id/")

# Get a specific budget
budget_details = azure.get_budget(
    budget_name="monthly-budget",
    scope="/subscriptions/your-subscription-id/"
)
```

## 📊 Enhanced Cost Analysis Examples

### Comprehensive Cost Trends Analysis
```python
# Get detailed cost trends with insights
trends = azure.get_cost_trends(
    scope="/subscriptions/your-subscription-id/",
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily"
)

# Analyze the results
print(f"Trend direction: {trends['trend_direction']}")
print(f"Growth rate: {trends['growth_rate']:.1f}%")
print(f"Total cost: ${trends['total_cost']:.2f}")
print(f"Average daily cost: ${trends['average_daily_cost']:.2f}")

# Check for patterns
for pattern in trends['patterns']:
    print(f"Pattern detected: {pattern}")

# Review insights
for insight in trends['insights']:
    print(f"Insight: {insight}")
```

### Multi-Dimensional Cost Analysis
```python
# Get cost breakdown by multiple dimensions
analysis = azure.get_cost_analysis(
    scope="/subscriptions/your-subscription-id/",
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["ResourceType", "ResourceLocation", "ResourceGroupName"]
)

# Access the analysis results
print(f"Total cost: ${analysis['total_cost']:.2f}")
print(f"Analyzed dimensions: {analysis['dimensions']}")

# Review cost breakdown
for key, cost in analysis['cost_breakdown'].items():
    print(f"{key}: ${cost:.2f}")

# Check insights
for insight in analysis['insights']:
    print(f"Insight: {insight}")
```

### Resource-Specific Cost Tracking
```python
# Get costs for a specific virtual machine
vm_costs = azure.get_resource_costs(
    scope="/subscriptions/your-subscription-id/",
    resource_id="/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.Compute/virtualMachines/your-vm",
    granularity="Daily",
    start_date="2024-01-01",
    end_date="2024-01-31"
)
``` 