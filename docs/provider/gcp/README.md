# GCP FinOps API Documentation

## 1. Cost Management

### get_cost_data
Fetches raw cost and usage data from GCP Billing BigQuery export.

**Signature:**
```python
def get_cost_data(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "Monthly",
    metrics: Optional[List[str]] = None,
    group_by: Optional[List[str]] = None,
    filter_: Optional[Dict[str, Any]] = None,
    bq_project_id: Optional[str] = None,
    bq_dataset: Optional[str] = None,
    bq_table: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date (YYYY-MM-DD). Defaults to first day of current month.
- `end_date` (str, optional): End date (YYYY-MM-DD). Defaults to today.
- `granularity` (str): "Daily", "Monthly", or "None". Defaults to "Monthly".
- `metrics` (list, optional): List of cost metrics. Defaults to ["cost"].
- `group_by` (list, optional): Grouping criteria.
- `filter_` (dict, optional): Filter criteria.
- `bq_project_id` (str, optional): BigQuery project ID for billing export.
- `bq_dataset` (str, optional): BigQuery dataset name for billing export.
- `bq_table` (str, optional): BigQuery table name for billing export.

**Returns:**
- Cost data from GCP Billing (requires BigQuery export setup).

**Example:**
```python
costs = gcp.get_cost_data(
    start_date="2024-06-01",
    end_date="2024-06-30",
    granularity="Daily",
    group_by=["service.description"],
    bq_project_id="your-bq-project",
    bq_dataset="your_billing_dataset",
    bq_table="your_billing_table"
)
print(costs)
```

---

### get_cost_analysis
Provides summarized cost analysis with GCP-specific dimensions (wrapper for get_cost_data).

**Signature:**
```python
def get_cost_analysis(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    bq_project_id: Optional[str] = None,
    bq_dataset: Optional[str] = None,
    bq_table: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date for analysis.
- `end_date` (str, optional): End date for analysis.
- `bq_project_id` (str, optional): BigQuery project ID for billing export.
- `bq_dataset` (str, optional): BigQuery dataset name for billing export.
- `bq_table` (str, optional): BigQuery table name for billing export.

**Returns:**
- Dictionary with cost analysis data (grouped by ["service", "location", "project"]).

**Example:**
```python
analysis = gcp.get_cost_analysis(
    start_date="2024-06-01",
    end_date="2024-06-30",
    bq_project_id="your-bq-project",
    bq_dataset="your_billing_dataset",
    bq_table="your_billing_table"
)
print(analysis)
```

---

### get_cost_trends
Analyzes cost trends over time with GCP-specific granularity (wrapper for get_cost_data).

**Signature:**
```python
def get_cost_trends(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "Daily",
    bq_project_id: Optional[str] = None,
    bq_dataset: Optional[str] = None,
    bq_table: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date for trend analysis.
- `end_date` (str, optional): End date for trend analysis.
- `granularity` (str, optional): Data granularity for trends. Defaults to "Daily".
- `bq_project_id` (str, optional): BigQuery project ID for billing export.
- `bq_dataset` (str, optional): BigQuery dataset name for billing export.
- `bq_table` (str, optional): BigQuery table name for billing export.

**Returns:**
- Dictionary with cost trends data.

**Example:**
```python
trends = gcp.get_cost_trends(
    start_date="2024-06-01",
    end_date="2024-06-30",
    granularity="Daily",
    bq_project_id="your-bq-project",
    bq_dataset="your_billing_dataset",
    bq_table="your_billing_table"
)
print(trends)
```

---

### get_resource_costs
Fetches cost data for a specific resource (wrapper for get_cost_data with filter).

**Signature:**
```python
def get_resource_costs(
    self,
    resource_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    bq_project_id: Optional[str] = None,
    bq_dataset: Optional[str] = None,
    bq_table: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `resource_id` (str): ID of the resource to get costs for (must match your BigQuery schema, e.g., resource.name).
- `start_date` (str, optional): Start date for cost data.
- `end_date` (str, optional): End date for cost data.
- `bq_project_id` (str, optional): BigQuery project ID for billing export.
- `bq_dataset` (str, optional): BigQuery dataset name for billing export.
- `bq_table` (str, optional): BigQuery table name for billing export.

**Returns:**
- Resource cost data.

**Example:**
```python
resource_costs = gcp.get_resource_costs(
    resource_id="your-resource-id",
    start_date="2024-06-01",
    end_date="2024-06-30",
    bq_project_id="your-bq-project",
    bq_dataset="your_billing_dataset",
    bq_table="your_billing_table"
)
print(resource_costs)
```

> **Note:** The filter key for resource_id must match your BigQuery schema (e.g., use `resource.name` if that's the column name).

## 2. Budget Management

### list_budgets
Lists GCP budgets for a billing account.

**Signature:**
```python
def list_budgets(
    self,
    gcp_billing_account: str,
    gcp_max_results: int = 50
) -> Dict[str, Any]:
```

**Parameters:**
- `gcp_billing_account` (str): GCP billing account ID.
- `gcp_max_results` (int, optional): Maximum number of results to return. Defaults to 50.

**Returns:**
- List of budgets.

**Example:**
```python
budgets = gcp.list_budgets(
    gcp_billing_account="your-billing-account",
    gcp_max_results=50
)
print(budgets)
```

---

### create_budget
<!--
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
-->

> **TODO:** The `create_budget` feature for GCP is currently not working and is under development. This section will be updated once the feature is available.

---

### get_budget_alerts
Gets threshold rules and alert info for a specific budget (requires Cloud Monitoring setup for actual notifications).

**Signature:**
```python
def get_budget_alerts(
    self,
    billing_account: str,
    budget_display_name: str
) -> Dict[str, Any]:
```

**Parameters:**
- `billing_account` (str): GCP billing account ID.
- `budget_display_name` (str): Display name of the budget.

**Returns:**
- Budget threshold rules and a message about alerting (or error if not found).

**Example:**
```python
alerts = gcp.get_budget_alerts(
    billing_account="your-billing-account",
    budget_display_name="Monthly GCP Budget"
)
print(alerts)
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
- `report_type`