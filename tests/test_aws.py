#!/usr/bin/env python3
"""
Test file for AWS cloud functionality.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from pycloudmesh import aws_client

# Load environment variables from .env file
load_dotenv()

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION = os.getenv("AWS_REGION")
ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")

# Budget config
BUDGET_NAME = "TestBudget-PyCloudMesh"
BUDGET_AMOUNT = 1.0  # USD

# Initialize AWS client
client = aws_client(
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    region=REGION
)


def test_aws_client_creation():
    """Test AWS client creation."""
    try:
        # Test with dummy credentials
        aws = aws_client("dummy_key", "dummy_secret", "us-east-1")
        print("✅ AWS client created successfully")
        return True
    except Exception as e:
        print(f"❌ AWS client creation failed: {e}")
        return False


def test_aws_methods():
    """Test that AWS client has required methods."""
    try:
        aws = aws_client("dummy_key", "dummy_secret", "us-east-1")

        required_methods = [
            'list_budgets',
            'get_cost_data',
            'get_reservation_cost',
            'get_reservation_recommendation',
            'get_cost_analysis',
            'get_cost_trends',
            'get_resource_costs'
        ]

        for method in required_methods:
            if hasattr(aws, method):
                print(f"✅ AWS client has {method} method")
            else:
                print(f"❌ AWS client missing {method} method")
                return False

        return True
    except Exception as e:
        print(f"❌ AWS methods test failed: {e}")
        return False


def test_aws_create_budget():
    """Test AWS budget functionality."""
    try:
        # Initialize AWS client
        aws = aws_client(
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            region=REGION
        )


        notifications = [{
            "Notification": {
                "NotificationType": "ACTUAL",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 90.0,
                "ThresholdType": "PERCENTAGE"
            },
            "Subscribers": [
                {
                    "SubscriptionType": "EMAIL",
                    "Address": "nitheshkg18@gmail.com"
                }
            ]
        }]
        # Create budget
        result = aws.create_budget(
            aws_account_id=ACCOUNT_ID,
            budget_name=BUDGET_NAME,
            budget_amount=BUDGET_AMOUNT,
            budget_type="COST",
            time_unit="MONTHLY",
            notifications_with_subscribers=notifications
        )

        print(result)
        return True
    except Exception as e:
        print(f"❌ AWS budget test failed: {e}")
        return False


def test_aws_list_budgets():
    """Test listing all budgets."""
    try:
        # Initialize AWS client
        aws = aws_client(
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            region=REGION
        )

        # List all budgets
        budgets = aws.list_budgets(aws_account_id=ACCOUNT_ID)
        print("\n--- Listing all budgets ---")
        print(budgets)
        return True
    except Exception as e:
        print(f"❌ AWS list budgets test failed: {e}")
        return False


def test_aws_create_quarterly_budget():
    """Test creating a new quarterly budget with 80% threshold and email notification."""
    try:
        aws = aws_client(
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            region=REGION
        )
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
                    "Address": "nitheshkg18@gmail.com"
                }
            ]
        }]
        new_budget = aws.create_budget(
            aws_account_id=ACCOUNT_ID,
            budget_name="Q1 Budget",
            budget_amount=5000.0,
            time_unit="QUARTERLY",
            notifications_with_subscribers=notifications
        )
        print("\n--- Creating new quarterly budget with 80% threshold and email notification ---")
        print(new_budget)
        return True
    except Exception as e:
        print(f"❌ AWS create quarterly budget test failed: {e}")
        return False


def test_aws_get_budget_notifications():
    """Test getting budget notifications."""
    try:
        # Initialize AWS client
        aws = aws_client(
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            region=REGION
        )

        # Get budget alerts for 'Q1 Budget'
        alerts = aws.get_budget_notifications(
            aws_account_id=ACCOUNT_ID,
            budget_name="Q1 Budget"
        )
        print("\n--- Getting budget notifications for 'Q1 Budget' ---")
        print(alerts)
        return True
    except Exception as e:
        print(f"❌ AWS get budget notifications test failed: {e}")
        return False


def test_aws_get_cost_data():
    """Test the get cost data"""
    try:
        aws = client
        cost_data = aws.get_cost_data(
            start_date="2025-03-01",
            end_date="2025-05-31",
            granularity="DAILY",
            group_by=[{"Type": "DIMENSION", "Key": "SERVICE"}, {"Type": "DIMENSION", "Key": "REGION"}]
        )
        print(cost_data)
        return True
    except Exception as e:
        print(f"❌ AWS get cost data test failed: {e}")
        return False
    

def test_aws_get_cost_analysis():
    """Test the get cost analysis with proper parameters."""
    try:
        aws = client
        cost_analysis = aws.get_cost_analysis(
            start_date="2025-03-01",
            end_date="2025-05-31",
            dimensions=["SERVICE", "REGION"]
        )
        print("\n--- Cost Analysis Results ---")
        print(f"Analysis period: 2025-03-01 to 2025-05-31")
        print(f"Dimensions: SERVICE, REGION")
        
        if "error" in cost_analysis:
            print(f"Error: {cost_analysis['error']}")
        else:
            print(f"Total Cost: ${cost_analysis.get('total_cost', 0):.2f}")
            print(f"Top Services:")
            for service in cost_analysis.get('top_services', [])[:3]:
                print(f"  - {service['service']}: ${service['cost']:.2f}")
            print(f"Insights:")
            for insight in cost_analysis.get('insights', []):
                print(f"  - {insight}")
            print(f"Cost Trends: {len(cost_analysis.get('cost_trends', []))} periods analyzed")
        
        print(cost_analysis)
        return True
    except Exception as e:
        print(f"❌ AWS get cost analysis test failed: {e}")
        return False


def test_aws_get_cost_trends():
    """Test the get cost trends with proper parameters."""
    try:
        aws = client
        cost_trends = aws.get_cost_trends(
            start_date="2025-03-01",
            end_date="2025-05-31",
            granularity="DAILY"
        )
        print("\n--- Cost Trends Analysis Results ---")
        print(f"Trends period: 2025-03-01 to 2025-05-31")
        print(f"Granularity: DAILY")
        
        if "error" in cost_trends:
            print(f"Error: {cost_trends['error']}")
        else:
            print(f"Total Periods: {cost_trends.get('total_periods', 0)}")
            print(f"Total Cost: ${cost_trends.get('total_cost', 0):.4f}")
            print(f"Average Cost per Period: ${cost_trends.get('average_daily_cost', 0):.4f}")
            print(f"Trend Direction: {cost_trends.get('trend_direction', 'unknown')}")
            print(f"Growth Rate: {cost_trends.get('growth_rate', 0):.1f}%")
            
            print(f"\nPatterns Detected:")
            for pattern in cost_trends.get('patterns', []):
                print(f"  - {pattern}")
            
            print(f"\nInsights:")
            for insight in cost_trends.get('insights', []):
                print(f"  - {insight}")
            
            print(f"\nPeak Periods:")
            for peak in cost_trends.get('peak_periods', [])[:3]:
                print(f"  - {peak['period']}: ${peak['cost']:.4f}")
            
            print(f"\nCost Periods (first 5):")
            for period in cost_trends.get('cost_periods', [])[:5]:
                print(f"  - {period['period']}: ${period['cost']:.4f}")
        
        print(f"\nFull trends analysis structure:")
        print(cost_trends)
        return True
    except Exception as e:
        print(f"❌ AWS get cost trends test failed: {e}")
        return False


def test_aws_get_resource_costs():
    """Test the get resource costs with a specific instance ID."""
    try:
        aws = client
        resource_costs = aws.get_resource_costs(
            resource_id="i-0df615a5315c31029",
            start_date="2025-03-01",
            end_date="2025-05-31",
            granularity="DAILY"
        )
        print("\n--- Resource Costs Analysis Results ---")
        print(f"Resource ID: i-0df615a5315c31029")
        print(f"Period: 2025-03-01 to 2025-05-31")
        print(f"Granularity: DAILY")
        
        if "error" in resource_costs:
            print(f"Error: {resource_costs['error']}")
        else:
            print(f"Total Cost: ${resource_costs.get('total_cost', 0):.4f}")
            print(f"Total Periods: {resource_costs.get('total_periods', 0)}")
            print(f"Active Periods: {resource_costs.get('active_periods', 0)}")
            
            # Show cost breakdown
            print(f"\nCost Breakdown:")
            for service, cost in resource_costs.get('cost_breakdown', {}).items():
                print(f"  - {service}: ${cost:.4f}")
            
            # Show utilization insights
            print(f"\nUtilization Insights:")
            for insight in resource_costs.get('utilization_insights', []):
                print(f"  - {insight}")
            
            # Show cost trends
            print(f"\nCost Trends:")
            for trend in resource_costs.get('cost_trends', []):
                print(f"  - {trend}")
            
            # Show recommendations
            print(f"\nRecommendations:")
            for rec in resource_costs.get('recommendations', []):
                print(f"  - {rec}")
            
            # Show cost periods (first 5)
            print(f"\nCost Periods (first 5):")
            for period in resource_costs.get('cost_periods', [])[:5]:
                print(f"  - {period['period']}: ${period['cost']:.4f}")
                if period.get('breakdown'):
                    for service, cost in period['breakdown'].items():
                        print(f"    * {service}: ${cost:.4f}")
        
        print(f"\nFull resource analysis structure:")
        print(resource_costs)
        return True
    except Exception as e:
        print(f"❌ AWS get resource costs test failed: {e}")
        return False

# <------------------- 3 Optimisations and Recommendations ---------------------->
def test_aws_get_optimization_recommendations():
    """Test the get optimization recommendations with comprehensive analysis."""
    try:
        aws = client
        optimization_recs = aws.get_optimization_recommendations()
        print("\n--- Optimization Recommendations Analysis Results ---")
        
        if "error" in optimization_recs:
            print(f"Error: {optimization_recs['error']}")
        else:
            # Check for each optimization category
            print(f"Optimization Categories Found:")
            
            # Reservations
            reservations = optimization_recs.get('reservations', {})
            if "error" in reservations:
                print(f"  - Reservations: Error - {reservations['error']}")
            else:
                rec_count = len(reservations.get('Recommendations', []))
                print(f"  - Reservations: {rec_count} recommendations found")
                if rec_count > 0:
                    print(f"    * Sample: {reservations['Recommendations'][0].get('RecommendationDetails', {}).get('TargetInstances', [])[:2]}")
            
            # Savings Plans
            savings_plans = optimization_recs.get('savings_plans', {})
            if "error" in savings_plans:
                print(f"  - Savings Plans: Error - {savings_plans['error']}")
            else:
                rec_count = len(savings_plans.get('SavingsPlansRecommendation', []))
                print(f"  - Savings Plans: {rec_count} recommendations found")
                if rec_count > 0:
                    print(f"    * Sample: {savings_plans['SavingsPlansRecommendation'][0].get('SavingsPlansRecommendationDetails', {}).get('EstimatedSavingsAmount', 'N/A')}")
            
            # Rightsizing
            rightsizing = optimization_recs.get('rightsizing', {})
            if "error" in rightsizing:
                print(f"  - Rightsizing: Error - {rightsizing['error']}")
            else:
                rec_count = len(rightsizing.get('RightsizingRecommendations', []))
                print(f"  - Rightsizing: {rec_count} recommendations found")
                if rec_count > 0:
                    print(f"    * Sample: {rightsizing['RightsizingRecommendations'][0].get('AccountId', 'N/A')}")
            
            # Idle Resources
            idle_resources = optimization_recs.get('idle_resources', {})
            if "error" in idle_resources:
                print(f"  - Idle Resources: Error - {idle_resources['error']}")
            else:
                idle_count = idle_resources.get('total_idle_count', 0)
                print(f"  - Idle Resources: {idle_count} idle resources found")
                if idle_count > 0:
                    sample_resources = idle_resources.get('idle_resources', [])[:3]
                    print(f"    * Sample resources:")
                    for resource in sample_resources:
                        print(f"      - {resource.get('resource_id', 'N/A')} ({resource.get('instance_type', 'N/A')})")
            
            # Summary
            total_recommendations = (
                len(reservations.get('Recommendations', [])) +
                len(savings_plans.get('SavingsPlansRecommendation', [])) +
                len(rightsizing.get('RightsizingRecommendations', [])) +
                idle_resources.get('total_idle_count', 0)
            )
            print(f"\nTotal Optimization Opportunities: {total_recommendations}")
            
            # Insights
            print(f"\nOptimization Insights:")
            if total_recommendations > 0:
                print(f"  - Found {total_recommendations} potential cost optimization opportunities")
                if idle_resources.get('total_idle_count', 0) > 0:
                    print(f"  - {idle_resources['total_idle_count']} idle resources detected - consider stopping or downsizing")
                if len(reservations.get('Recommendations', [])) > 0:
                    print(f"  - {len(reservations['Recommendations'])} reservation opportunities available")
                if len(savings_plans.get('SavingsPlansRecommendation', [])) > 0:
                    print(f"  - {len(savings_plans['SavingsPlansRecommendation'])} Savings Plans opportunities available")
                if len(rightsizing.get('RightsizingRecommendations', [])) > 0:
                    print(f"  - {len(rightsizing['RightsizingRecommendations'])} rightsizing opportunities available")
            else:
                print(f"  - No immediate optimization opportunities detected")
                print(f"  - This could indicate good cost optimization practices or limited usage data")
        
        print(f"\nFull optimization recommendations structure:")
        print(optimization_recs)
        return True
    except Exception as e:
        print(f"❌ AWS get optimization recommendations test failed: {e}")
        return False

# def test_





def main():
    """Run AWS tests."""
    print("Testing AWS Functionality")
    print("=" * 30)
    
    tests = [
        # test_aws_client_creation,
        #  test_aws_methods,
         test_aws_create_budget,
        #  test_aws_list_budgets,
        #  test_aws_create_quarterly_budget,
        #  test_aws_get_budget_notifications,
        # test_aws_get_cost_data,
        # test_aws_get_cost_analysis,
        # test_aws_get_cost_trends,
        # test_aws_get_resource_costs,
        # test_aws_get_optimization_recommendations
    ]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
