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

def main():
    """Run Azure tests."""
    print("Testing Azure Functionality")
    print("=" * 30)
    
    tests = [test_azure_client_creation, test_azure_methods]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main()) 