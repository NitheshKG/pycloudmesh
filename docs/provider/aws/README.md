# AWS FinOps API Documentation

## 1. Cost Management

### get_cost_data
Fetches raw cost and usage data from AWS Cost Explorer.

**Signature:**
```python
def get_aws_cost_data(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "MONTHLY",
    metrics: Optional[List[str]] = None,
    group_by: Optional[List[Dict[str, str]]] = None,
    filter_: Optional[Dict[str, Any]] = None,
    sort_by: Optional[List[Dict[str, str]]] = None
) -> List[Dict[str, Any]]:
```

**Parameters:**
- `start_date` (str, optional): Start date in YYYY-MM-DD format. Defaults to 30 days ago.
- `end_date` (str, optional): End date in YYYY-MM-DD format. Defaults to today.
- `granularity` (str): "DAILY", "MONTHLY", or "HOURLY". Defaults to "MONTHLY".
- `metrics` (list, optional): List of AWS cost metrics (e.g., ["UnblendedCost"]).
- `group_by` (list, optional): List of dicts for grouping (e.g., [{"Type": "DIMENSION", "Key": "SERVICE"}]).
- `filter_` (dict, optional): AWS Cost Explorer filter expression.
- `sort_by` (list, optional): List of dicts for sorting.

**Returns:**
- List of cost and usage data dicts from AWS Cost Explorer.

**Example:**
```python
costs = aws.get_cost_data(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="DAILY",
    group_by=[{"Type": "DIMENSION", "Key": "SERVICE"}]
)
print(costs)
```

**Sample Response:**
```json
[
    {
        "TimePeriod": {
            "Start": "2024-01-01",
            "End": "2024-01-02"
        },
        "Total": {
            "UnblendedCost": {
                "Amount": "45.25",
                "Unit": "USD"
            }
        },
        "Groups": [
            {
                "Keys": ["Amazon EC2"],
                "Metrics": {
                    "UnblendedCost": {
                        "Amount": "25.50",
                        "Unit": "USD"
                    }
                }
            },
            {
                "Keys": ["Amazon S3"],
                "Metrics": {
                    "UnblendedCost": {
                        "Amount": "19.75",
                        "Unit": "USD"
                    }
                }
            }
        ],
        "Estimated": true
    }
]
```

---

### get_cost_analysis
Provides summarized cost analysis with breakdowns, top services, and actionable insights.

**Signature:**
```python
def get_aws_cost_analysis(
    self,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    dimensions: Optional[List[str]] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date for analysis.
- `end_date` (str, optional): End date for analysis.
- `dimensions` (list, optional): List of dimensions to analyze (e.g., ["SERVICE", "REGION"]).

**Returns:**
- Dictionary with period, dimensions, total_cost, cost_breakdown, top_services, cost_trends, and insights.

**Example:**
```python
analysis = aws.get_cost_analysis(
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["SERVICE", "REGION"]
)
print(analysis)
```

**Sample Response:**
```json
{
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "dimensions": ["SERVICE", "REGION"],
    "total_cost": 1250.75,
    "cost_breakdown": {
        "Amazon EC2": 650.50,
        "Amazon S3": 350.25,
        "Amazon RDS": 250.00
    },
    "top_services": [
        {"service": "Amazon EC2", "cost": 650.50, "percentage": 52.0},
        {"service": "Amazon S3", "cost": 350.25, "percentage": 28.0},
        {"service": "Amazon RDS", "cost": 250.00, "percentage": 20.0}
    ],
    "cost_trends": [
        {"date": "2024-01-01", "cost": 40.25},
        {"date": "2024-01-02", "cost": 42.50}
    ],
    "insights": [
        "Amazon EC2 represents 52% of total costs",
        "Consider reserved instances for cost optimization",
        "S3 costs are within expected range"
    ]
}
```

---

### get_cost_trends
Analyzes cost trends over time with patterns, growth rates, and trend detection.

**Signature:**
```python
def get_aws_cost_trends(self, **kwargs) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date for trend analysis.
- `end_date` (str, optional): End date for trend analysis.
- `granularity` (str, optional): "DAILY" or "MONTHLY". Defaults to "DAILY".
- Other Cost Explorer parameters as needed.

**Returns:**
- Dictionary with period, granularity, total_periods, total_cost, average_daily_cost, trend_direction, growth_rate, patterns, insights, peak_periods, and cost_periods.

**Example:**
```python
trends = aws.get_cost_trends(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="DAILY"
)
print(trends)
```

**Sample Response:**
```json
{
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "granularity": "DAILY",
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
    "cost_periods": [
        {"date": "2024-01-01", "cost": 38.25},
        {"date": "2024-01-02", "cost": 42.50},
        {"date": "2024-01-03", "cost": 41.75}
    ]
}
```

### get_resource_costs
Provides comprehensive resource cost analysis with utilization insights and optimization recommendations.

**Signature:**
```python
def get_aws_resource_costs(
    self,
    resource_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "DAILY"
) -> Dict[str, Any]:
```

**Parameters:**
- `resource_id` (str): AWS resource ID (e.g., EC2 instance ID, RDS instance ARN)
- `start_date` (str, optional): Start date for cost data (YYYY-MM-DD)
- `end_date` (str, optional): End date for cost data (YYYY-MM-DD)
- `granularity` (str): Data granularity (DAILY, MONTHLY). Default: "DAILY"

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
resource_costs = aws.get_aws_resource_costs(
    resource_id="i-1234567890abcdef0",
    start_date="2024-06-01",
    end_date="2024-06-30"
)
print(resource_costs)
```

**Sample Response:**
```json
{
   "resource_id": "i-1234567890abcdef0",
   "resource_type": "EC2 Instance",
   "period": {"start": "2024-06-01", "end": "2024-06-30"},
   "granularity": "DAILY",
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
Lists AWS budgets for an account.

**Signature:**
```python
def list_budgets(
    self,
    account_id: str,
    max_results: Optional[int] = None,
    next_token: Optional[str] = None
) -> Dict[str, Any]:
```

**Parameters:**
- `account_id` (str): AWS account ID.
- `max_results` (int, optional): Maximum number of results to return.
- `next_token` (str, optional): Token for pagination.

**Returns:**
- List of budgets and pagination information.

**Example:**
```python
budgets = aws.list_budgets(account_id="123456789012")
print(budgets)
```

**Sample Response:**
```json
{
    "Budgets": [
        {
            "BudgetName": "Monthly Budget",
            "BudgetLimit": {
                "Amount": "1000.00",
                "Unit": "USD"
            },
            "TimeUnit": "MONTHLY",
            "BudgetType": "COST",
            "CalculatedSpend": {
                "ActualSpend": {
                    "Amount": "750.25",
                    "Unit": "USD"
                },
                "ForecastedSpend": {
                    "Amount": "950.00",
                    "Unit": "USD"
                }
            },
            "TimePeriod": {
                "Start": "2024-01-01T00:00:00Z",
                "End": "2024-12-31T23:59:59Z"
            },
            "LastUpdatedTime": "2024-01-15T10:30:00.123000+00:00",
            "CostTypes": {
                "IncludeTax": true,
                "IncludeSubscription": true,
                "UseBlended": false,
                "IncludeRefund": true,
                "IncludeCredit": true,
                "IncludeUpfront": true,
                "IncludeRecurring": true,
                "IncludeOtherSubscription": true,
                "IncludeSupport": true,
                "IncludeDiscount": true,
                "UseAmortized": false
            }
        }
    ],
    "ResponseMetadata": {
        "RequestId": "398fb9d7-4a39-4f5b-bef0-1e4be3301173",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "date": "Sun, 27 Jul 2025 11:54:03 GMT",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "11917",
            "connection": "keep-alive",
            "x-amzn-requestid": "398fb9d7-4a39-4f5b-bef0-1e4be3301173",
            "cache-control": "no-store, no-cache"
        },
        "RetryAttempts": 0
    }
}
```

**Note:** When using `json.dumps()` to print the response, use a custom JSON encoder to handle datetime objects:
```python
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Usage
print(json.dumps(budgets, indent=4, cls=DateTimeEncoder))
```

---

### create_budget
Creates a new AWS budget.

**Signature:**
```python
def create_budget(
    self,
    account_id: str,
    budget_name: str,
    budget_amount: float,
    budget_type: str = "COST",
    time_unit: str = "MONTHLY",
    notifications_with_subscribers: list = None
) -> Dict[str, Any]:
```

**Parameters:**
- `account_id` (str): AWS account ID.
- `budget_name` (str): Name of the budget.
- `budget_amount` (float): Budget amount.
- `budget_type` (str): Type of budget (COST, USAGE, RI_UTILIZATION, RI_COVERAGE). Defaults to "COST".
- `time_unit` (str): Time unit for the budget (MONTHLY, QUARTERLY, ANNUALLY). Defaults to "MONTHLY".
- `notifications_with_subscribers` (list, optional): List of notification dicts.

**Returns:**
- Budget creation response.

**Example:**
```python
budget = aws.create_budget(
    aws_account_id="123456789012",
    budget_name="Monthly Budget",
    budget_amount=1000.0,
    notifications=[
        {
            "Notification": {
                "NotificationType": "ACTUAL",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 80.0,
                "ThresholdType": "PERCENTAGE"
            },
            "Subscribers": [
                {"SubscriptionType": "EMAIL", "Address": "admin@example.com"}
            ]
        }
    ]
)
print(budget)
```

**Sample Response:**
```json
{
    "ResponseMetadata": {
        "RequestId": "6b13740c-5eb5-4179-bb9b-0ab8a12fe91b",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "date": "Sun, 27 Jul 2025 10:37:12 GMT",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "2",
            "connection": "keep-alive",
            "x-amzn-requestid": "6b13740c-5eb5-4179-bb9b-0ab8a12fe91b",
            "cache-control": "no-store, no-cache"
        },
        "RetryAttempts": 0
    }
}
```

**Error Response (Duplicate Budget):**
```json
{
    "error": "Failed to create budget: An error occurred (DuplicateRecordException) when calling the CreateBudget operation: Error creating budget: Monthly Budget - the budget already exists."
}
```

---

### get_budget_notifications
Gets notifications for a specific budget.

**Signature:**
```python
def get_budget_notifications(
    self,
    account_id: str,
    budget_name: str
) -> Dict[str, Any]:
```

**Parameters:**
- `account_id` (str): AWS account ID.
- `budget_name` (str): Name of the budget.

**Returns:**
- Budget notifications.

**Example:**
```python
alerts = aws.get_budget_notifications(
    account_id="123456789012",
    budget_name="Monthly Budget"
)
print(alerts)
```

**Sample Response:**
```json
{
    "Notifications": [
        {
            "NotificationType": "ACTUAL",
            "ComparisonOperator": "GREATER_THAN",
            "Threshold": 80.0,
            "ThresholdType": "PERCENTAGE",
            "NotificationState": "ALARM",
            "Subscribers": [
                {
                    "SubscriptionType": "EMAIL",
                    "Address": "admin@example.com"
                }
            ]
        },
        {
            "NotificationType": "FORECASTED",
            "ComparisonOperator": "GREATER_THAN",
            "Threshold": 100.0,
            "ThresholdType": "PERCENTAGE",
            "NotificationState": "OK",
            "Subscribers": [
                {
                    "SubscriptionType": "EMAIL",
                    "Address": "admin@example.com"
                }
            ]
        }
    ]
}
```

## 3. Optimization & Recommendations

### get_optimization_recommendations
Get comprehensive optimization recommendations (savings plans, reservations, rightsizing, idle resources).

**Signature:**
```python
def get_optimization_recommendations(self) -> Dict[str, Any]:
```

**Returns:**
- Dictionary with keys: 'savings_plans', 'reservations', 'rightsizing', 'idle_resources'.

**Example:**
```python
optimizations = aws.get_optimization_recommendations()
```

---

### get_savings_plans_recommendations
Get AWS Savings Plans recommendations with optional parameters.

**Signature:**
```python
def get_savings_plans_recommendations(self, **kwargs) -> Dict[str, Any]:
```

**Parameters:**
- `SavingsPlansType` (str, optional): COMPUTE_SP, EC2_INSTANCE_SP, etc. Default: COMPUTE_SP
- `AccountScope` (str, optional): PAYER or LINKED. Default: PAYER
- `LookbackPeriodInDays` (str, optional): SEVEN_DAYS, THIRTY_DAYS, SIXTY_DAYS. Default: THIRTY_DAYS
- `TermInYears` (str, optional): ONE_YEAR, THREE_YEARS. Default: ONE_YEAR
- `PaymentOption` (str, optional): NO_UPFRONT, PARTIAL_UPFRONT, ALL_UPFRONT. Default: NO_UPFRONT
- Other Cost Explorer parameters as needed.

**Returns:**
- Savings Plans recommendations.

**Example:**
```python
savings_plans = aws.get_savings_plans_recommendations(
    SavingsPlansType="EC2_INSTANCE_SP",
    TermInYears="THREE_YEARS",
    PaymentOption="ALL_UPFRONT"
)
```

---

### get_reservation_purchase_recommendations
Get AWS Reserved Instance recommendations with optional parameters.

**Signature:**
```python
def get_reservation_purchase_recommendations(self, **kwargs) -> Dict[str, Any]:
```

**Parameters:**
- `AccountScope` (str, optional): PAYER or LINKED. Default: PAYER
- `LookbackPeriodInDays` (str, optional): SEVEN_DAYS, THIRTY_DAYS, SIXTY_DAYS. Default: THIRTY_DAYS
- `TermInYears` (str, optional): ONE_YEAR, THREE_YEARS. Default: ONE_YEAR
- `PaymentOption` (str, optional): NO_UPFRONT, PARTIAL_UPFRONT, ALL_UPFRONT. Default: NO_UPFRONT
- `Service` (str, optional): e.g., AmazonEC2, AmazonRDS, etc. Default: Amazon Elastic Compute Cloud - Compute
- Other Cost Explorer parameters as needed.

**Returns:**
- Reserved Instance recommendations.

**Example:**
```python
reservation_recs = aws.get_reservation_purchase_recommendations(
    Service="Amazon Redshift",
    TermInYears="THREE_YEARS",
    PaymentOption="ALL_UPFRONT"
)
```

---

### get_rightsizing_recommendations
Get AWS rightsizing recommendations with optional parameters.

**Signature:**
```python
def get_rightsizing_recommendations(self, **kwargs) -> Dict[str, Any]:
```

**Parameters:**
- `Service` (str, optional): e.g., AmazonEC2. Default: AmazonEC2
- `Filter`, `Configuration`, `PageSize`, `NextPageToken` (optional): See AWS docs for details.

**Returns:**
- Rightsizing recommendations.

**Example:**
```python
rightsizing = aws.get_rightsizing_recommendations(
    Service="AmazonEC2",
    Configuration={"RecommendationTarget": "SAME_INSTANCE_FAMILY", "BenefitsConsidered": True}
)
```

---

### get_idle_resources
Identify idle or underutilized resources (EC2, etc.).

**Signature:**
```python
def get_idle_resources(self, **kwargs) -> Dict[str, Any]:
```

**Parameters:**
- `InstanceIds`, `DryRun`, `Filters`, `NextToken`, `MaxResults` (optional): See AWS docs for details.

**Returns:**
- List of idle resources with cost impact.

**Example:**
```python
idle_resources = aws.get_idle_resources(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])
```

## 4. Advanced Analytics

### get_cost_forecast
Get cost forecast for the specified period (future), with robust defaults.

**Signature:**
```python
def get_cost_forecast(
    self,
    TimePeriod: dict = None,
    Metric: str = "UNBLENDED_COST",
    Granularity: str = "MONTHLY",
    Filter: dict = None,
    BillingViewArn: str = None,
    PredictionIntervalLevel: int = None,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `TimePeriod` (dict, optional): {"Start": YYYY-MM-DD, "End": YYYY-MM-DD}. Defaults to today to today+30 days.
- `Metric` (str, optional): Cost metric. Default: "UNBLENDED_COST".
- `Granularity` (str, optional): "DAILY" or "MONTHLY". Default: "MONTHLY".
- `Filter` (dict, optional): Cost Explorer filter.
- `BillingViewArn` (str, optional): Billing view ARN.
- `PredictionIntervalLevel` (int, optional): Confidence interval.
- `**kwargs`: Any other supported parameters.

**Returns:**
- Cost forecast data.

**Example:**
```python
forecast = aws.get_cost_forecast(
    TimePeriod={"Start": "2024-07-01", "End": "2024-08-01"},
    Metric="BLENDED_COST",
    Granularity="DAILY"
)
```

---

### get_cost_anomalies
Get cost anomalies for a given period, with robust defaults.

**Signature:**
```python
def get_cost_anomalies(
    self,
    DateInterval: dict = None,
    MonitorArn: str = None,
    Feedback: str = None,
    TotalImpact: dict = None,
    NextPageToken: str = None,
    MaxResults: int = None,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `DateInterval` (dict, optional): {"StartDate": YYYY-MM-DD, "EndDate": YYYY-MM-DD}. Defaults to one month prior to today.
- `MonitorArn` (str, optional): ARN of the anomaly monitor.
- `Feedback` (str, optional): Feedback string.
- `TotalImpact` (dict, optional): {"NumericOperator": ..., "StartValue": ...}.
- `NextPageToken` (str, optional): For pagination.
- `MaxResults` (int, optional): Max results per page.
- `**kwargs`: Any other supported parameters.

**Returns:**
- Cost anomalies data.

**Example:**
```python
anomalies = aws.get_cost_anomalies(
    MonitorArn="arn:aws:ce:us-east-1:123456789012:anomalymonitor/your-monitor",
    DateInterval={"StartDate": "2024-06-01", "EndDate": "2024-07-01"},
    MaxResults=50
)
```

---

### get_cost_efficiency_metrics
Calculate cost efficiency metrics (cost per user, per transaction, etc.), with robust defaults.

**Signature:**
```python
def get_cost_efficiency_metrics(
    self,
    user_count: int = None,
    transaction_count: int = None,
    TimePeriod: dict = None,
    Granularity: str = "MONTHLY",
    Metrics: list = ["UnblendedCost"],
    GroupBy: list = [{"Type": "DIMENSION", "Key": "SERVICE"}],
    Filter: dict = None,
    BillingViewArn: str = None,
    NextPageToken: str = None,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `user_count` (int, optional): Number of users for cost per user.
- `transaction_count` (int, optional): Number of transactions for cost per transaction.
- `TimePeriod` (dict, optional): {"Start": YYYY-MM-DD, "End": YYYY-MM-DD}. Defaults to current month.
- `Granularity` (str, optional): "DAILY" or "MONTHLY". Default: "MONTHLY".
- `Metrics` (list, optional): List of metrics. Default: ["UnblendedCost"].
- `GroupBy` (list, optional): Grouping. Default: [{"Type": "DIMENSION", "Key": "SERVICE"}].
- `Filter` (dict, optional): Cost Explorer filter.
- `BillingViewArn` (str, optional): Billing view ARN.
- `NextPageToken` (str, optional): For pagination.
- `**kwargs`: Any other supported parameters.

**Returns:**
- Cost efficiency metrics.

**Example:**
```python
efficiency = aws.get_cost_efficiency_metrics(
    user_count=100,
    transaction_count=10000,
    TimePeriod={"Start": "2024-06-01", "End": "2024-07-01"},
    Granularity="DAILY"
)
```

---

### generate_cost_report
Generate a comprehensive cost report, robust to missing metrics.

**Signature:**
```python
def generate_cost_report(
    self,
    report_type: str = "monthly",
    TimePeriod: dict = None,
    Granularity: str = "MONTHLY",
    Metrics: list = ["UnblendedCost"],
    GroupBy: list = [{"Type": "DIMENSION", "Key": "SERVICE"}],
    Filter: dict = None,
    BillingViewArn: str = None,
    NextPageToken: str = None,
    **kwargs
) -> Dict[str, Any]:
```

**Parameters:**
- `report_type` (str, optional): Type of report (monthly, quarterly, annual). Default: "monthly".
- `TimePeriod` (dict, optional): {"Start": YYYY-MM-DD, "End": YYYY-MM-DD}. Defaults to current month.
- `Granularity` (str, optional): "DAILY" or "MONTHLY". Default: "MONTHLY".
- `Metrics` (list, optional): List of metrics. Default: ["UnblendedCost"].
- `GroupBy` (list, optional): Grouping. Default: [{"Type": "DIMENSION", "Key": "SERVICE"}].
- `Filter` (dict, optional): Cost Explorer filter.
- `BillingViewArn` (str, optional): Billing view ARN.
- `NextPageToken` (str, optional): For pagination.
- `**kwargs`: Any other supported parameters.

**Returns:**
- Cost report data.

**Example:**
```python
report = aws.generate_cost_report(
    report_type="custom",
    TimePeriod={"Start": "2024-06-01", "End": "2024-07-01"},
    Granularity="DAILY",
    Metrics=["BlendedCost", "UsageQuantity"],
    GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
)
```

## 5. Governance & Compliance

### get_governance_policies
Get AWS cost-related management policies (e.g., Service Control Policies mentioning cost).

**Signature:**
```python
def get_cost_policies(self, **kwargs) -> Dict[str, Any]:
```

**Parameters:**
- `**kwargs`: Optional filter parameters (see AWS Organizations API).

**Returns:**
- Dictionary with a list of cost-related policies (id, name, description, type, aws_managed, content, arn, tags).

**Example:**
```python
policies = aws.get_cost_policies()
```

---

### get_cost_allocation_tags
Get cost allocation tags for a given resource.

**Signature:**
```python
def get_cost_allocation_tags(self, ResourceId: str = "") -> Dict[str, Any]:
```

**Parameters:**
- `ResourceId` (str, optional): AWS resource ID. Default: "" (empty string).

**Returns:**
- Cost allocation tags for the resource.

**Example:**
```python
tags = aws.get_cost_allocation_tags(ResourceId="your-resource-id")
```

---

### get_compliance_status
Get compliance status for cost policies.

**Signature:**
```python
def get_compliance_status(self, ConfigRuleName: str = None) -> Dict[str, Any]:
```

**Parameters:**
- `ConfigRuleName` (str, optional): Name of the AWS Config rule to check compliance for.

**Returns:**
- Compliance status for the specified rule.

**Example:**
```python
compliance = aws.get_compliance_status(ConfigRuleName="required-tags")
```

## 6. Reservation Management

### get_reservation_cost
Get AWS reservation utilization and cost data.

**Signature:**
```python
def get_reservation_cost(
    self,
    start_date: str = None,
    end_date: str = None,
    granularity: str = "MONTHLY"
) -> Dict[str, Any]:
```

**Parameters:**
- `start_date` (str, optional): Start date in YYYY-MM-DD format. Defaults to one month before today.
- `end_date` (str, optional): End date in YYYY-MM-DD format. Defaults to today.
- `granularity` (str, optional): "DAILY", "MONTHLY", or "HOURLY". Default: "MONTHLY".

**Returns:**
- Reservation utilization data from AWS Cost Explorer.

**Example:**
```python
reservation_costs = aws.get_reservation_cost(
    start_date="2024-06-01",
    end_date="2024-06-30",
    granularity="DAILY"
)
```

---

### get_reservation_purchase_recommendation
Get AWS reservation purchase recommendations for various services.

**Signature:**
```python
def get_reservation_purchase_recommendation(
    self,
    Service: str = "AmazonEC2",
    LookbackPeriodInDays: str = "SIXTY_DAYS",
    TermInYears: str = "ONE_YEAR",
    PaymentOption: str = "NO_UPFRONT",
    AccountScope: str = "PAYER",
    AccountId: str = None,
    NextPageToken: str = None,
    PageSize: int = None,
    Filter: dict = None,
    ServiceSpecification: dict = None
) -> dict:
```

**Parameters:**
- `Service` (str, optional): e.g., 'AmazonEC2', 'AmazonRDS', etc. Default: 'AmazonEC2'.
- `LookbackPeriodInDays` (str, optional): 'SEVEN_DAYS', 'THIRTY_DAYS', 'SIXTY_DAYS'. Default: 'SIXTY_DAYS'.
- `TermInYears` (str, optional): 'ONE_YEAR', 'THREE_YEARS'. Default: 'ONE_YEAR'.
- `PaymentOption` (str, optional): 'NO_UPFRONT', 'PARTIAL_UPFRONT', 'ALL_UPFRONT'. Default: 'NO_UPFRONT'.
- `AccountScope` (str, optional): 'PAYER' or 'LINKED'. Default: 'PAYER'.
- `AccountId` (str, optional): AWS Account ID.
- `NextPageToken` (str, optional): For pagination.
- `PageSize` (int, optional): For pagination.
- `Filter` (dict, optional): Expression for filtering.
- `ServiceSpecification` (dict, optional): e.g., {"EC2Specification": {"OfferingClass": "STANDARD"}}.

**Returns:**
- Full response from AWS get_reservation_purchase_recommendation.

**Example:**
```python
recommendations = aws.get_reservation_purchase_recommendation(
    Service="AmazonEC2",
    TermInYears="THREE_YEARS",
    PaymentOption="ALL_UPFRONT"
)
```

---

### get_reservation_coverage
Get AWS reservation coverage data using Cost Explorer.

**Signature:**
```python
def get_reservation_coverage(
    self,
    start_date: str = None,
    end_date: str = None,
    granularity: str = "MONTHLY",
    GroupBy: list = None,
    Filter: dict = None,
    NextPageToken: str = None
) -> dict:
```

**Parameters:**
- `start_date` (str, optional): Start date in YYYY-MM-DD format. Default: 30 days ago.
- `end_date` (str, optional): End date in YYYY-MM-DD format. Default: today.
- `granularity` (str, optional): 'DAILY' or 'MONTHLY'. Default: 'MONTHLY'.
- `GroupBy` (list, optional): List of dicts for grouping.
- `Filter` (dict, optional): Expression for filtering.
- `NextPageToken` (str, optional): For pagination.

**Returns:**
- Full response from AWS get_reservation_coverage.

**Example:**
```python
coverage = aws.get_reservation_coverage(
    start_date="2024-06-01",
    end_date="2024-06-30",
    granularity="DAILY",
    GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
)
``` 