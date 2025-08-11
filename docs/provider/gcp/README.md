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

**Sample Response:**
```json
{
    "period": {"start": "2024-06-01", "end": "2024-06-30"},
    "granularity": "Daily",
    "metrics": ["cost"],
    "group_by": ["service.description"],
    "cost_data": [
        {
            "description": "Compute Engine",
            "total_cost": 450.25
        },
        {
            "description": "Cloud Storage",
            "total_cost": 125.50
        },
        {
            "description": "BigQuery",
            "total_cost": 75.25
        },
        {
            "description": "Cloud Logging",
            "total_cost": 25.00
        }
    ]
}
```

---

### get_cost_analysis
Provides comprehensive cost analysis with insights, breakdowns, and actionable recommendations.

**Signature:**
```python
def get_cost_analysis(
    self,
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str): BigQuery project ID for billing export (required).
- `bq_dataset` (str): BigQuery dataset name for billing export (required).
- `bq_table` (str): BigQuery table name for billing export (required).
- `start_date` (str, optional): Start date for analysis.
- `end_date` (str, optional): End date for analysis.

**Returns:**
- Dictionary with comprehensive cost analysis including:
  - `period`: Time period covered
  - `dimensions`: Analysis dimensions used (service, location, project)
  - `total_cost`: Total cost calculation
  - `cost_breakdown`: Service-wise cost breakdown
  - `top_services`: Top 5 services by cost
  - `cost_trends`: Cost trends over time
  - `insights`: Percentage analysis and recommendations

**Example:**
```python
analysis = gcp.get_cost_analysis(
    bq_project_id="your-bq-project",
    bq_dataset="your_billing_dataset",
    bq_table="your_billing_table",
    start_date="2024-06-01",
    end_date="2024-06-30"
)
print(analysis)
```

**Sample Response:**
```json
{
   "period": {"start": "2024-06-01", "end": "2024-06-30"},
   "dimensions": ["service", "location", "project"],
   "total_cost": 450.25,
   "cost_breakdown": {
      "Compute Engine": 200.50,
      "Cloud Storage": 150.75,
      "BigQuery": 99.00
   },
   "top_services": [
      {"service": "Compute Engine", "cost": 200.50, "percentage": 44.6},
      {"service": "Cloud Storage", "cost": 150.75, "percentage": 33.5}
   ],
   "cost_trends": [
      {"date": "2024-06-01", "cost": 15.25},
      {"date": "2024-06-02", "cost": 14.75}
   ],
   "insights": [
      "Compute Engine represents 44.6% of total costs",
      "Consider rightsizing recommendations for cost optimization"
   ]
}
```

---

### get_cost_trends
Analyzes cost trends over time with daily granularity and comprehensive trend analysis.

**Signature:**
```python
def get_cost_trends(
    self,
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str): BigQuery project ID for billing export.
- `bq_dataset` (str): BigQuery dataset name for billing export.
- `bq_table` (str): BigQuery table name for billing export.
- `start_date` (str, optional, in kwargs): Start date for trend analysis.
- `end_date` (str, optional, in kwargs): End date for trend analysis.

**Returns:**
- Dictionary with comprehensive cost trends data including:
  - `period`: Time period covered
  - `granularity`: Data granularity (Daily)
  - `total_periods`: Number of periods analyzed
  - `total_cost`: Total cost for the period
  - `average_daily_cost`: Average daily cost
  - `trend_direction`: Cost trend direction (increasing/decreasing/stable)
  - `growth_rate`: Percentage growth rate
  - `patterns`: Identified cost patterns
  - `insights`: Trend insights and recommendations
  - `peak_periods`: Periods with highest costs
  - `cost_periods`: Daily cost breakdown

**Example:**
```python
trends = gcp.get_cost_trends(
    bq_project_id="your-bq-project",
    bq_dataset="your_billing_dataset",
    bq_table="your_billing_table",
    start_date="2024-06-01",
    end_date="2024-06-30"
)
print(trends)
```

**Sample Response:**
```json
{
   "period": {"start": "2024-06-01", "end": "2024-06-30"},
   "granularity": "Daily",
   "total_periods": 30,
   "total_cost": 450.25,
   "average_daily_cost": 15.01,
   "trend_direction": "increasing",
   "growth_rate": 12.5,
   "patterns": ["weekend_spikes", "monthly_cycle"],
   "insights": ["Costs are trending upward", "Consider optimization"],
   "peak_periods": ["2024-06-15", "2024-06-22"],
   "cost_periods": [
      {"date": "2024-06-01", "cost": 12.50},
      {"date": "2024-06-02", "cost": 14.75}
   ]
}
```

---

### get_resource_costs
Provides comprehensive resource cost analysis with utilization insights and optimization recommendations.

**Signature:**
```python
def get_resource_costs(
    self,
    resource_name: str,
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `resource_name` (str): Name/ID of the resource to get costs for (must match your BigQuery schema, e.g., resource.name).
- `bq_project_id` (str): BigQuery project ID for billing export.
- `bq_dataset` (str): BigQuery dataset name for billing export.
- `bq_table` (str): BigQuery table name for billing export.
- `start_date` (str, optional, in kwargs): Start date for cost data.
- `end_date` (str, optional, in kwargs): End date for cost data.

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
resource_costs = gcp.get_resource_costs(
    resource_name="your-resource-name",
    bq_project_id="your-bq-project",
    bq_dataset="your_billing_dataset",
    bq_table="your_billing_table",
    start_date="2024-06-01",
    end_date="2024-06-30"
)
print(resource_costs)
```

**Sample Response:**
```json
{
   "resource_id": "your-resource-name",
   "resource_type": "compute_instance",
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
      "Consider committed use discounts for cost savings",
      "Review idle periods for optimization opportunities"
   ]
}
```

> **Note:** The filter key for resource_name must match your BigQuery schema (e.g., use `resource.name` if that's the column name).

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

**Sample Response:**
```json
{
    "budgets": [
        {
            "name": "billingAccounts/your-billing-account/budgets/your-budget-id",
            "display_name": "Monthly GCP Budget",
            "budget_filter": {
                "projects": ["projects/your-project"],
                "credit_types_treatment": "INCLUDE_ALL_CREDITS"
            },
            "amount": {
                "specified_amount": {
                    "currency_code": "USD",
                    "units": "2000",
                    "nanos": 0
                }
            },
            "threshold_rules": [
                {
                    "threshold_percent": 0.5,
                    "spend_basis": "CURRENT_SPEND"
                },
                {
                    "threshold_percent": 0.8,
                    "spend_basis": "CURRENT_SPEND"
                },
                {
                    "threshold_percent": 1.0,
                    "spend_basis": "CURRENT_SPEND"
                }
            ]
        },
        {
            "name": "billingAccounts/your-billing-account/budgets/your-quarterly-budget-id",
            "display_name": "Quarterly GCP Budget",
            "budget_filter": {
                "projects": ["projects/your-project"],
                "credit_types_treatment": "INCLUDE_ALL_CREDITS"
            },
            "amount": {
                "specified_amount": {
                    "currency_code": "USD",
                    "units": "5000",
                    "nanos": 0
                }
            },
            "threshold_rules": [
                {
                    "threshold_percent": 0.7,
                    "spend_basis": "CURRENT_SPEND"
                },
                {
                    "threshold_percent": 1.0,
                    "spend_basis": "CURRENT_SPEND"
                }
            ]
        }
    ]
}
```

**Error Response (Not Found):**
```json
{
    "error": "Failed to list budgets: 404 Client Error: Not Found for url: https://billingbudgets.googleapis.com/v1/billingAccounts/invalid-billing-account/budgets"
}
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
    currency_code: str = "USD",
    notifications: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `billing_account` (str): GCP billing account ID.
- `budget_name` (str): Name of the budget.
- `amount` (float): Budget amount.
- `currency_code` (str, optional): Currency code for the budget. Defaults to "USD".
- `notifications` (List[Dict[str, Any]], optional): List of notification configurations.

**Returns:**
- Budget creation response.

**Example:**
```python
budget = gcp.create_budget(
    billing_account="your-billing-account",
    budget_name="Monthly GCP Budget",
    amount=2000.0,
    notifications=[
        {
            "displayName": "Budget Alert",
            "pubsubTopic": "projects/your-project/topics/budget-alerts",
            "schemaVersion": "1.0",
            "monitoringNotificationChannels": ["projects/your-project/notificationChannels/123456789"]
        }
    ]
)
print(budget)
```

**Sample Response:**
```json
{
    "name": "billingAccounts/your-billing-account/budgets/your-budget-id",
    "displayName": "Monthly GCP Budget",
    "budgetFilter": {
        "projects": ["projects/your-project"]
    },
    "amount": {
        "specifiedAmount": {
            "currencyCode": "USD",
            "units": "2000"
        }
    },
    "thresholdRules": [
        {
            "thresholdPercent": 0.5,
            "spendBasis": "CURRENT_SPEND"
        },
        {
            "thresholdPercent": 0.8,
            "spendBasis": "CURRENT_SPEND"
        },
        {
            "thresholdPercent": 1.0,
            "spendBasis": "CURRENT_SPEND"
        }
    ],
    "notificationsRule": {
        "pubsubTopic": "projects/your-project/topics/budget-alerts",
        "schemaVersion": "1.0",
        "monitoringNotificationChannels": ["projects/your-project/notificationChannels/123456789"]
    },
    "etag": "\"abc123\""
}
```

**Error Response (Not Implemented):**
```json
{
    "error": "The create_budget feature for GCP is currently not working and is under development."
}
```

> **Note:** The `create_budget` feature for GCP is currently under development. This section shows the expected interface and response format for when the feature becomes available.

---

### get_budget_notifications

Retrieve all notifications configured for a specific GCP budget.

**Parameters:**
- `billing_account` (str): GCP billing account ID (required)
- `budget_display_name` (str): Display name of the budget (required)

**Returns:**
A dictionary with budget notification information, or an error message.

**Example:**
```python
gcp = gcp_client("your_project_id", "/path/to/credentials.json")
notifications = gcp.get_budget_notifications(
    billing_account="012345-678901-ABCDEF",
    budget_display_name="monthly-budget"
)
print(notifications)
```

**Sample Response:**
```json
{
    "budget_name": "billingAccounts/012345-678901-ABCDEF/budgets/your-budget-id",
    "display_name": "monthly-budget",
    "threshold_rules": [
        {
            "threshold_percent": 0.5,
            "spend_basis": "CURRENT_SPEND"
        },
        {
            "threshold_percent": 0.8,
            "spend_basis": "CURRENT_SPEND"
        },
        {
            "threshold_percent": 1.0,
            "spend_basis": "CURRENT_SPEND"
        }
    ],
    "message": "GCP budget alerts are delivered via Cloud Monitoring and/or Pub/Sub. To receive notifications, ensure you have set up notification channels in the budget configuration."
}
```

**Error Response (Not Found):**
```json
{
    "error": "Budget with display name 'nonexistent-budget' not found."
}
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
Get unified cost forecast for the specified period with AI/ML enhanced predictions using BigQuery ML (ARIMA_PLUS model) and statistical analysis.

**Signature:**
```python
def get_cost_forecast(
    self,
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    forecast_period: int = 30,
    use_ai_model: bool = True
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str): BigQuery project ID for billing export.
- `bq_dataset` (str): BigQuery dataset name for billing export.
- `bq_table` (str): BigQuery table name for billing export.
- `start_date` (str, optional): Start date for historical data (YYYY-MM-DD). Defaults to 90 days ago.
- `end_date` (str, optional): End date for historical data (YYYY-MM-DD). Defaults to today.
- `forecast_period` (int, optional): Number of days to forecast. Default: 12.
- `use_ai_model` (bool, optional): Whether to use BigQuery ML ARIMA_PLUS model. Default: True.

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
forecast = gcp.get_cost_forecast(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX",
    start_date="2025-05-01",
    end_date="2025-07-31",
    forecast_period=30,
    use_ai_model=True
)
print(forecast)
```

**Sample Response:**
```json
{
    "forecast_period": 30,
    "start_date": "2025-05-01",
    "end_date": "2025-07-31",
    "total_historical_cost": 417.93,
    "total_forecast_cost": 107.04,
    "average_daily_cost": 4.54,
    "forecast_results": [
      {
            "date": "2025-07-30",
            "forecast_value": 3.060538723422985,
            "lower_bound": -0.31526241770335384,
            "upper_bound": 6.436339864549323,
            "confidence_level": 0.9
      },
      {
            "date": "2025-07-31",
            "forecast_value": 4.118712071445168,
            "lower_bound": -0.6553916862102707,
            "upper_bound": 8.892815829100607,
            "confidence_level": 0.9
        }
    ],
    "ai_model_used": true,
    "model_accuracy": {
        "mape": 0.0,
        "rmse": 0.0,
        "mean_absolute_error": 0.0
    },
    "insights": [
        "Historical average daily cost: 4.54",
        "Recent 7-day trend: 33.3% change",
        "Forecasted total cost for 30 days: 107.04"
    ],
    "granularity": "Daily",
    "message": "Unified cost forecast generated for 30 days using BigQuery ML"
}
```

---

### get_cost_anomalies
Detect cost anomalies using BigQuery ML's ML.DETECT_ANOMALIES on daily cost data. Flags days as anomalies based on the ARIMA_PLUS model's prediction intervals.

**Signature:**
```python
def get_cost_anomalies(
    self,
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    anomaly_prob_threshold: float = 0.95
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str): BigQuery project ID for billing export.
- `bq_dataset` (str): BigQuery dataset name for billing export.
- `bq_table` (str): BigQuery table name for billing export.
- `start_date` (str, optional): Start date for analysis (YYYY-MM-DD). Defaults to 60 days ago.
- `end_date` (str, optional): End date for analysis (YYYY-MM-DD). Defaults to today.
- `anomaly_prob_threshold` (float, optional): Probability threshold for anomaly detection. Default: 0.95.

**Returns:**
- List of cost anomalies with date, cost, and anomaly probability.

**Example:**
```python
anomalies = gcp.get_cost_anomalies(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX"
)
print(anomalies)
```

**Sample Response:**
```json
{
   "anomalies": [
      {
         "date": "2025-07-01",
         "cost": 25.50,
         "anomaly_probability": 0.98
      },
      {
         "date": "2025-07-03",
         "cost": 30.75,
         "anomaly_probability": 0.99
      }
   ],
   "period": {
      "start": "2025-05-01",
      "end": "2025-07-04"
   },
   "anomaly_prob_threshold": 0.95,
   "message": "Anomalies detected using BigQuery ML ARIMA_PLUS model."
}
```

---

### get_cost_efficiency_metrics
Calculate optimal cost efficiency metrics with adaptive ML usage. Automatically chooses the best approach based on data characteristics.

**Signature:**
```python
def get_cost_efficiency_metrics(
    self,
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    use_ml: bool = True
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str): BigQuery project ID for billing export.
- `bq_dataset` (str): BigQuery dataset name for billing export.
- `bq_table` (str): BigQuery table name for billing export.
- `start_date` (str, optional): Start date for analysis (YYYY-MM-DD). Defaults to 30 days ago.
- `end_date` (str, optional): End date for analysis (YYYY-MM-DD). Defaults to today.
- `use_ml` (bool, optional): Whether to attempt ML-based analysis. Default: True.

**Returns:**
- Cost efficiency metrics with method transparency.

**Example:**
```python
gcp = GCPFinOpsAnalytics(project_id="your_project", credentials_path="path/to/credentials.json")
efficiency_metrics = gcp.get_cost_efficiency_metrics(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX",
    start_date="2025-06-29",
    end_date="2025-07-29"
)
```

**Sample Response:**
```json
{
   "efficiency_metrics": {
      "total_days_analyzed": 30,
      "total_cost_period": 417.59,
      "avg_daily_cost": 0.58,
      "min_daily_cost": 0.04,
      "max_daily_cost": 2.19,
      "cost_stddev": 0.19,
      "cost_variance_ratio": 0.328,
      "cost_efficiency_score": 0.902,
      "waste_percentage": 0.0,
      "waste_days": 0,
      "method_used": "Manual (ML failed)",
      "ml_enabled": true
   },
   "period": {
      "start": "2025-06-29",
      "end": "2025-07-29"
   },
   "message": "Efficiency metrics calculated."
}
```

---

## Cost Reports

### `generate_cost_report`

Generate comprehensive cost report using BigQuery billing export data with unified format across all cloud providers.

**Signature:**
```python
def generate_cost_report(
    self,
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    report_type: str = "monthly",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `bq_project_id` (str, required): BigQuery project ID for billing export
- `bq_dataset` (str, required): BigQuery dataset name for billing export
- `bq_table` (str, required): BigQuery table name for billing export
- `report_type` (str, optional): Type of report (monthly, quarterly, annual, custom). Default: "monthly"
- `start_date` (str, optional): Start date in YYYY-MM-DD format
- `end_date` (str, optional): End date in YYYY-MM-DD format

**Returns:**
- `Dict[str, Any]`: Unified cost report format with processed data

**Example:**
```python
gcp = GCPFinOpsAnalytics(project_id="your_project", credentials_path="path/to/credentials.json")
report = gcp.generate_cost_report(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX",
    report_type="monthly",
    start_date="2025-07-01",
    end_date="2025-07-31"
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
    "generated_at": "2025-07-31T02:10:26.005790",
   "summary": {
        "total_cost": 416.83,
        "total_days": 30,
      "avg_daily_cost": 0.01,
      "min_daily_cost": -0.47,
        "max_daily_cost": 0.54,
      "unique_services": 6,
      "unique_projects": 1,
      "unique_locations": 3
   },
   "breakdowns": {
      "by_service": [
         {
                "service": "Networking",
                "total_cost": 161.74,
                "avg_daily_cost": 0.08
         },
         {
            "service": "VM Manager",
                "total_cost": 160.97,
            "avg_daily_cost": 0.26
            },
            {
                "service": "Compute Engine",
                "total_cost": 94.12,
                "avg_daily_cost": 0.0
         }
      ],
      "by_project": [
         {
            "project": "your-gcp-project",
                "total_cost": 416.83,
            "avg_daily_cost": 0.01
         }
      ],
      "by_location": [
         {
            "location": "us-central1",
                "total_cost": 242.46,
            "avg_daily_cost": 0.01
            },
            {
                "location": "us-central1-c",
                "total_cost": 160.97,
                "avg_daily_cost": 0.26
         }
      ]
   },
   "trends": {
      "daily_costs": [
         {
            "date": "2025-07-01",
                "daily_cost": 3.0135890000000005
         },
         {
            "date": "2025-07-02",
                "daily_cost": 2.9882110000000006
         }
      ]
   },
   "cost_drivers": [
      {
         "sku": {
            "id": "CF4E-A0C7-E3BF",
            "description": "E2 Instance Core running in Americas"
         },
         "service": {
            "id": "6F81-5844-456A",
            "description": "Compute Engine"
         },
            "total_cost": 291.2
        },
        {
            "sku": {
                "id": "210B-55F7-AA37",
                "description": "VM Manager Usage (Cloud Ops)"
            },
            "service": {
                "id": "5E18-9A83-2867",
                "description": "VM Manager"
            },
            "total_cost": 160.97
      }
   ],
   "efficiency_metrics": {
        "cost_efficiency_score": 0.723,
        "cost_variance_ratio": 0.277,
        "cost_stddev": 3.85
   },
   "message": "Comprehensive cost report generated for monthly period."
}
```

---

## 5. Governance & Compliance

### get_governance_policies
Get GCP governance policies and compliance status for cost management.

**Signature:**
```python
def get_governance_policies(
    self,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str, optional): BigQuery project ID for billing export.
- `bq_dataset` (str, optional): BigQuery dataset name for billing export.
- `bq_table` (str, optional): BigQuery table name for billing export.
- `gcp_billing_account` (str, optional): GCP billing account ID for budget information.

**Returns:**
- `Dict[str, Any]`: Dictionary with unified structure:
    - `cost_allocation_labels`: Cost allocation labels (unified with AWS/Azure)
    - `policy_compliance`: Compliance status for cost policies (unified with AWS/Azure)
    - `cost_policies`: Cost-related governance policies

**Example:**
```python
governance_data = gcp.get_governance_policies(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX",
    gcp_billing_account="your-billing-account"
)
```

**Sample Response:**
```json
{
   "cost_allocation_labels": {
      "project_labels": {
         "pycloudmesh_project_label": "pycloudmesh_project_value"
      },
      "resource_labels": {
         "unique_labels": [
            {
               "key": "goog-resource-type",
               "value": "gce_instance"
            },
            {
               "key": "goog-agent-metric-class",
               "value": "cpu"
                },
                {
                    "key": "goog-agent-metric-class",
                    "value": "disk"
                },
                {
                    "key": "goog-agent-metric-class",
                    "value": "interface"
                },
                {
                    "key": "goog-agent-metric-class",
                    "value": "memory"
                },
                {
                    "key": "goog-agent-metric-class",
                    "value": "network"
                },
                {
                    "key": "goog-agent-metric-class",
                    "value": "processes"
                },
                {
                    "key": "goog-agent-metric-class",
                    "value": "swap"
                },
                {
                    "key": "goog-metric-domain",
                    "value": "agent.googleapis.com"
                },
                {
                    "key": "goog-ops-agent-policy",
                    "value": "v2-x86-template-1-4-0"
                },
                {
                    "key": "goog-resource-type",
                    "value": "bigquery_dataset"
                },
                {
                    "key": "goog-resource-type",
                    "value": "bigquery_dts_config"
                },
                {
                    "key": "goog-resource-type",
                    "value": "bigquery_project"
                },
                {
                    "key": "goog-resource-type",
                    "value": "bigquery_resource"
                },
                {
                    "key": "goog-resource-type",
                    "value": "gce_instance"
                },
                {
                    "key": "goog-resource-type",
                    "value": "networking.googleapis.com/Location"
                },
                {
                    "key": "goog-resource-type",
                    "value": "project"
            }
         ],
         "total_unique_labels": 17,
         "message": "Unique labels retrieved from BigQuery billing data (17 unique key-value pairs)"
      },
      "total_labels": 1,
      "message": "Cost allocation labels retrieved from GCP Resource Manager API"
   },
   "policy_compliance": {
      "compliance_status": {
         "project_compliance": {
                "total_resources": 1,
            "compliance_checked": true,
            "status": "compliant",
                "resource_types_found": [
                    "compute.googleapis.com/Instance"
                ]
            },
            "resource_compliance": {},
            "cost_policy_compliance": {
                "budget_alerts_enabled": true,
                "cost_allocation_enabled": true,
                "resource_quota_enforced": false,
                "cost_monitoring_enabled": true
         },
         "organization_policy_compliance": {
            "policies_checked": 4,
                "policies_enforced": 0,
            "policy_details": {
               "compute.requireOsLogin": {
                        "enforced": false,
                        "policy_exists": false
                    },
                    "compute.requireShieldedVm": {
                        "enforced": false,
                        "policy_exists": false
               },
               "storage.uniformBucketLevelAccess": {
                        "enforced": false,
                        "policy_exists": false
                    },
                    "compute.vmExternalIpAccess": {
                  "enforced": false,
                  "policy_exists": false
               }
            },
            "status": "checked"
         },
            "overall_status": "partial"
      },
      "message": "Policy compliance status retrieved from GCP Asset, Organization Policy, and Budget APIs"
   },
   "cost_policies": {
      "policies": {
         "budget_policies": {
            "budgets_configured": true,
                "total_budgets": 0,
                "message": "Budget client accessible but no billing account specified. Pass 'gcp_billing_account' parameter to get budget details.",
                "recommendation": "Provide gcp_billing_account parameter to retrieve actual budget information"
            },
            "quota_policies": {
                "compute.quota.maxCpusPerProject": {
                    "enforced": false,
                    "policy_exists": false
                },
                "compute.quota.maxInstancesPerProject": {
                    "enforced": false,
                    "policy_exists": false
                },
                "storage.quota.maxBucketsPerProject": {
                    "enforced": false,
                    "policy_exists": false
                }
            },
            "cost_control_policies": {
                "auto_shutdown_enabled": false,
                "idle_resource_cleanup": false,
                "cost_alerting": true,
                "resource_tagging_required": false
            },
            "organization_policies": {
                "cost_center_tagging": false,
                "budget_approval_required": false,
                "resource_quota_enforcement": false,
                "cost_transparency": true
            }
        },
        "total_policies": 4,
        "message": "Cost management policies retrieved from GCP Organization Policy API"
    }
}
```
                  "name": "pycloudmesh_budget",
                  "amount": {
                     "currency_code": "INR",
                     "units": 100
                  },
                  "threshold_rules": [
                     {
                        "threshold_percent": 1.0,
                        "spend_basis": "CURRENT_SPEND"
                     }
                  ]
               }
            ],
            "currency": "INR",
            "message": "Found 1 budget(s) for billing account your-billing-account"
         },
         "quota_policies": {
            "compute.quota.maxCpusPerProject": {
               "enforced": false,
               "policy_exists": false
            },
            "compute.quota.maxInstancesPerProject": {
               "enforced": false,
               "policy_exists": false
            },
            "storage.quota.maxBucketsPerProject": {
               "enforced": false,
               "policy_exists": false
            }
         },
         "cost_control_policies": {
            "auto_shutdown_enabled": false,
            "idle_resource_cleanup": false,
            "cost_alerting": true,
            "resource_tagging_required": false
         },
         "organization_policies": {
            "cost_center_tagging": false,
            "budget_approval_required": false,
            "resource_quota_enforcement": false,
            "cost_transparency": true
         }
      },
      "total_policies": 4,
      "message": "Cost management policies retrieved from GCP Organization Policy API"
   }
}
```

### get_cost_allocation_tags
Get cost allocation labels from GCP resources and billing data.

**Signature:**
```python
def get_cost_allocation_tags(
    self,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str, optional): BigQuery project ID for billing export.
- `bq_dataset` (str, optional): BigQuery dataset name for billing export.
- `bq_table` (str, optional): BigQuery table name for billing export.

**Returns:**
- Cost allocation labels with usage statistics.

**Example:**
```python
labels = gcp.get_cost_allocation_tags(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX"
)
print(labels)
```

### get_policy_compliance
Get policy compliance status for GCP resources and cost policies.

**Signature:**
```python
def get_policy_compliance(
    self,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str, optional): BigQuery project ID for billing export.

**Returns:**
- Policy compliance status with detailed findings.

**Example:**
```python
compliance = gcp.get_policy_compliance(
    bq_project_id="your-gcp-project"
)
print(compliance)
```

### get_cost_policies
Get cost management policies and budget configurations.

**Signature:**
```python
def get_cost_policies(
    self,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `gcp_billing_account` (str, optional): GCP billing account ID for budget information.

**Returns:**
- Cost policies with budget and quota information.

**Example:**
```python
policies = gcp.get_cost_policies(
    gcp_billing_account="your-billing-account"
)
print(policies)
```

---

## 6. Reservation Management *(Beta)*

> **Note:** GCP Reservation Management features are currently in Beta. These features provide comprehensive reservation cost analysis and optimization recommendations using BigQuery billing export and GCP Recommender API.

### get_reservation_cost
Get GCP reservation utilization and cost data using BigQuery billing export.

**Signature:**
```python
def get_reservation_cost(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    bq_project_id: Optional[str] = None,
    bq_dataset: Optional[str] = None,
    bq_table: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date in YYYY-MM-DD format. Defaults to first day of current month.
- `end_date` (str, optional): End date in YYYY-MM-DD format. Defaults to last day of current month.
- `bq_project_id` (str, optional): BigQuery project ID for billing export. Defaults to the client's project ID.
- `bq_dataset` (str, optional): BigQuery dataset name for billing export. Defaults to "billing_dataset".
- `bq_table` (str, optional): BigQuery table name for billing export. Defaults to "gcp_billing_export_resource_v1_XXXXXX".

**Returns:**
- Comprehensive reservation utilization data from GCP Billing BigQuery export.

**Example:**
```python
reservation_data = gcp.get_reservation_cost(
    start_date="2024-06-01",
    end_date="2024-06-30",
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_BILLING_ACCOUNT"
)
print(reservation_data)
```

**Sample Response:**
```json
{
   "period": {
      "start": "2024-06-01",
      "end": "2024-06-30"
   },
   "total_reservation_cost": 1250.75,
   "reservation_utilization": [
      {
         "date": "2024-06-15",
         "service": "Compute Engine",
         "sku_description": "E2 Instance Core running with committed use discount",
         "cost": 45.25,
         "usage_amount": 86400.0,
         "usage_unit": "seconds",
         "project_count": 2
      }
   ],
   "insights": {
      "days_with_reservations": 30,
      "projects_with_reservations": 3,
      "avg_daily_reservation_cost": 41.69,
      "total_reservations_found": 15
   },
   "message": "Reservation cost data retrieved from BigQuery billing export for 15 reservation records"
}
```

**Features:**
- **BigQuery Integration**: Uses actual billing export data for accurate cost analysis
- **Comprehensive Filtering**: Identifies committed use discounts, reservations, and sustained use discounts
- **Detailed Insights**: Provides utilization metrics, project distribution, and cost trends
- **Error Handling**: Graceful handling of missing data or unavailable BigQuery exports

---

### get_reservation_recommendation
Get comprehensive GCP reservation optimization recommendations using the Recommender API.

**Signature:**
```python
def get_reservation_recommendation(
    self
) -> Dict[str, Any]:
```

**Returns:**
- Comprehensive reservation recommendations with priority sorting and cost impact analysis.

**Example:**
```python
recommendations = gcp.get_reservation_recommendation()
print(recommendations)
```

**Sample Response:**
```json
{
   "recommendations": [
      {
         "type": "committed_use_discount",
         "name": "projects/your-project/locations/global/recommenders/google.compute.commitment.UsageCommitmentRecommender/recommendations/123456",
         "description": "Purchase committed use discount for e2-standard-2 instances",
         "primary_impact": {
            "category": "COST",
            "cost_projection": {
               "cost": "500",
               "currency_code": "USD"
            }
         },
         "state_info": {
            "state": "ACTIVE"
         },
         "priority": "high"
      },
      {
         "type": "machine_type_optimization",
         "name": "projects/your-project/locations/global/recommenders/google.compute.instance.MachineTypeRecommender/recommendations/789012",
         "description": "Change machine type from n1-standard-2 to e2-standard-2",
         "primary_impact": {
            "category": "COST",
            "cost_projection": {
               "cost": "200",
               "currency_code": "USD"
            }
         },
         "state_info": {
            "state": "ACTIVE"
         },
         "priority": "medium"
      }
   ],
   "summary": {
      "total_recommendations": 8,
      "total_potential_savings": 1200.50,
      "recommendation_types": ["committed_use_discount", "machine_type_optimization", "sustained_use_discount"],
      "high_priority_count": 3,
      "message": "Found 8 reservation optimization recommendations"
   }
}
```

**Features:**
- **Multiple Recommender Types**: 
  - Machine Type Optimizer
  - Committed Use Discount Recommender
  - Sustained Use Discount Recommender
- **Priority Sorting**: Recommendations sorted by priority and potential savings
- **Comprehensive Summary**: Total recommendations, potential savings, and recommendation types
- **Error Resilience**: Graceful handling of unavailable recommenders

---

### GCP-Specific Reservation Methods

#### get_committed_use_discount_recommendations
Get dedicated committed use discount recommendations.

**Example:**
```python
cud_recommendations = gcp.get_committed_use_discount_recommendations()
print(cud_recommendations)
```

#### get_sustained_use_discount_recommendations
Get dedicated sustained use discount recommendations.

**Example:**
```python
sud_recommendations = gcp.get_sustained_use_discount_recommendations()
print(sud_recommendations)
```

---

### Prerequisites for GCP Reservation Management

1. **BigQuery Billing Export Setup**:
   - Enable billing export to BigQuery
   - Ensure proper IAM permissions for BigQuery access
   - Verify billing export table contains reservation/discount data

2. **Required IAM Permissions**:
   - `roles/bigquery.user` - Access BigQuery billing export
   - `roles/recommender.viewer` - View optimization recommendations
   - `roles/billing.viewer` - View billing information

3. **API Enablement**:
   - BigQuery API
   - Recommender API
   - Cloud Billing API

### Error Handling

The reservation management methods include comprehensive error handling:

- **Missing BigQuery Data**: Returns appropriate message when no reservation data is found
- **API Unavailable**: Graceful fallback when recommenders are not available
- **Permission Issues**: Clear error messages with setup recommendations
- **Null Data Handling**: Safe processing of missing or null values in BigQuery results

---

## Advanced Usage Examples

### Comprehensive Governance Check
```python
from pycloudmesh import gcp_client

# Initialize GCP client
gcp = gcp_client("your-project-id", "/path/to/credentials.json")

# Get comprehensive governance information
governance_data = gcp.get_governance_policies(
    bq_project_id="your-project-id",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_BILLING_ACCOUNT",
    gcp_billing_account="your-billing-account"
)

# Access different governance components
cost_allocation = governance_data["cost_allocation_labels"]
policy_compliance = governance_data["policy_compliance"]
cost_policies = governance_data["cost_policies"]

# Check compliance status
overall_status = policy_compliance["compliance_status"]["overall_status"]
print(f"Overall compliance status: {overall_status}")

# Get budget information
budget_info = cost_policies["policies"]["budget_policies"]
if budget_info["budgets_configured"]:
    print(f"Found {budget_info['total_budgets']} budget(s)")
    for budget in budget_info["budget_details"]:
        print(f"- {budget['name']}: {budget['amount']['units']} {budget['amount']['currency_code']}")

# Get resource labels for cost allocation
resource_labels = cost_allocation["resource_labels"]["unique_labels"]
print(f"Found {len(resource_labels)} unique resource labels")
```

### Cost Analysis with Governance
```python
# Get cost data with governance context
costs = gcp.get_cost_data(
    start_date="2024-06-01",
    end_date="2024-06-30",
    bq_project_id="your-project-id",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_BILLING_ACCOUNT"
)

# Get governance policies
governance = gcp.get_governance_policies(
    bq_project_id="your-project-id",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_BILLING_ACCOUNT",
    gcp_billing_account="your-billing-account"
)

# Combine cost and governance data for comprehensive analysis
print("Cost Analysis with Governance Context:")
print(f"Total Cost: {costs['cost_data'][0]['total_cost']}")
print(f"Compliance Status: {governance['policy_compliance']['compliance_status']['overall_status']}")
print(f"Budget Alerts: {governance['cost_policies']['policies']['budget_policies']['budgets_configured']}")
```

---

## Error Handling

The governance methods include comprehensive error handling:

### Common Error Scenarios
1. **Missing IAM Permissions**: Clear error messages with recommendations
2. **BigQuery Export Not Configured**: Graceful fallback with setup instructions
3. **API Unavailable**: Conditional imports with helpful error messages
4. **No Data Available**: Appropriate status messages

### Example Error Handling
```python
try:
    governance_data = gcp.get_governance_policies(
        bq_project_id="your-project-id",
        gcp_billing_account="your-billing-account"
    )
    
    if "error" in governance_data:
        print(f"Error: {governance_data['error']}")
    else:
        print("Governance data retrieved successfully")
        
except Exception as e:
    print(f"Unexpected error: {e}")
```