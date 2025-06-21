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
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["ResourceType", "ResourceLocation"]
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
```python
# Get detailed cost data
costs = client.get_cost_data(
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="Daily",
    group_by=["SERVICE", "REGION"]
)

# Cost analysis by dimensions
analysis = client.get_cost_analysis(
    dimensions=["SERVICE", "USAGE_TYPE", "REGION"]
)

# Cost trends over time
trends = client.get_cost_trends(granularity="Daily")

# Resource-specific costs
resource_costs = client.get_resource_costs("i-1234567890abcdef0")
```

### 2. Budget Management
```python
# List all budgets
budgets = client.list_budgets()

# Create new budget
new_budget = client.create_budget(
    budget_name="Q1 Budget",
    budget_amount=5000.0,
    time_unit="QUARTERLY"
)

# Get budget alerts
alerts = client.get_budget_notifications(budget_name="Q1 Budget")
```

### 3. Optimization & Recommendations
```python
# Get comprehensive optimization recommendations
optimizations = client.get_optimization_recommendations()

# AWS-specific: Savings Plans recommendations
savings_plans = aws_client.get_savings_plans_recommendations()

# AWS-specific: Rightsizing recommendations
rightsizing = aws_client.get_rightsizing_recommendations()

# AWS-specific: Idle resources
idle_resources = aws_client.get_idle_resources()

# Azure-specific: Advisor recommendations
advisor_recs = azure_client.get_advisor_recommendations()

# GCP-specific: Machine type recommendations
machine_recs = gcp_client.get_machine_type_recommendations()

# GCP-specific: Idle resource recommendations
idle_recs = gcp_client.get_idle_resource_recommendations()
```

### 4. Advanced Analytics
```python
# Cost forecasting
forecast = client.get_cost_forecast(
    start_date="2024-01-01",
    end_date="2024-01-31",
    forecast_period=12
)

# Cost anomalies
anomalies = client.get_cost_anomalies()

# Cost efficiency metrics
efficiency = client.get_cost_efficiency_metrics()

# Generate comprehensive reports
report = client.generate_cost_report(
    report_type="monthly",
    start_date="2024-01-01",
    end_date="2024-01-31"
)
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

