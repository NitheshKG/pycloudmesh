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

# Cost per resource per month
costs = azure.get_cost_data(
    "/providers/Microsoft.Billing/billingAccounts/your-billing-account-id",
    granularity="Monthly",
    group_by=["ResourceId"]
)

# Cost per service per day (trend)
costs = azure.get_cost_data(
    "/providers/Microsoft.Billing/billingAccounts/your-billing-account-id",
    granularity="Daily",
    group_by=["ServiceName"]
)

# Cost per subscription (billing account scope)
costs = azure.get_cost_data(
    "/providers/Microsoft.Billing/billingAccounts/your-billing-account-id",
    granularity="Monthly",
    group_by=["SubscriptionId"]
)

# Cost per resource group (subscription scope)
costs = azure.get_cost_data(
    "/subscriptions/your-subscription-id/",
    granularity="Monthly",
    group_by=["ResourceGroupName"]
)
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

# Access trend insights
print(f"Trend direction: {trends['trend_direction']}")
print(f"Growth rate: {trends['growth_rate']:.1f}%")
print(f"Patterns: {trends['patterns']}")
print(f"Insights: {trends['insights']}")
```

**Sample Output:**
```json
{
  "period": {"start": "2024-01-01", "end": "2024-01-31"},
  "granularity": "Daily",
  "total_periods": 31,
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
Get costs for a specific resource.

**Signature:**
```python
def get_resource_costs(
    self,
    scope: str,
    resource_id: str,
    granularity: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metrics: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `scope` (str): Azure scope (subscription, resource group, billing account, etc.)
- `resource_id` (str): ID of the resource to get costs for
- `granularity` (str): Data granularity ("Daily", "Monthly", etc.)
- `start_date` (str, optional): Start date for cost data
- `end_date` (str, optional): End date for cost data
- `metrics` (str, optional): Cost metrics to retrieve

**Returns:**
- Dict[str, Any]: Resource cost data

**Example:**
```python
resource_costs = azure.get_resource_costs(
    "/subscriptions/your-subscription-id/",
    "/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.Compute/virtualMachines/your-vm",
    granularity="Daily",
    start_date="2024-01-01",
    end_date="2024-01-31"
)
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
```

---

### get_budget
Get a specific budget by name and scope.

**Signature:**
```python
def get_budget(
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
budget = azure.get_budget(
    budget_name="Monthly Azure Budget",
    scope="/subscriptions/your-subscription-id/"
)
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
Get cost forecast for the specified period.

**Signature:**
```python
def get_cost_forecast(
    self,
    start_date: str,
    end_date: str,
    forecast_period: int = 12
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str): Start date for historical data.
- `end_date` (str): End date for historical data.
- `forecast_period` (int, optional): Number of months to forecast. Default: 12.

**Returns:**
- Cost forecast data.

**Example:**
```python
forecast = azure.get_cost_forecast(
    start_date="2024-01-01",
    end_date="2024-06-30",
    forecast_period=6
)
```

---

### get_cost_anomalies
Get cost anomalies (placeholder implementation).

**Signature:**
```python
def get_cost_anomalies(self) -> Dict[str, Any]:
```

**Returns:**
- Cost anomalies data.

**Example:**
```python
anomalies = azure.get_cost_anomalies()
```

---

### get_cost_efficiency_metrics
Get cost efficiency metrics (cost per user, per transaction, etc.).

**Signature:**
```python
def get_cost_efficiency_metrics(self) -> Dict[str, Any]:
```

**Returns:**
- Cost efficiency metrics.

**Example:**
```python
efficiency = azure.get_cost_efficiency_metrics()
```

---

### generate_cost_report
Generate a comprehensive cost report.

**Signature:**
```python
def generate_cost_report(
    self,
    report_type: str = "monthly",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `report_type` (str, optional): Type of report (monthly, quarterly, annual). Default: "monthly".
- `start_date` (str, optional): Start date for report. Defaults to first day of current month.
- `end_date` (str, optional): End date for report. Defaults to today.

**Returns:**
- Cost report data.

**Example:**
```python
report = azure.generate_cost_report(
    report_type="quarterly",
    start_date="2024-01-01",
    end_date="2024-03-31"
)
```

## 5. Governance & Compliance

### get_governance_policies
Get Azure cost management policies.

**Signature:**
```python
def get_cost_policies(self) -> Dict[str, Any]:
```

**Returns:**
- Dictionary with a list of cost management policies.

**Example:**
```python
policies = azure.get_cost_policies()
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
Get policy compliance status for Azure resources.

**Signature:**
```python
def get_policy_compliance(self) -> Dict[str, Any]:
```

**Returns:**
- Policy compliance status.

**Example:**
```python
compliance = azure.get_policy_compliance()
```

## 6. Reservation Management

### get_reservation_cost
Get Azure reservation utilization and cost data.

**Signature:**
```python
def get_reservation_cost(
    self,
    start_date: str = None,
    end_date: str = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
- `end_date` (str, optional): End date in YYYY-MM-DD format. Defaults to last day of current month.

**Returns:**
- Reservation utilization data from Azure Cost Management.

**Example:**
```python
reservation_costs = azure.get_reservation_cost(
    start_date="2024-06-01",
    end_date="2024-06-30"
)
```

---

### get_reservation_recommendation
Get Azure reservation recommendations for various services.

**Signature:**
```python
def get_reservation_recommendation(
    self,
    subscription_id: str
) -> List[Dict[str, Any]]:
```

**Parameters:**
- `subscription_id` (str): Azure subscription ID.

**Returns:**
- List of reservation recommendations.

**Example:**
```python
recommendations = azure.get_reservation_recommendation(subscription_id="your-subscription-id")
```

---

### get_reservation_order_details
Get Azure reservation order details.

**Signature:**
```python
def get_azure_reservation_order_details(self) -> Dict[str, Any]:
```

**Returns:**
- Reservation order details.

**Example:**
```python
order_details = azure.get_azure_reservation_order_details()
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