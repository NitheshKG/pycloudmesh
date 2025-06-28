# Azure FinOps API Documentation

## 1. Cost Management

### get_cost_data
Fetches raw cost and usage data from Azure Cost Management API.

**Signature:**
```python
def get_cost_data(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "Monthly",
    metrics: Optional[List[str]] = None,
    group_by: Optional[List[str]] = None,
    filter_: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date (YYYY-MM-DD). Defaults to first day of current month.
- `end_date` (str, optional): End date (YYYY-MM-DD). Defaults to today.
- `granularity` (str): "Daily", "Monthly", or "None". Defaults to "Monthly".
- `metrics` (list, optional): List of cost metrics. Defaults to standard cost metrics.
- `group_by` (list, optional): Grouping criteria.
- `filter_` (dict, optional): Filter criteria.

**Returns:**
- Cost data from Azure Cost Management.

**Example:**
```python
costs = azure.get_cost_data(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily",
    group_by=["ResourceType", "ResourceLocation"]
)
```

---

### get_cost_analysis
Provides summarized cost analysis with Azure-specific dimensions.

**Signature:**
```python
def get_cost_analysis(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    dimensions: Optional[List[str]] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date for analysis.
- `end_date` (str, optional): End date for analysis.
- `dimensions` (list, optional): List of dimensions to analyze (e.g., ["ResourceType", "ResourceLocation", "ResourceGroupName"]).

**Returns:**
- Dictionary with cost analysis data.

**Example:**
```python
analysis = azure.get_cost_analysis(
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["ResourceType", "ResourceLocation"]
)
```

---

### get_cost_trends
Analyzes cost trends over time with Azure-specific granularity.

**Signature:**
```python
def get_cost_trends(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "Daily"
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date for trend analysis.
- `end_date` (str, optional): End date for trend analysis.
- `granularity` (str, optional): Data granularity for trends. Defaults to "Daily".

**Returns:**
- Dictionary with cost trends data.

**Example:**
```python
trends = azure.get_cost_trends(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily"
)
```

### get_resource_costs
Detailed usage, parameters, and examples here.

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
- `scope` (str): Azure scope (subscription, resource group, etc.).
- `api_version` (str, optional): API version to use. Defaults to "2024-08-01".

**Returns:**
- List of budgets.

**Example:**
```python
budgets = azure.list_budgets(scope="subscriptions/your-subscription-id")
```

---

### create_budget
Creates a new Azure budget.

**Signature:**
```python
def create_budget(
    self,
    budget_name: str,
    amount: float,
    scope: str,
    time_grain: str = "Monthly",
    start_date: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `budget_name` (str): Name of the budget.
- `amount` (float): Budget amount.
- `scope` (str): Azure scope.
- `time_grain` (str, optional): Time grain for the budget. Defaults to "Monthly".
- `start_date` (str, optional): Start date for the budget.

**Returns:**
- Budget creation response.

**Example:**
```python
budget = azure.create_budget(
    budget_name="Monthly Azure Budget",
    amount=3000.0,
    scope="subscriptions/your-subscription-id"
)
```

---

### get_budget_alerts
Gets alerts for a specific budget.

**Signature:**
```python
def get_budget_alerts(
    self,
    budget_name: str
) -> Dict[str, Any]:
```

**Parameters:**
- `budget_name` (str): Name of the budget.

**Returns:**
- Budget alerts.

**Example:**
```python
alerts = azure.get_budget_alerts(budget_name="Monthly Azure Budget")
```

## 3. Optimization & Recommendations

### get_advisor_recommendations
Get Azure Advisor recommendations for cost optimization.

**Signature:**
```python
def get_advisor_recommendations(self) -> Dict[str, Any]:
```

**Returns:**
- Advisor recommendations.

**Example:**
```python
advisor_recs = azure.get_advisor_recommendations()
```

---

### get_optimization_recommendations
Get comprehensive optimization recommendations (advisor and reserved instance recommendations).

**Signature:**
```python
def get_optimization_recommendations(self) -> Dict[str, Any]:
```

**Returns:**
- Dictionary with keys: 'advisor_recommendations', 'reserved_instance_recommendations'.

**Example:**
```python
optimizations = azure.get_optimization_recommendations()
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