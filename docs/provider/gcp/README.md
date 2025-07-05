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
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    granularity: str = "Daily",
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str): BigQuery project ID for billing export.
- `bq_dataset` (str): BigQuery dataset name for billing export.
- `bq_table` (str): BigQuery table name for billing export.
- `granularity` (str, optional): Data granularity for trends. Defaults to "Daily".
- `start_date` (str, optional, in kwargs): Start date for trend analysis.
- `end_date` (str, optional, in kwargs): End date for trend analysis.

**Returns:**
- Dictionary with cost trends data.

**Example:**
```python
trends = gcp.get_cost_trends(
    bq_project_id="your-bq-project",
    bq_dataset="your_billing_dataset",
    bq_table="your_billing_table",
    granularity="Daily",
    start_date="2024-06-01",
    end_date="2024-06-30"
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
- Resource cost data.

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
Forecast GCP costs for the specified period using BigQuery ML (ARIMA_PLUS model). This requires your billing export to BigQuery and BigQuery ML permissions.

**Signature:**
```python
def get_cost_forecast(
    self,
    bq_project_id: str,
    bq_dataset: str,
    bq_table: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    forecast_period: int = 14
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str): BigQuery project ID for billing export.
- `bq_dataset` (str): BigQuery dataset name for billing export.
- `bq_table` (str): BigQuery table name for billing export.
- `start_date` (str, optional): Historical data start date (YYYY-MM-DD). Defaults to first day of previous month.
- `end_date` (str, optional): Historical data end date (YYYY-MM-DD). Defaults to today.
- `forecast_period` (int, optional): Number of days to forecast. Default: 14.

**Returns:**
- Cost forecast data (requires BigQuery ML setup). Includes prediction intervals.

**Example:**
```python
forecast = gcp.get_cost_forecast(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX",
    start_date="2025-06-01",
    end_date="2025-07-04",
    forecast_period=12
)
print(forecast)
```

**Sample Response:**
```json
{
   "message": "Forecast generated using BigQuery ML ARIMA_PLUS model.",
   "period": {
      "start": "2025-06-01",
      "end": "2025-07-04"
   },
   "forecast_period_days": 12,
   "forecast": [
      {
         "date": "2025-07-04",
         "forecast_cost": 10.49,
         "prediction_interval_lower_bound": 9.12,
         "prediction_interval_upper_bound": 11.85
      },
      {
         "date": "2025-07-05",
         "forecast_cost": 9.67,
         "prediction_interval_lower_bound": 7.29,
         "prediction_interval_upper_bound": 12.04
      },
      // ... more days ...
   ]
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
efficiency = gcp.get_cost_efficiency_metrics(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX",
    start_date="2025-06-01",
    end_date="2025-07-04"
)
print(efficiency)
```

**Sample Response:**
```json
{
   "efficiency_metrics": {
      "total_days_analyzed": 30,
      "total_cost_period": 450.25,
      "avg_daily_cost": 15.01,
      "min_daily_cost": 8.50,
      "max_daily_cost": 25.75,
      "cost_stddev": 4.16,
      "cost_variance_ratio": 0.28,
      "cost_efficiency_score": 0.72,
      "waste_percentage": 15.3,
      "waste_days": 4,
      "method_used": "ML-enhanced",
      "ml_enabled": true
   },
   "period": {
      "start": "2025-06-01",
      "end": "2025-07-04"
   },
   "message": "Efficiency metrics calculated using ML-enhanced."
}
```

---

### generate_cost_report
Generate comprehensive cost report using BigQuery billing export data with detailed breakdowns and analysis.

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
) -> Dict[str, Any]:
```

**Parameters:**
- `bq_project_id` (str): BigQuery project ID for billing export.
- `bq_dataset` (str): BigQuery dataset name for billing export.
- `bq_table` (str): BigQuery table name for billing export.
- `report_type` (str): Type of report (monthly, quarterly, annual, custom). Default: "monthly".
- `start_date` (str, optional): Start date for report (YYYY-MM-DD).
- `end_date` (str, optional): End date for report (YYYY-MM-DD).

**Returns:**
- Comprehensive cost report with breakdowns and analysis.

**Example:**
```python
report = gcp.generate_cost_report(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX",
    report_type="monthly",
    start_date="2025-07-01",
    end_date="2025-07-05"
)
print(report)
```

**Sample Response:**
```json
{
   "report_type": "monthly",
   "period": {
      "start": "2025-07-01",
      "end": "2025-07-05"
   },
   "generated_at": "2025-07-05T12:47:55.275555",
   "summary": {
      "total_cost": 26.02,
      "total_days": 4,
      "avg_daily_cost": 0.01,
      "min_daily_cost": -0.47,
      "max_daily_cost": 0.47,
      "unique_services": 6,
      "unique_projects": 1,
      "unique_locations": 3
   },
   "breakdowns": {
      "by_service": [
         {
            "service": "Compute Engine",
            "total_cost": 11.62,
            "avg_daily_cost": 0.01
         },
         {
            "service": "VM Manager",
            "total_cost": 7.2,
            "avg_daily_cost": 0.26
         }
      ],
      "by_project": [
         {
            "project": "your-gcp-project",
            "total_cost": 26.02,
            "avg_daily_cost": 0.01
         }
      ],
      "by_location": [
         {
            "location": "us-central1",
            "total_cost": 17.81,
            "avg_daily_cost": 0.01
         }
      ]
   },
   "trends": {
      "daily_costs": [
         {
            "date": "2025-07-01",
            "daily_cost": 3.01
         },
         {
            "date": "2025-07-02",
            "daily_cost": 2.99
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
         "total_cost": 12.6
      }
   ],
   "efficiency_metrics": {
      "cost_efficiency_score": 0.36,
      "cost_variance_ratio": 0.64,
      "cost_stddev": 4.16
   },
   "message": "Comprehensive cost report generated for monthly period."
}
```

---

## 5. Governance & Compliance

### get_governance_policies
Get comprehensive governance policies and compliance status for GCP resources, including cost allocation labels, policy compliance, and cost policies.

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
- Comprehensive governance data including cost allocation labels, policy compliance, and cost policies.

**Example:**
```python
governance_data = gcp.get_governance_policies(
    bq_project_id="your-gcp-project",
    bq_dataset="billing_dataset",
    bq_table="gcp_billing_export_resource_v1_XXXXXX",
    gcp_billing_account="your-billing-account"
)
print(governance_data)
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
            "total_resources": 5,
            "compliance_checked": true,
            "status": "compliant",
            "resource_types_found": ["compute.googleapis.com/Instance", "storage.googleapis.com/Bucket"]
         },
         "organization_policy_compliance": {
            "policies_checked": 4,
            "policies_enforced": 2,
            "policy_details": {
               "compute.requireOsLogin": {
                  "enforced": true,
                  "policy_exists": true
               },
               "storage.uniformBucketLevelAccess": {
                  "enforced": false,
                  "policy_exists": false
               }
            },
            "status": "checked"
         },
         "cost_policy_compliance": {
            "budget_alerts_enabled": true,
            "cost_allocation_enabled": true,
            "resource_quota_enforced": false,
            "cost_monitoring_enabled": true
         },
         "overall_status": "compliant"
      },
      "message": "Policy compliance status retrieved from GCP Asset, Organization Policy, and Budget APIs"
   },
   "cost_policies": {
      "policies": {
         "budget_policies": {
            "budgets_configured": true,
            "total_budgets": 1,
            "budget_details": [
               {
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