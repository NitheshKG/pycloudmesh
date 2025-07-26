# PyCloudMesh - Comprehensive FinOps Management

PyCloudMesh is a unified Python library for comprehensive Financial Operations (FinOps) management across AWS, Azure, and GCP. It provides a consistent interface for cost optimization, governance, analytics, and resource management across all major cloud providers.

## 🌟 Features

- Real-time cost tracking, analysis, and reporting
- Budget management with alerts
- Reservation and commitment optimization
- Resource optimization recommendations
- Cost forecasting and anomaly detection
- Policy compliance and cost allocation
- Advanced analytics and reporting

## 🚀 Quick Start

### Installation

```bash
pip install pycloudmesh
```

### Basic Usage

![PyCloudMesh](assets/pycloudmesh.gif)

```python
from pycloudmesh import aws_client, azure_client, gcp_client

# AWS Example
aws = aws_client("your_access_key", "your_secret_key", "us-east-1")
costs = aws.get_cost_data(start_date="2024-01-01", end_date="2024-01-31")

# Azure Example
azure = azure_client("your_subscription_id", "your_token")
analysis = azure.get_cost_analysis("/subscriptions/your-subscription-id/", dimensions=["SERVICE", "REGION"])

# GCP Example
gcp = gcp_client("your_project_id", "/path/to/credentials.json")
budgets = gcp.list_budgets(billing_account="your_billing_account")
```

## 📊 Comprehensive FinOps Features

For detailed documentation, see the [docs/provider](docs/provider/) directory.

### 1. Cost Management

**AWS:**  
[ get_cost_data ](docs/provider/aws/README.md#get_cost_data)  
[ get_cost_analysis ](docs/provider/aws/README.md#get_cost_analysis)  
[ get_cost_trends ](docs/provider/aws/README.md#get_cost_trends)  
[ get_resource_costs ](docs/provider/aws/README.md#get_resource_costs)

**Azure:**  
[ get_cost_data ](docs/provider/azure/README.md#get_cost_data)  
[ get_cost_analysis ](docs/provider/azure/README.md#get_cost_analysis)  
[ get_cost_trends ](docs/provider/azure/README.md#get_cost_trends)  
[ get_resource_costs ](docs/provider/azure/README.md#get_resource_costs)

**GCP:**  
[ get_cost_data ](docs/provider/gcp/README.md#get_cost_data)  
[ get_cost_analysis ](docs/provider/gcp/README.md#get_cost_analysis)  
[ get_cost_trends ](docs/provider/gcp/README.md#get_cost_trends)  
[ get_resource_costs ](docs/provider/gcp/README.md#get_resource_costs)

### 2. Budget Management

**AWS:**  
[ list_budgets ](docs/provider/aws/README.md#list_budgets)  
[ create_budget ](docs/provider/aws/README.md#create_budget)  
[ get_budget_notifications ](docs/provider/aws/README.md#get_budget_notifications)

**Azure:**  
[ list_budgets ](docs/provider/azure/README.md#list_budgets)  
[ create_budget ](docs/provider/azure/README.md#create_budget)
[ get_budget ](docs/provider/azure/README.md#get_budget)

**GCP:**  
[ list_budgets ](docs/provider/gcp/README.md#list_budgets)  
[ create_budget ](docs/provider/gcp/README.md#create_budget)  
[ get_budget_alerts ](docs/provider/gcp/README.md#get_budget_alerts)

### 3. Optimization & Recommendations

**AWS:**  
[ get_optimization_recommendations ](docs/provider/aws/README.md#get_optimization_recommendations)  
[ get_savings_plans_recommendations ](docs/provider/aws/README.md#get_savings_plans_recommendations)  
[ get_reservation_purchase_recommendations ](docs/provider/aws/README.md#get_reservation_purchase_recommendations)  
[ get_rightsizing_recommendations ](docs/provider/aws/README.md#get_rightsizing_recommendations)  
[ get_idle_resources ](docs/provider/aws/README.md#get_idle_resources)

**Azure:**  
[ get_advisor_recommendations ](docs/provider/azure/README.md#get_advisor_recommendations)
[ get_optimization_recommendations ](docs/provider/azure/README.md#get_optimization_recommendations)  
[ get_reserved_instance_recommendations ](docs/provider/azure/README.md#get_reserved_instance_recommendations)

**GCP:**  
[ get_machine_type_recommendations ](docs/provider/gcp/README.md#get_machine_type_recommendations)  
[ get_idle_resource_recommendations ](docs/provider/gcp/README.md#get_idle_resource_recommendations)

### 4. Advanced Analytics

**All Providers:**  
[ get_cost_forecast ](docs/provider/aws/README.md#get_cost_forecast)  
[ get_cost_anomalies ](docs/provider/aws/README.md#get_cost_anomalies)  
[ get_cost_efficiency_metrics ](docs/provider/aws/README.md#get_cost_efficiency_metrics)  
[ generate_cost_report ](docs/provider/aws/README.md#generate_cost_report)

### 5. Governance & Compliance

**AWS:**  
[ get_governance_policies ](docs/provider/aws/README.md#get_governance_policies)  

**Azure:**  
[ get_governance_policies ](docs/provider/azure/README.md#get_governance_policies)

**GCP:**  
[ get_governance_policies ](docs/provider/gcp/README.md#get_governance_policies)

### 6. Reservation Management

**AWS:**  
[ get_reservation_cost ](docs/provider/aws/README.md#get_reservation_cost)  
[ get_reservation_purchase_recommendation ](docs/provider/aws/README.md#get_reservation_purchase_recommendation)  
[ get_reservation_coverage ](docs/provider/aws/README.md#get_reservation_coverage)

**Azure:**  
[ get_reservation_order_details ](docs/provider/azure/README.md#get_reservation_order_details)

**GCP:** *(Beta)*  
[ get_reservation_cost ](docs/provider/gcp/README.md#get_reservation_cost)  
[ get_reservation_recommendation ](docs/provider/gcp/README.md#get_reservation_recommendation)

---

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
- **Cost Management API**: Comprehensive cost analysis with scope-based queries
- **Budget API**: Azure-native budget management
- **Advisor**: Cost optimization recommendations
- **Policy**: Azure Policy integration for governance
- **Reservations**: Reserved Instance management
- **Cost Anomaly Detection**: Azure-native anomaly detection

### GCP Features
- **Billing API**: GCP billing integration with BigQuery export
- **Budget API**: Google Cloud Budgets with real-time monitoring
- **Recommender API**: Machine learning-based optimization recommendations
- **BigQuery ML**: Advanced cost forecasting and anomaly detection
- **Resource Manager**: Cost allocation with labels and tags
- **Organization Policy**: Policy compliance management and enforcement
- **Asset API**: Resource inventory and compliance checking
- **Advanced Analytics**: ML-powered cost efficiency metrics

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
- `google-cloud-asset` (for GCP governance)
- `google-cloud-org-policy` (for GCP policy compliance)
- `google-cloud-resource-manager` (for GCP cost allocation)
- `google-cloud-bigquery` (for GCP advanced analytics)

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

#### AWS IAM Policies

To use PyCloudMesh with AWS, you'll need to attach the following IAM policies to your user or role:

**Cost Explorer Policy (CEPolicy):**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetCostForecast",
                "ce:GetDimensionValues",
                "ce:GetReservationUtilization",
                "ce:GetRightsizingRecommendation",
                "ce:GetSavingsPlansPurchaseRecommendation",
                "ce:GetReservationPurchaseRecommendation",
                "ce:GetAnomalies",
                "ce:GetReservationCoverage"
            ],
            "Resource": "*"
        }
    ]
}
```

**Organizations Policy (OrgPolicy):**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "organizations:ListTagsForResource",
            "Resource": "*"
        }
    ]
}
```

**Config Policy (ConfPolicy):**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "config:GetComplianceDetailsByConfigRule",
                "config:PutConfigRule",
                "config:DescribeConfigRules"
            ],
            "Resource": "*"
        }
    ]
}
```

#### Azure
```python
# Using service principal token
azure = azure_client("subscription_id", "access_token")

# Or using Azure CLI
az login
# Then use the token from az account get-access-token
```

**Azure Scopes:**
Azure cost management methods require a scope parameter to specify the level at which to query costs:

- **Subscription scope**: `/subscriptions/{subscription-id}/`
- **Resource Group scope**: `/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/`
- **Billing Account scope**: `/providers/Microsoft.Billing/billingAccounts/{billing-account-id}`
- **Management Group scope**: `/providers/Microsoft.Management/managementGroups/{management-group-id}/`

Example:
```python
# Query costs at subscription level
costs = azure.get_cost_data("/subscriptions/your-subscription-id/")

# Query costs at resource group level
costs = azure.get_cost_data("/subscriptions/your-subscription-id/resourceGroups/your-rg/")
```

#### GCP
```python
# Using service account key file
gcp = gcp_client("project_id", "/path/to/service-account-key.json")

# Or using Application Default Credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

#### GCP IAM Permissions

To use PyCloudMesh with GCP, your service account needs the following roles:

**Basic Cost Management:**
- `roles/billing.viewer` - View billing information
- `roles/bigquery.user` - Access BigQuery billing export
- `roles/recommender.viewer` - View optimization recommendations

**Advanced Governance (Optional):**
- `roles/cloudasset.viewer` - View resource inventory for compliance
- `roles/orgpolicy.policyViewer` - View organization policies
- `roles/resourcemanager.projectIamAdmin` - Manage project labels

**Example Service Account Setup:**
```bash
# Grant basic roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL" \
    --role="roles/billing.viewer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL" \
    --role="roles/bigquery.user"

# Grant advanced governance roles (optional)
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL" \
    --role="roles/cloudasset.viewer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL" \
    --role="roles/orgpolicy.policyViewer"
```

## 🧪 Testing

Run the test suite:

```bash
For detailed API documentation and examples, see the [docs/provider](docs/provider/) directory for each p`bash
# Test AWS functionality
python tests/test_aws.py

# Test Azure functionality
python tests/test_azure.py

# Test GCP functionality
python tests/test_gcp.py
```provider.

## 📚 Examples

See the `examples/` directory for comprehensive usage examples.

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

- [x] Machine learning-based cost predictions (GCP BigQuery ML)
- [x] Cost allocation automation (GCP labels and tags)
- [x] Compliance reporting templates (GCP governance policies)
- [x] Real-time cost monitoring and alerts (GCP budget alerts)
- [ ] Multi-cloud cost comparison dashboard
- [ ] Automated cost optimization workflows
- [ ] Integration with popular FinOps tools
- [ ] Enhanced AWS and Azure governance features

