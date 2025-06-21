#!/usr/bin/env python3
"""
Comprehensive FinOps Example for PyCloudMesh

This example demonstrates all the FinOps features available in PyCloudMesh
across AWS, Azure, and GCP providers.
"""

import os
from datetime import datetime, timedelta
from pycloudmesh import aws_client, azure_client, gcp_client, CloudMesh


def aws_finops_demo():
    """Demonstrate comprehensive AWS FinOps features."""
    print("🚀 AWS FinOps Demo")
    print("=" * 50)
    
    # Initialize AWS client
    aws = aws_client(
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    
    # 1. Cost Management
    print("\n📊 Cost Management:")
    print("-" * 30)
    
    # Get cost data
    costs = aws.get_cost_data(
        start_date="2024-01-01",
        end_date="2024-01-31",
        granularity="MONTHLY"
    )
    print(f"Cost data retrieved: {len(costs)} records")
    
    # Cost analysis
    analysis = aws.get_cost_analysis(
        start_date="2024-01-01",
        end_date="2024-01-31",
        dimensions=["SERVICE", "REGION"]
    )
    print(f"Cost analysis completed with {len(analysis)} dimensions")
    
    # Cost trends
    trends = aws.get_cost_trends(
        start_date="2024-01-01",
        end_date="2024-01-31",
        granularity="DAILY"
    )
    print(f"Cost trends analyzed: {len(trends)} data points")
    
    # 2. Budget Management
    print("\n💰 Budget Management:")
    print("-" * 30)
    
    # List budgets
    budgets = aws.list_budgets(aws_account_id=os.getenv("AWS_ACCOUNT_ID"))
    print(f"Found {len(budgets.get('Budgets', []))} budgets")
    
    # Create budget (commented out to avoid actual creation)
    # budget = aws.create_budget(
    #     aws_account_id=os.getenv("AWS_ACCOUNT_ID"),
    #     budget_name="Demo Budget",
    #     budget_amount=1000.0,
    #     budget_type="COST",
    #     time_unit="MONTHLY"
    # )
    # print("Budget created successfully")
    
    # 3. Optimization & Recommendations
    print("\n🔧 Optimization & Recommendations:")
    print("-" * 30)
    
    # Get comprehensive optimization recommendations
    optimizations = aws.get_optimization_recommendations()
    print("Optimization recommendations retrieved")
    
    # AWS-specific optimizations
    savings_plans = aws.get_savings_plans_recommendations()
    print("Savings Plans recommendations retrieved")
    
    rightsizing = aws.get_rightsizing_recommendations()
    print("Rightsizing recommendations retrieved")
    
    idle_resources = aws.get_idle_resources()
    print(f"Found {idle_resources.get('total_idle_count', 0)} idle resources")
    
    # 4. Advanced Analytics
    print("\n📈 Advanced Analytics:")
    print("-" * 30)
    
    # Cost forecasting
    forecast = aws.get_cost_forecast(
        start_date="2024-01-01",
        end_date="2024-01-31",
        forecast_period=12
    )
    print("Cost forecast generated")
    
    # Cost anomalies
    anomalies = aws.get_cost_anomalies()
    print(f"Found {len(anomalies.get('anomalies', []))} cost anomalies")
    
    # Efficiency metrics
    efficiency = aws.get_cost_efficiency_metrics()
    print("Cost efficiency metrics calculated")
    
    # Generate report
    report = aws.generate_cost_report(
        report_type="monthly",
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    print("Cost report generated")
    
    # 5. Governance & Compliance
    print("\n🛡️ Governance & Compliance:")
    print("-" * 30)
    
    governance = aws.get_governance_policies()
    print("Governance policies retrieved")
    
    # 6. Reservation Management
    print("\n📋 Reservation Management:")
    print("-" * 30)
    
    reservation_costs = aws.get_reservation_cost()
    print("Reservation costs retrieved")
    
    reservation_recs = aws.get_reservation_recommendation()
    print(f"Found {len(reservation_recs)} reservation recommendations")


def azure_finops_demo():
    """Demonstrate comprehensive Azure FinOps features."""
    print("\n🚀 Azure FinOps Demo")
    print("=" * 50)
    
    # Initialize Azure client
    azure = azure_client(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        token=os.getenv("AZURE_TOKEN")
    )
    
    # 1. Cost Management
    print("\n📊 Cost Management:")
    print("-" * 30)
    
    # Get cost data
    costs = azure.get_cost_data(
        start_date="2024-01-01",
        end_date="2024-01-31",
        granularity="Monthly"
    )
    print("Cost data retrieved")
    
    # Cost analysis
    analysis = azure.get_cost_analysis(
        start_date="2024-01-01",
        end_date="2024-01-31",
        dimensions=["ResourceType", "ResourceLocation"]
    )
    print("Cost analysis completed")
    
    # Cost trends
    trends = azure.get_cost_trends(
        start_date="2024-01-01",
        end_date="2024-01-31",
        granularity="Daily"
    )
    print("Cost trends analyzed")
    
    # 2. Budget Management
    print("\n💰 Budget Management:")
    print("-" * 30)
    
    # List budgets
    budgets = azure.list_budgets(
        scope=f"subscriptions/{os.getenv('AZURE_SUBSCRIPTION_ID')}"
    )
    print("Budgets listed")
    
    # 3. Optimization & Recommendations
    print("\n🔧 Optimization & Recommendations:")
    print("-" * 30)
    
    # Get comprehensive optimization recommendations
    optimizations = azure.get_optimization_recommendations()
    print("Optimization recommendations retrieved")
    
    # Azure-specific optimizations
    advisor_recs = azure.get_advisor_recommendations()
    print("Azure Advisor recommendations retrieved")
    
    # 4. Advanced Analytics
    print("\n📈 Advanced Analytics:")
    print("-" * 30)
    
    # Cost forecasting
    forecast = azure.get_cost_forecast(
        start_date="2024-01-01",
        end_date="2024-01-31",
        forecast_period=12
    )
    print("Cost forecast generated")
    
    # Cost anomalies
    anomalies = azure.get_cost_anomalies()
    print("Cost anomalies detected")
    
    # Efficiency metrics
    efficiency = azure.get_cost_efficiency_metrics()
    print("Cost efficiency metrics calculated")
    
    # Generate report
    report = azure.generate_cost_report(
        report_type="monthly",
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    print("Cost report generated")
    
    # 5. Governance & Compliance
    print("\n🛡️ Governance & Compliance:")
    print("-" * 30)
    
    governance = azure.get_governance_policies()
    print("Governance policies retrieved")
    
    # 6. Reservation Management
    print("\n📋 Reservation Management:")
    print("-" * 30)
    
    reservation_costs = azure.get_reservation_cost()
    print("Reservation costs retrieved")
    
    reservation_recs = azure.get_reservation_recommendation(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID")
    )
    print("Reservation recommendations retrieved")
    
    # Azure-specific reservation details
    reservation_orders = azure.get_reservation_order_details()
    print("Reservation order details retrieved")


def gcp_finops_demo():
    """Demonstrate comprehensive GCP FinOps features."""
    print("\n🚀 GCP FinOps Demo")
    print("=" * 50)
    
    # Initialize GCP client
    gcp = gcp_client(
        project_id=os.getenv("GCP_PROJECT_ID"),
        credentials_path=os.getenv("GCP_CREDENTIALS_PATH")
    )
    
    # 1. Cost Management
    print("\n📊 Cost Management:")
    print("-" * 30)
    
    # Get cost data
    costs = gcp.get_cost_data(
        start_date="2024-01-01",
        end_date="2024-01-31",
        granularity="Monthly"
    )
    print("Cost data retrieved")
    
    # Cost analysis
    analysis = gcp.get_cost_analysis(
        start_date="2024-01-01",
        end_date="2024-01-31",
        dimensions=["service", "location"]
    )
    print("Cost analysis completed")
    
    # Cost trends
    trends = gcp.get_cost_trends(
        start_date="2024-01-01",
        end_date="2024-01-31",
        granularity="Daily"
    )
    print("Cost trends analyzed")
    
    # 2. Budget Management
    print("\n💰 Budget Management:")
    print("-" * 30)
    
    # List budgets
    budgets = gcp.list_budgets(
        billing_account=os.getenv("GCP_BILLING_ACCOUNT")
    )
    print("Budgets listed")
    
    # 3. Optimization & Recommendations
    print("\n🔧 Optimization & Recommendations:")
    print("-" * 30)
    
    # Get comprehensive optimization recommendations
    optimizations = gcp.get_optimization_recommendations()
    print("Optimization recommendations retrieved")
    
    # GCP-specific optimizations
    machine_recs = gcp.get_machine_type_recommendations()
    print("Machine type recommendations retrieved")
    
    idle_recs = gcp.get_idle_resource_recommendations()
    print("Idle resource recommendations retrieved")
    
    # 4. Advanced Analytics
    print("\n📈 Advanced Analytics:")
    print("-" * 30)
    
    # Cost forecasting
    forecast = gcp.get_cost_forecast(
        start_date="2024-01-01",
        end_date="2024-01-31",
        forecast_period=12
    )
    print("Cost forecast generated")
    
    # Cost anomalies
    anomalies = gcp.get_cost_anomalies()
    print("Cost anomalies detected")
    
    # Efficiency metrics
    efficiency = gcp.get_cost_efficiency_metrics()
    print("Cost efficiency metrics calculated")
    
    # Generate report
    report = gcp.generate_cost_report(
        report_type="monthly",
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    print("Cost report generated")
    
    # 5. Governance & Compliance
    print("\n🛡️ Governance & Compliance:")
    print("-" * 30)
    
    governance = gcp.get_governance_policies()
    print("Governance policies retrieved")
    
    # 6. Reservation Management
    print("\n📋 Reservation Management:")
    print("-" * 30)
    
    reservation_costs = gcp.get_reservation_cost()
    print("Reservation costs retrieved")
    
    reservation_recs = gcp.get_reservation_recommendation()
    print("Reservation recommendations retrieved")


def unified_interface_demo():
    """Demonstrate the unified CloudMesh interface."""
    print("\n🚀 Unified CloudMesh Interface Demo")
    print("=" * 50)
    
    # AWS CloudMesh
    print("\n📊 AWS CloudMesh:")
    print("-" * 30)
    aws_mesh = CloudMesh(
        "aws",
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    
    # All methods work the same way
    costs = aws_mesh.get_cost_data(
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    print("AWS cost data retrieved via unified interface")
    
    optimizations = aws_mesh.get_optimization_recommendations()
    print("AWS optimization recommendations retrieved via unified interface")
    
    # Azure CloudMesh
    print("\n📊 Azure CloudMesh:")
    print("-" * 30)
    azure_mesh = CloudMesh(
        "azure",
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        token=os.getenv("AZURE_TOKEN")
    )
    
    costs = azure_mesh.get_cost_data(
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    print("Azure cost data retrieved via unified interface")
    
    optimizations = azure_mesh.get_optimization_recommendations()
    print("Azure optimization recommendations retrieved via unified interface")
    
    # GCP CloudMesh
    print("\n📊 GCP CloudMesh:")
    print("-" * 30)
    gcp_mesh = CloudMesh(
        "gcp",
        project_id=os.getenv("GCP_PROJECT_ID"),
        credentials_path=os.getenv("GCP_CREDENTIALS_PATH")
    )
    
    costs = gcp_mesh.get_cost_data(
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    print("GCP cost data retrieved via unified interface")
    
    optimizations = gcp_mesh.get_optimization_recommendations()
    print("GCP optimization recommendations retrieved via unified interface")


def main():
    """Run the comprehensive FinOps demo."""
    print("🌟 PyCloudMesh Comprehensive FinOps Demo")
    print("=" * 60)
    print("This demo showcases all FinOps features across AWS, Azure, and GCP")
    print("=" * 60)
    
    # Check environment variables
    required_vars = {
        "AWS": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        "Azure": ["AZURE_SUBSCRIPTION_ID", "AZURE_TOKEN"],
        "GCP": ["GCP_PROJECT_ID", "GCP_CREDENTIALS_PATH"]
    }
    
    for provider, vars in required_vars.items():
        missing = [var for var in vars if not os.getenv(var)]
        if missing:
            print(f"⚠️  Missing {provider} environment variables: {missing}")
            print(f"   Skipping {provider} demo...")
        else:
            print(f"✅ {provider} environment variables found")
    
    # Run demos based on available credentials
    if all(os.getenv(var) for var in required_vars["AWS"]):
        aws_finops_demo()
    
    if all(os.getenv(var) for var in required_vars["Azure"]):
        azure_finops_demo()
    
    if all(os.getenv(var) for var in required_vars["GCP"]):
        gcp_finops_demo()
    
    # Unified interface demo (requires at least one provider)
    if any(all(os.getenv(var) for var in vars) for vars in required_vars.values()):
        unified_interface_demo()
    
    print("\n🎉 Comprehensive FinOps Demo Complete!")
    print("=" * 60)
    print("All FinOps features have been demonstrated:")
    print("✅ Cost Management")
    print("✅ Budget Management")
    print("✅ Optimization & Recommendations")
    print("✅ Advanced Analytics")
    print("✅ Governance & Compliance")
    print("✅ Reservation Management")
    print("✅ Unified Interface")


if __name__ == "__main__":
    main() 