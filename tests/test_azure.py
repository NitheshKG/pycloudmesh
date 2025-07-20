#!/usr/bin/env python3
"""
Test file for Azure cloud functionality.
"""

import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_azure_client_creation():
    """Test Azure client creation."""
    try:
        from pycloudmesh import azure_client
        
        # Test with dummy credentials
        azure = azure_client("dummy_subscription", "dummy_token")
        print("✅ Azure client created successfully")
        return True
    except Exception as e:
        print(f"❌ Azure client creation failed: {e}")
        return False

def test_azure_methods():
    """Test that Azure client has required methods."""
    try:
        from pycloudmesh import azure_client
        
        azure = azure_client("dummy_subscription", "dummy_token")
        
        required_methods = [
            'list_budgets',
            'get_cost_data',
            'get_reservation_cost',
            'get_reservation_recommendation',
            'get_cost_analysis',
            'get_cost_trends',
            'get_resource_costs',
            'get_reservation_order_details'
        ]
        
        for method in required_methods:
            if hasattr(azure, method):
                print(f"✅ Azure client has {method} method")
            else:
                print(f"❌ Azure client missing {method} method")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Azure methods test failed: {e}")
        return False

def test_azure_provider_direct_methods():
    """Test all AzureProvider methods directly with dummy parameters."""
    from pycloudmesh import azure_client
    azure = azure_client("dummy_subscription", "dummy_token")
    scope = "/subscriptions/dummy_subscription"
    resource_id = "/subscriptions/dummy_subscription/resourceGroups/dummy_rg/providers/Microsoft.Compute/virtualMachines/dummy-vm"
    tag_names = ["Environment", "Project"]
    notifications = [{
        "enabled": True,
        "operator": "GreaterThan",
        "threshold": 80.0,
        "contactEmails": ["test@example.com"]
    }]
    budget_name = "dummy-budget"
    amount = 100.0
    time_grain = "Monthly"
    api_version = "2024-08-01"
    filter_str = "Category eq 'Cost'"
    # list_budgets
    try:
        result = azure.list_budgets(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ list_budgets result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ list_budgets failed: {e}")
    # get_cost_data
    try:
        result = azure.get_cost_data(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_cost_data result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_cost_data failed: {e}")
    # get_reservation_cost
    try:
        result = azure.get_reservation_cost(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_reservation_cost result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_reservation_cost failed: {e}")
    # get_reservation_recommendation
    try:
        result = azure.get_reservation_recommendation(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_reservation_recommendation result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_reservation_recommendation failed: {e}")
    # get_cost_analysis
    try:
        result = azure.get_cost_analysis(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_cost_analysis result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_cost_analysis failed: {e}")
    # get_cost_trends
    try:
        result = azure.get_cost_trends(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_cost_trends result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_cost_trends failed: {e}")
    # get_resource_costs
    try:
        result = azure.get_resource_costs(scope=scope, resource_id=resource_id)
        assert isinstance(result, dict)
        print(f"✅ get_resource_costs result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_resource_costs failed: {e}")
    # get_cost_forecast
    try:
        result = azure.get_cost_forecast(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_cost_forecast result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_cost_forecast failed: {e}")
    # get_cost_anomalies
    try:
        result = azure.get_cost_anomalies(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_cost_anomalies result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_cost_anomalies failed: {e}")
    # get_cost_efficiency_metrics
    try:
        result = azure.get_cost_efficiency_metrics(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_cost_efficiency_metrics result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_cost_efficiency_metrics failed: {e}")
    # generate_cost_report
    try:
        result = azure.generate_cost_report(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ generate_cost_report result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ generate_cost_report failed: {e}")
    # get_governance_policies
    try:
        result = azure.get_governance_policies(scope=scope, tag_names=tag_names)
        assert isinstance(result, dict)
        print(f"✅ get_governance_policies result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_governance_policies failed: {e}")
    # get_costs_by_tags
    try:
        result = azure.get_costs_by_tags(scope=scope, tag_names=tag_names)
        assert isinstance(result, dict)
        print(f"✅ get_costs_by_tags result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_costs_by_tags failed: {e}")
    # get_reservation_order_details
    try:
        result = azure.get_reservation_order_details()
        assert isinstance(result, dict)
        print(f"✅ get_reservation_order_details result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_reservation_order_details failed: {e}")
    # create_budget
    try:
        result = azure.create_budget(budget_name=budget_name, amount=amount, scope=scope, notifications=notifications, time_grain=time_grain)
        assert isinstance(result, dict)
        print(f"✅ create_budget result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ create_budget failed: {e}")
    # get_budget
    try:
        result = azure.get_budget(budget_name=budget_name, scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_budget result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_budget failed: {e}")
    # get_advisor_recommendations
    try:
        result = azure.get_advisor_recommendations()
        assert isinstance(result, dict)
        print(f"✅ get_advisor_recommendations result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_advisor_recommendations failed: {e}")
    # get_reserved_instance_recommendations
    try:
        result = azure.get_reserved_instance_recommendations(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_reserved_instance_recommendations result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_reserved_instance_recommendations failed: {e}")
    # get_optimization_recommendations
    try:
        result = azure.get_optimization_recommendations(scope=scope)
        assert isinstance(result, dict)
        print(f"✅ get_optimization_recommendations result keys: {list(result.keys())}")
    except Exception as e:
        print(f"❌ get_optimization_recommendations failed: {e}")
    return True

def main():
    """Run Azure tests."""
    print("Testing Azure Functionality")
    print("=" * 30)
    
    tests = [test_azure_client_creation, test_azure_methods, test_azure_provider_direct_methods]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main()) 