# GCP FinOps API Documentation

## 1. Cost Management

### get_cost_data
Fetches raw cost and usage data from GCP Billing API (requires BigQuery billing export).

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
- Cost data from GCP Billing (requires BigQuery export setup).

**Example:**
```python
costs = gcp.get_cost_data(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily",
    group_by=["service", "location", "project"]
)
```

---

### get_cost_analysis
Provides summarized cost analysis with GCP-specific dimensions.

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
- `dimensions` (list, optional): List of dimensions to analyze (e.g., ["service", "location", "project"]).

**Returns:**
- Dictionary with cost analysis data.

**Example:**
```python
analysis = gcp.get_cost_analysis(
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["service", "location", "project"]
)
```

---

### get_cost_trends
Analyzes cost trends over time with GCP-specific granularity.

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
trends = gcp.get_cost_trends(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily"
)
```

### get_resource_costs
Detailed usage, parameters, and examples here.

## 2. Budget Management

### list_budgets
Lists GCP budgets for a billing account.

**Signature:**
```python
def list_budgets(
    self,
    billing_account: str,
    max_results: Optional[int] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `billing_account` (str): GCP billing account ID.
- `max_results` (int, optional): Maximum number of results to return.

**Returns:**
- List of budgets.

**Example:**
```python
budgets = gcp.list_budgets(billing_account="your-billing-account")
```

---

### create_budget
Creates a new GCP budget.

**Signature:**
```python
def create_budget(
    self,
    billing_account: str,
    budget_name: str,
    amount: float,
    currency_code: str = "USD"
) -> Dict[str, Any]:
```

**Parameters:**
- `billing_account` (str): GCP billing account ID.
- `budget_name` (str): Name of the budget.
- `amount` (float): Budget amount.
- `currency_code` (str, optional): Currency code for the budget. Defaults to "USD".

**Returns:**
- Budget creation response.

**Example:**
```python
budget = gcp.create_budget(
    billing_account="your-billing-account",
    budget_name="Monthly GCP Budget",
    amount=2000.0
)
```

---

### get_budget_alerts
Gets alerts for a specific budget (requires Cloud Monitoring setup).

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
- Budget alerts (or message if not set up).

**Example:**
```python
alerts = gcp.get_budget_alerts(budget_name="Monthly GCP Budget")
```

## 3. Optimization & Recommendations

### get_machine_type_recommendations
Get machine type optimization recommendations for GCP resources.

**Signature:**
```python
def get_machine_type_recommendations(self) -> Dict[str, Any]:
```

**Returns:**
- Machine type recommendations.

**Example:**
```python
machine_recs = gcp.get_machine_type_recommendations()
```

---

### get_idle_resource_recommendations
Get idle resource recommendations for GCP resources.

**Signature:**
```python
def get_idle_resource_recommendations(self) -> Dict[str, Any]:
```

**Returns:**
- Idle resource recommendations.

**Example:**
```python
idle_recs = gcp.get_idle_resource_recommendations()
```

---

### get_optimization_recommendations
Get comprehensive optimization recommendations (machine type and idle resource recommendations).

**Signature:**
```python
def get_optimization_recommendations(self) -> Dict[str, Any]:
```

**Returns:**
- Dictionary with keys: 'machine_type_recommendations', 'idle_resource_recommendations'.

**Example:**
```python
optimizations = gcp.get_optimization_recommendations()
```

## 4. Advanced Analytics

### get_cost_forecast
Get cost forecast for the specified period (requires BigQuery ML setup).

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
- Cost forecast data (requires BigQuery ML setup).

**Example:**
```python
forecast = gcp.get_cost_forecast(
    start_date="2024-01-01",
    end_date="2024-06-30",
    forecast_period=6
)
```

---

### get_cost_anomalies
Get cost anomalies (requires Cloud Monitoring setup).

**Signature:**
```python
def get_cost_anomalies(self) -> Dict[str, Any]:
```

**Returns:**
- Cost anomalies data.

**Example:**
```python
anomalies = gcp.get_cost_anomalies()
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
efficiency = gcp.get_cost_efficiency_metrics()
```

---

### generate_cost_report
Generate a comprehensive cost report (requires BigQuery billing export setup).

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
- Cost report data (requires BigQuery billing export setup).

**Example:**
```python
report = gcp.generate_cost_report(
    report_type="quarterly",
    start_date="2024-01-01",
    end_date="2024-03-31"
)
```

## 5. Governance & Compliance

### get_governance_policies
Get GCP cost management policies (requires Organization Policy API setup).

**Signature:**
```python
def get_cost_policies(self) -> Dict[str, Any]:
```

**Returns:**
- Dictionary with a list of cost management policies (or message if not set up).

**Example:**
```python
policies = gcp.get_cost_policies()
```

---

### get_cost_allocation_tags
Get cost allocation labels for GCP resources (requires Resource Manager API setup).

**Signature:**
```python
def get_cost_allocation_tags(self) -> Dict[str, Any]:
```

**Returns:**
- Cost allocation labels for GCP resources (or message if not set up).

**Example:**
```python
tags = gcp.get_cost_allocation_tags()
```

---

### get_policy_compliance
Get policy compliance status for GCP resources (requires Policy API setup).

**Signature:**
```python
def get_policy_compliance(self) -> Dict[str, Any]:
```

**Returns:**
- Policy compliance status (or message if not set up).

**Example:**
```python
compliance = gcp.get_policy_compliance()
```

## 6. Reservation Management

### get_reservation_cost
Get GCP reservation utilization and cost data (requires billing export setup).

**Signature:**
```python
def get_reservation_cost(
    start_date: str = None,
    end_date: str = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
- `end_date` (str, optional): End date in YYYY-MM-DD format. Defaults to last day of current month.

**Returns:**
- Reservation utilization data from GCP Billing (requires billing export setup).

**Example:**
```python
reservation_costs = gcp.get_reservation_cost(
    start_date="2024-06-01",
    end_date="2024-06-30"
)
```

---

### get_reservation_recommendation
Get GCP reservation recommendations using the Recommender API.

**Signature:**
```python
def get_reservation_recommendation(self) -> List[Dict[str, Any]]:
```

**Returns:**
- List of reservation recommendations.

**Example:**
```python
recommendations = gcp.get_reservation_recommendation()
``` 