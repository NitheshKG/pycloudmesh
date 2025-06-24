# PyCloudMesh - Comprehensive FinOps Management

PyCloudMesh is a unified Python library for comprehensive Financial Operations (FinOps) management across AWS, Azure, and GCP. It provides a consistent interface for cost optimization, governance, analytics, and resource management across all major cloud providers.

## 🌟 Features

### Core FinOps Capabilities
- **Cost Management**: Real-time cost tracking, analysis, and reporting
- **Budget Management**: Create, monitor, and manage budgets with alerts
- **Reservation Management**: Optimize costs with reserved instances and committed use discounts
- **Resource Optimization**: Identify idle resources and get optimization recommendations
- **Cost Forecasting**: Predict future costs using historical data
- **Anomaly Detection**: Detect unusual spending patterns
- **Governance**: Policy compliance and cost allocation management
- **Analytics**: Advanced cost efficiency metrics and reporting

### Cloud Provider Support
- **AWS**: Full integration with Cost Explorer, Budgets, Reservations, and Savings Plans
- **Azure**: Complete Cost Management, Budgets, Reservations, and Advisor integration
- **GCP**: Billing API, Budgets, Recommender API, and BigQuery integration

## 🚀 Quick Start

### Installation

```bash
pip install pycloudmesh
```

### Basic Usage

```python
from pycloudmesh import aws_client, azure_client, gcp_client

# AWS FinOps
aws = aws_client("your_access_key", "your_secret_key", "us-east-1")

# Get cost data
costs = aws.get_cost_data(start_date="2024-01-01", end_date="2024-01-31")

# Get optimization recommendations
optimizations = aws.get_optimization_recommendations()

# Create budget
budget = aws.create_budget(
    aws_account_id="123456789012",
    budget_name="Monthly Budget",
    budget_amount=1000.0
)

# Azure FinOps
azure = azure_client("your_subscription_id", "your_token")

# Get cost analysis
analysis = azure.get_cost_analysis(
    dimensions=["SERVICE", "REGION"]
)

# Get advisor recommendations
advisor_recs = azure.get_advisor_recommendations()

# GCP FinOps
gcp = gcp_client("your_project_id", "/path/to/credentials.json")

# Get machine type recommendations
machine_recs = gcp.get_machine_type_recommendations()

# List budgets
budgets = gcp.list_budgets(billing_account="your_billing_account")
```

## 📊 Comprehensive FinOps Features

### 1. Cost Management

#### AWS Cost Management Methods

PyCloudMesh provides four distinct AWS cost management methods, each serving different purposes:

##### 1.1 `get_cost_data` - Raw Cost Data
Fetches raw cost and usage data from AWS Cost Explorer without any processing.

```python
# Get raw cost data
cost_data = aws.get_cost_data(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="DAILY",
    group_by=[{"Type": "DIMENSION", "Key": "SERVICE"}, {"Type": "DIMENSION", "Key": "REGION"}]
)

# Example output structure:
[
    {
        "TimePeriod": {"Start": "2024-01-01", "End": "2024-01-02"},
        "Groups": [
            {
                "Keys": ["AmazonEC2", "us-east-1"],
                "Metrics": {"UnblendedCost": {"Amount": "1.23", "Unit": "USD"}}
            }
        ],
        "Total": {"UnblendedCost": {"Amount": "1.68", "Unit": "USD"}},
        "Estimated": False
    }
    # ... more periods
]
```

**Use case:** Custom reporting, data export, when you need raw AWS data.

##### 1.2 `get_cost_analysis` - Cost Analysis with Insights
Provides summarized cost analysis with breakdowns, top services, and actionable insights.

```python
# Get cost analysis with insights
analysis = aws.get_cost_analysis(
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["SERVICE", "REGION"]
)

# Example output structure:
{
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "dimensions": ["SERVICE", "REGION"],
    "total_cost": 123.45,
    "cost_breakdown": {
        "AmazonEC2": 80.00,
        "AmazonS3": 30.00,
        "AmazonRDS": 13.45
    },
    "top_services": [
        {"service": "AmazonEC2", "cost": 80.00},
        {"service": "AmazonS3", "cost": 30.00},
        {"service": "AmazonRDS", "cost": 13.45}
    ],
    "cost_trends": [
        {"period": "2024-01-01 to 2024-01-02", "cost": 4.00}
    ],
    "insights": [
        "Top service 'AmazonEC2' accounts for 64.8% of total costs",
        "Top 3 services account for 100.0% of total costs"
    ]
}
```

**Use case:** High-level cost summary, executive reporting, cost optimization insights.

##### 1.3 `get_cost_trends` - Cost Trends Analysis
Analyzes cost trends over time with patterns, growth rates, and trend detection.

```python
# Get cost trends (now accepts flexible parameters and has robust defaults)
trends = aws.get_cost_trends()

# Example with custom parameters
trends = aws.get_cost_trends(
    start_date="2024-06-01",
    end_date="2024-07-01",
    granularity="DAILY",
    metrics=["UnblendedCost"],
    group_by=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    filter_={
        # ... your filter structure ...
    }
)

# Example output structure:
{
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "granularity": "DAILY",
    "total_periods": 31,
    "total_cost": 123.45,
    "average_daily_cost": 3.98,
    "trend_direction": "increasing",
    "growth_rate": 15.2,
    "patterns": ["High cost variability", "Weekend cost reduction"],
    "insights": [
        "Total cost over 31 periods: $123.45",
        "Average cost per period: $3.98",
        "Cost trend is increasing (15.2% change)",
        "Peak cost period: 2024-01-15 to 2024-01-16 ($8.00)"
    ],
    "peak_periods": [
        {"period": "2024-01-15 to 2024-01-16", "cost": 8.00, "date": "2024-01-15"}
    ],
    "cost_periods": [
        {"period": "2024-01-01 to 2024-01-02", "cost": 4.00, "date": "2024-01-01"}
    ]
}
```

**Use case:** Trend analysis, anomaly detection, cost forecasting preparation.

##### 1.4 `get_resource_costs` - Resource-Level Cost Analysis
Provides resource-specific cost analysis with utilization insights and recommendations.

```python
# Get resource-specific costs
resource_costs = aws.get_resource_costs(
    resource_id="i-0df615a5315c31029",
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="DAILY"
)

# Example output structure:
{
    "resource_id": "i-0df615a5315c31029",
    "resource_type": "EC2 Instance",
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "granularity": "DAILY",
    "total_cost": 12.34,
    "total_periods": 31,
    "active_periods": 20,
    "cost_breakdown": {
        "BoxUsage:t2.micro": 10.00,
        "DataTransfer-Out-Bytes": 2.34
    },
    "utilization_insights": [
        "EC2 utilization rate: 64.5% (20 active out of 31 periods)",
        "Low EC2 utilization detected - consider stopping or downsizing instances"
    ],
    "cost_trends": ["EC2 cost trend: Stable"],
    "recommendations": [
        "Top EC2 cost component: BoxUsage:t2.micro (81.0% of total) - review for optimization",
        "Note: Analysis based on EC2 service costs. For specific resource costs, use AWS Cost Explorer with resource tags."
    ]
}
```

**Use case:** Resource optimization, instance-level cost analysis, utilization monitoring.

#### Method Comparison Summary

| Method | Returns | Analysis Level | Insights | Grouping | Best For |
|--------|---------|---------------|----------|----------|----------|
| `get_cost_data` | Raw list | Any | ❌ | Custom | Custom reporting, data export |
| `get_cost_analysis` | Summary dict | Account-wide | ✅ | Service/Region | Executive summaries, cost breakdowns |
| `get_cost_trends` | Trends dict | Account-wide | ✅ | Time-based | Trend analysis, anomaly detection |
| `get_resource_costs` | Resource dict | Resource/Type | ✅ | Service/Usage | Resource optimization, utilization |

#### Azure Cost Management
Azure provides the same four cost management methods with Azure-specific implementations:

##### 1.1 `get_cost_data` - Raw Cost Data
Fetches raw cost and usage data from Azure Cost Management API.

```python
# Get raw cost data
cost_data = azure.get_cost_data(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily",
    group_by=["ResourceType", "ResourceLocation"]
)

# Example output structure:
{
    "properties": {
        "nextLink": "https://management.azure.com/subscriptions/...",
        "columns": [
            {"name": "UsageDate", "type": "String"},
            {"name": "ResourceType", "type": "String"},
            {"name": "ResourceLocation", "type": "String"},
            {"name": "PreTaxCost", "type": "Number"}
        ],
        "rows": [
            ["2024-01-01", "Microsoft.Compute/virtualMachines", "East US", 15.50],
            ["2024-01-01", "Microsoft.Storage/storageAccounts", "East US", 2.30]
        ]
    }
}
```

**Use case:** Custom reporting, data export, when you need raw Azure cost data.

##### 1.2 `get_cost_analysis` - Cost Analysis with Insights
Provides summarized cost analysis with Azure-specific dimensions.

```python
# Get cost analysis with insights
analysis = azure.get_cost_analysis(
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["ResourceType", "ResourceLocation", "ResourceGroupName"]
)

# Example output structure:
{
    "properties": {
        "columns": [
            {"name": "ResourceType", "type": "String"},
            {"name": "ResourceLocation", "type": "String"},
            {"name": "ResourceGroupName", "type": "String"},
            {"name": "PreTaxCost", "type": "Number"}
        ],
        "rows": [
            ["Microsoft.Compute/virtualMachines", "East US", "my-rg", 465.00],
            ["Microsoft.Storage/storageAccounts", "East US", "my-rg", 69.00],
            ["Microsoft.Network/virtualNetworks", "East US", "my-rg", 12.00]
        ]
    }
}
```

**Use case:** High-level cost summary, executive reporting, Azure resource optimization.

##### 1.3 `get_cost_trends` - Cost Trends Analysis
Analyzes cost trends over time with Azure-specific granularity.

```python
# Get cost trends with detailed analysis
trends = azure.get_cost_trends(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily"
)

# Example output structure:
{
    "properties": {
        "columns": [
            {"name": "UsageDate", "type": "String"},
            {"name": "PreTaxCost", "type": "Number"}
        ],
        "rows": [
            ["2024-01-01", 18.50],
            ["2024-01-02", 19.20],
            ["2024-01-03", 17.80]
        ]
    }
}
```

**Use case:** Trend analysis, anomaly detection, Azure cost forecasting preparation.

##### 1.4 `get_resource_costs` - Resource-Level Cost Analysis
Provides resource-specific cost analysis for Azure resources.

```python
# Get resource-specific costs
resource_costs = azure.get_resource_costs(
    resource_id="/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg/providers/Microsoft.Compute/virtualMachines/my-vm",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Example output structure:
{
    "properties": {
        "columns": [
            {"name": "UsageDate", "type": "String"},
            {"name": "ResourceId", "type": "String"},
            {"name": "PreTaxCost", "type": "Number"}
        ],
        "rows": [
            ["2024-01-01", "/subscriptions/.../virtualMachines/my-vm", 15.50],
            ["2024-01-02", "/subscriptions/.../virtualMachines/my-vm", 15.50]
        ]
    }
}
```

**Use case:** Azure resource optimization, VM-level cost analysis, utilization monitoring.

#### GCP Cost Management
GCP provides the same four cost management methods with GCP-specific implementations:

##### 1.1 `get_cost_data` - Raw Cost Data
Fetches raw cost and usage data from GCP Billing API (requires BigQuery billing export).

```python
# Get raw cost data
cost_data = gcp.get_cost_data(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily",
    group_by=["service", "location", "project"]
)

# Example output structure:
{
    "message": "GCP cost data requires BigQuery billing export setup",
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "cost_data": [
        {
            "usage_start_time": "2024-01-01T00:00:00Z",
            "usage_end_time": "2024-01-02T00:00:00Z",
            "service": "Compute Engine",
            "location": "us-central1",
            "project": "my-project",
            "cost": 12.50
        }
    ]
}
```

**Use case:** Custom reporting, data export, when you need raw GCP cost data.

##### 1.2 `get_cost_analysis` - Cost Analysis with Insights
Provides summarized cost analysis with GCP-specific dimensions.

```python
# Get cost analysis with insights
analysis = gcp.get_cost_analysis(
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["service", "location", "project"]
)

# Example output structure:
{
    "message": "GCP cost analysis requires BigQuery billing export setup",
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "cost_breakdown": {
        "Compute Engine": 375.00,
        "Cloud Storage": 45.00,
        "Cloud SQL": 120.00
    },
    "dimensions": ["service", "location", "project"]
}
```

**Use case:** High-level cost summary, executive reporting, GCP service optimization.

##### 1.3 `get_cost_trends` - Cost Trends Analysis
Analyzes cost trends over time with GCP-specific granularity.

```python
# Get cost trends with detailed analysis
trends = gcp.get_cost_trends(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily"
)

# Example output structure:
{
    "message": "GCP cost trends require BigQuery billing export setup",
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "granularity": "Daily",
    "cost_trends": [
        {"date": "2024-01-01", "cost": 18.50},
        {"date": "2024-01-02", "cost": 19.20},
        {"date": "2024-01-03", "cost": 17.80}
    ]
}
```

**Use case:** Trend analysis, anomaly detection, GCP cost forecasting preparation.

##### 1.4 `get_resource_costs` - Resource-Level Cost Analysis
Provides resource-specific cost analysis for GCP resources.

```python
# Get resource-specific costs
resource_costs = gcp.get_resource_costs(
    resource_id="projects/my-project/zones/us-central1-a/instances/my-instance",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Example output structure:
{
    "message": "GCP resource costs require BigQuery billing export setup",
    "resource_id": "projects/my-project/zones/us-central1-a/instances/my-instance",
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "cost_breakdown": {
        "Compute Engine Instance": 15.50,
        "Persistent Disk": 2.30,
        "Network Egress": 1.20
    }
}
```

**Use case:** GCP resource optimization, instance-level cost analysis, utilization monitoring.

#### Cross-Cloud Method Comparison

| Method | AWS | Azure | GCP | Best For |
|--------|-----|-------|-----|----------|
| `get_cost_data` | ✅ Raw Cost Explorer data | ✅ Raw Cost Management data | ✅ Raw Billing data (BigQuery) | Custom reporting, data export |
| `get_cost_analysis` | ✅ Enhanced with insights | ✅ Azure-specific dimensions | ✅ GCP-specific dimensions | Executive summaries, cost breakdowns |
| `get_cost_trends` | ✅ Enhanced trend analysis | ✅ Time-based analysis | ✅ Time-based analysis | Trend analysis, anomaly detection |
| `get_resource_costs` | ✅ Resource-level analysis | ✅ Resource-specific filtering | ✅ Resource-specific filtering | Resource optimization, utilization |

### 2. Budget Management

#### AWS Budget Management
Create and manage budgets with notifications and thresholds:

```python
# List all budgets
budgets = aws.list_budgets(aws_account_id="123456789012")

# Create budget with notifications and thresholds
notifications = [{
    "Notification": {
        "NotificationType": "ACTUAL",
        "ComparisonOperator": "GREATER_THAN",
        "Threshold": 80.0,
        "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [
        {
            "SubscriptionType": "EMAIL",
            "Address": "admin@company.com"
        }
    ]
}]

# Create monthly budget with 80% threshold notification
monthly_budget = aws.create_budget(
    aws_account_id="123456789012",
    budget_name="Monthly Production Budget",
    budget_amount=5000.0,
    budget_type="COST",
    time_unit="MONTHLY",
    notifications_with_subscribers=notifications
)

# Create quarterly budget with multiple thresholds
quarterly_notifications = [
    {
        "Notification": {
            "NotificationType": "ACTUAL",
            "ComparisonOperator": "GREATER_THAN",
            "Threshold": 50.0,
            "ThresholdType": "PERCENTAGE"
        },
        "Subscribers": [
            {"SubscriptionType": "EMAIL", "Address": "team@company.com"}
        ]
    },
    {
        "Notification": {
            "NotificationType": "ACTUAL",
            "ComparisonOperator": "GREATER_THAN",
            "Threshold": 90.0,
            "ThresholdType": "PERCENTAGE"
        },
        "Subscribers": [
            {"SubscriptionType": "EMAIL", "Address": "admin@company.com"},
            {"SubscriptionType": "SNS", "Address": "arn:aws:sns:us-east-1:123456789012:budget-alerts"}
        ]
    }
]

quarterly_budget = aws.create_budget(
    aws_account_id="123456789012",
    budget_name="Q1 2024 Budget",
    budget_amount=15000.0,
    budget_type="COST",
    time_unit="QUARTERLY",
    notifications_with_subscribers=quarterly_notifications
)

# Get budget notifications
alerts = aws.get_budget_notifications(
    aws_account_id="123456789012",
    budget_name="Monthly Production Budget"
)
```

#### Azure Budget Management
Create and manage Azure budgets with notifications:

```python
# List all budgets
budgets = azure.list_budgets(
    scope=f"subscriptions/{subscription_id}"
)

# Create budget with notifications
notifications = {
    "notifications": {
        "actual_80_percent": {
            "enabled": True,
            "operator": "GreaterThan",
            "threshold": 80.0,
            "contact_emails": ["admin@company.com"],
            "contact_roles": ["Owner"],
            "contact_groups": ["/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg/providers/Microsoft.Insights/actionGroups/my-action-group"]
        },
        "actual_90_percent": {
            "enabled": True,
            "operator": "GreaterThan",
            "threshold": 90.0,
            "contact_emails": ["admin@company.com", "finance@company.com"],
            "contact_roles": ["Owner", "Contributor"]
        }
    }
}

# Create monthly budget
monthly_budget = azure.create_budget(
    scope=f"subscriptions/{subscription_id}",
    budget_name="Monthly Azure Budget",
    amount=3000.0,
    time_grain="Monthly",
    notifications=notifications
)

# Create budget with forecast notifications
forecast_notifications = {
    "notifications": {
        "forecast_80_percent": {
            "enabled": True,
            "operator": "GreaterThan",
            "threshold": 80.0,
            "contact_emails": ["admin@company.com"],
            "threshold_type": "Forecasted"
        }
    }
}

forecast_budget = azure.create_budget(
    scope=f"subscriptions/{subscription_id}",
    budget_name="Forecast Budget",
    amount=5000.0,
    time_grain="Monthly",
    notifications=forecast_notifications
)
```

#### GCP Budget Management
Create and manage GCP budgets with notifications:

```python
# List all budgets
budgets = gcp.list_budgets(
    billing_account="billingAccounts/123456-789012-345678"
)

# Create budget with notifications
notifications = {
    "pubsubTopic": "projects/my-project/topics/budget-notifications",
    "schemaVersion": "1.0",
    "monitoringNotificationChannels": [
        "projects/my-project/notificationChannels/123456789"
    ]
}

# Create monthly budget with threshold rules
threshold_rules = [
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
]

monthly_budget = gcp.create_budget(
    billing_account="billingAccounts/123456-789012-345678",
    budget_name="Monthly GCP Budget",
    amount=2000.0,
    threshold_rules=threshold_rules,
    notifications=notifications
)

# Create budget with custom threshold rules
custom_thresholds = [
    {
        "thresholdPercent": 0.25,
        "spendBasis": "FORECASTED_SPEND"
    },
    {
        "thresholdPercent": 0.5,
        "spendBasis": "FORECASTED_SPEND"
    },
    {
        "thresholdPercent": 0.75,
        "spendBasis": "FORECASTED_SPEND"
    },
    {
        "thresholdPercent": 1.0,
        "spendBasis": "FORECASTED_SPEND"
    }
]

forecast_budget = gcp.create_budget(
    billing_account="billingAccounts/123456-789012-345678",
    budget_name="Forecast Budget",
    amount=5000.0,
    threshold_rules=custom_thresholds,
    notifications=notifications
)
```

#### Budget Notification Types

| Provider | Notification Types | Threshold Types | Subscriber Types |
|----------|-------------------|-----------------|------------------|
| **AWS** | `ACTUAL`, `FORECASTED` | `PERCENTAGE`, `ABSOLUTE_VALUE` | `EMAIL`, `SNS` |
| **Azure** | `Actual`, `Forecasted` | `Percentage`, `Absolute` | `Email`, `Action Groups`, `Roles` |
| **GCP** | `CURRENT_SPEND`, `FORECASTED_SPEND` | `Percentage` | `Pub/Sub`, `Monitoring Channels` |

#### Common Budget Patterns

```python
# Pattern 1: Early Warning System
early_warning_notifications = [
    {"threshold": 50.0, "type": "PERCENTAGE", "contacts": ["team@company.com"]},
    {"threshold": 80.0, "type": "PERCENTAGE", "contacts": ["admin@company.com"]},
    {"threshold": 95.0, "type": "PERCENTAGE", "contacts": ["emergency@company.com"]}
]

# Pattern 2: Forecast-Based Alerts
forecast_notifications = [
    {"threshold": 80.0, "type": "FORECASTED", "contacts": ["finance@company.com"]},
    {"threshold": 100.0, "type": "FORECASTED", "contacts": ["admin@company.com"]}
]

# Pattern 3: Multi-Channel Notifications
multi_channel_notifications = [
    {
        "threshold": 90.0,
        "type": "PERCENTAGE",
        "email": ["admin@company.com"],
        "slack": ["#budget-alerts"],
        "sms": ["+1234567890"]
    }
]
```

### 3. Optimization & Recommendations
```python
# Get comprehensive optimization recommendations
optimizations = client.get_optimization_recommendations()

# AWS-specific: Savings Plans recommendations (now accepts flexible parameters)
savings_plans = aws_client.get_savings_plans_recommendations(
    SavingsPlansType="EC2_INSTANCE_SP",
    TermInYears="THREE_YEARS",
    PaymentOption="ALL_UPFRONT",
    AccountScope="LINKED",
    LookbackPeriodInDays="SIXTY_DAYS",
    # ... any other supported params
)

# AWS-specific: Reservation purchase recommendations (now accepts flexible parameters)
reservation_recs = aws_client.get_reservation_purchase_recommendations(
    Service="Amazon Redshift",
    TermInYears="THREE_YEARS",
    PaymentOption="ALL_UPFRONT",
    AccountScope="LINKED",
    LookbackPeriodInDays="SIXTY_DAYS",
    ServiceSpecification={"EC2Specification": {"OfferingClass": "STANDARD"}},
    # ... any other supported params
)

# AWS-specific: Rightsizing recommendations (now accepts flexible parameters)
rightsizing = aws_client.get_rightsizing_recommendations(
    Service="AmazonEC2",
    Configuration={"RecommendationTarget": "SAME_INSTANCE_FAMILY", "BenefitsConsidered": True},
    Filter={
        # ... your filter structure ...
    },
    PageSize=100,
    # ... any other supported params
)

# AWS-specific: Idle resources (now accepts flexible parameters)
idle_resources = aws_client.get_idle_resources(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}],
    MaxResults=50,
    # ... any other supported params
)

# Azure-specific: Advisor recommendations
advisor_recs = azure_client.get_advisor_recommendations()

# GCP-specific: Machine type recommendations
machine_recs = gcp_client.get_machine_type_recommendations()

# GCP-specific: Idle resource recommendations
idle_recs = gcp_client.get_idle_resource_recommendations()
```

### 4. Advanced Analytics
```python
# Cost forecasting (now accepts flexible parameters and has robust defaults)
forecast = client.get_cost_forecast(
    # You can specify TimePeriod, Metric, Granularity, Filter, etc.
    # If not provided, defaults are:
    #   TimePeriod: today to today+30 days
    #   Metric: 'UNBLENDED_COST'
    #   Granularity: 'MONTHLY'
    # Example with all defaults:
)

# Example with custom parameters:
forecast = client.get_cost_forecast(
    TimePeriod={"Start": "2024-07-01", "End": "2024-08-01"},
    Metric="BLENDED_COST",
    Granularity="DAILY",
    Filter={
        # ... your filter structure ...
    }
)

# Cost anomalies (now accepts flexible parameters and has robust defaults)
anomalies = client.get_cost_anomalies(
    # You can specify MonitorArn, DateInterval, Feedback, TotalImpact, etc.
    # If DateInterval is not provided, defaults are:
    #   StartDate: one month prior to today
    #   EndDate: today
    # Example with all defaults:
)

# Example with custom parameters:
anomalies = client.get_cost_anomalies(
    MonitorArn="arn:aws:ce:us-east-1:123456789012:anomalymonitor/your-monitor",
    DateInterval={"StartDate": "2024-06-01", "EndDate": "2024-07-01"},
    Feedback="YES",
    TotalImpact={"NumericOperator": "GREATER_THAN", "StartValue": 200.0},
    MaxResults=50
)

# Cost efficiency metrics (now accepts flexible parameters and has robust defaults)
efficiency = client.get_cost_efficiency_metrics()

# Example with user_count and transaction_count (for cost per user/transaction)
efficiency = client.get_cost_efficiency_metrics(
    user_count=100,
    transaction_count=10000
)

# Example with custom parameters for AWS Cost Explorer (TimePeriod, Granularity, Metrics, GroupBy, Filter, etc.)
efficiency = client.get_cost_efficiency_metrics(
    TimePeriod={"Start": "2024-06-01", "End": "2024-07-01"},
    Granularity="DAILY",
    Metrics=["UnblendedCost", "UsageQuantity"],
    GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    Filter={
        # ... your filter structure ...
    },
    user_count=100,
    transaction_count=10000
)

# Generate comprehensive reports (now accepts flexible parameters and is robust to missing metrics)
report = client.generate_cost_report(
    report_type="monthly",
    # You can specify TimePeriod, Granularity, Metrics, GroupBy, Filter, etc.
    # If not provided, defaults are:
    #   TimePeriod: first of month to today
    #   Granularity: 'MONTHLY'
    #   Metrics: ['UnblendedCost']
    #   GroupBy: [{"Type": "DIMENSION", "Key": "SERVICE"}]
    # The method is robust to missing metrics in the AWS response.
)

# Example with custom parameters for AWS Cost Explorer (TimePeriod, Granularity, Metrics, GroupBy, Filter, etc.)
report = client.generate_cost_report(
    report_type="custom",
    TimePeriod={"Start": "2024-06-01", "End": "2024-07-01"},
    Granularity="DAILY",
    Metrics=["BlendedCost", "UsageQuantity"],
    GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    Filter={
        # ... your filter structure ...
    }
)
```

### Enhanced Cost Trends Analysis
```python
# Get detailed cost trends with analysis
trends = client.get_cost_trends(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="DAILY"
)

# Sample output structure:
{
    "period": {"start": "2024-01-01", "end": "2024-01-31"},
    "granularity": "DAILY",
    "total_periods": 31,
    "total_cost": 1250.75,
    "average_daily_cost": 40.35,
    "trend_direction": "increasing",
    "growth_rate": 15.2,
    "patterns": ["High cost variability", "Weekend cost reduction"],
    "insights": [
        "Total cost over 31 periods: $1250.75",
        "Average cost per period: $40.35",
        "Cost trend is increasing (15.2% change)",
        "Peak cost period: 2024-01-15 to 2024-01-16 ($85.20)"
    ],
    "peak_periods": [
        {"period": "2024-01-15 to 2024-01-16", "cost": 85.20, "date": "2024-01-15"}
    ],
    "cost_periods": [
        {"period": "2024-01-01 to 2024-01-02", "cost": 35.50, "date": "2024-01-01"},
        # ... more periods
    ]
}
```

### 5. Governance & Compliance
```python
# Get governance policies and compliance status
governance = client.get_governance_policies()

# AWS: Cost allocation tags
aws_tags = aws_client.get_cost_allocation_tags()

# Azure: Policy compliance
azure_compliance = azure_client.get_policy_compliance()

# GCP: Cost allocation labels
gcp_labels = gcp_client.get_cost_allocation_labels()
```

### 6. Reservation Management
```python
# Get reservation costs
reservation_costs = client.get_reservation_cost()

# Get reservation recommendations
reservation_recs = client.get_reservation_recommendation()

# Azure-specific: Reservation order details
azure_orders = azure_client.get_reservation_order_details()
```

## 🔧 Provider-Specific Features

### AWS Features
- **Cost Explorer Integration**: Full access to AWS Cost Explorer APIs
- **Budgets API**: Create and manage budgets with notifications
- **Reservations**: Reserved Instance and Savings Plans management
- **Rightsizing**: Instance rightsizing recommendations
- **Cost Anomaly Detection**: Built-in anomaly detection
- **Organizations**: Multi-account cost management
- **Config**: Compliance and policy management

### Azure Features
- **Cost Management API**: Comprehensive cost analysis
- **Budget API**: Azure-native budget management
- **Advisor**: Cost optimization recommendations
- **Policy**: Azure Policy integration for governance
- **Reservations**: Reserved Instance management
- **Cost Anomaly Detection**: Azure-native anomaly detection

### GCP Features
- **Billing API**: GCP billing integration
- **Budget API**: Google Cloud Budgets
- **Recommender API**: Machine learning-based recommendations
- **BigQuery**: Advanced analytics and reporting
- **Resource Manager**: Cost allocation with labels
- **Organization Policy**: Policy compliance management

## 🛠️ Advanced Usage

### Unified Interface
```python
from pycloudmesh import CloudMesh

# Create unified interface
cloudmesh = CloudMesh("aws", access_key="...", secret_key="...", region="us-east-1")

# All methods work the same way regardless of provider
costs = cloudmesh.get_cost_data()
budgets = cloudmesh.list_budgets()
optimizations = cloudmesh.get_optimization_recommendations()
```

### Error Handling
```python
try:
    costs = client.get_cost_data()
except Exception as e:
    print(f"Error fetching cost data: {e}")
    # Handle error appropriately
```

### Caching
```python
# Reservation costs are automatically cached
reservation_costs = client.get_reservation_cost()  # Cached for performance
```

## 📋 Requirements

### Python Version
- Python 3.8+

### Dependencies
- `boto3` (for AWS)
- `requests` (for Azure)
- `google-cloud-billing` (for GCP)
- `google-cloud-recommender` (for GCP)
- `google-cloud-billing-budgets` (for GCP)

### Authentication

#### AWS
```python
# Using access keys
aws = aws_client("ACCESS_KEY", "SECRET_KEY", "us-east-1")

# Or using environment variables
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

#### Azure
```python
# Using service principal token
azure = azure_client("subscription_id", "access_token")

# Or using Azure CLI
az login
# Then use the token from az account get-access-token
```

#### GCP
```python
# Using service account key file
gcp = gcp_client("project_id", "/path/to/service-account-key.json")

# Or using Application Default Credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

## 🧪 Testing

Run the test suite:

```bash
# Test AWS functionality
python tests/test_aws.py

# Test Azure functionality
python tests/test_azure.py

# Test GCP functionality
python tests/test_gcp.py
```

## 📚 Examples

See the `examples/` directory for comprehensive usage examples:

- `aws_finops_example.py`: Complete AWS FinOps workflow
- `azure_finops_example.py`: Complete Azure FinOps workflow
- `gcp_finops_example.py`: Complete GCP FinOps workflow
- `multi_cloud_example.py`: Multi-cloud cost comparison

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` directory
- Review the examples in the `examples/` directory

## 🔄 Roadmap

- [ ] Multi-cloud cost comparison dashboard
- [ ] Automated cost optimization workflows
- [ ] Integration with popular FinOps tools
- [ ] Machine learning-based cost predictions
- [ ] Real-time cost monitoring and alerts
- [ ] Cost allocation automation
- [ ] Compliance reporting templates

