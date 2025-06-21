#!/usr/bin/env python3
"""
Test file for GCP cloud functionality.
"""

import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_gcp_client_creation():
    """Test GCP client creation."""
    try:
        from pycloudmesh import gcp_client
        
        # Test with dummy credentials (will fail on file not found, but that's expected)
        try:
            gcp = gcp_client("dummy_project", "/nonexistent/credentials.json")
            print("✅ GCP client created successfully")
        except FileNotFoundError:
            print("✅ GCP client creation attempted (file not found expected)")
        
        return True
    except Exception as e:
        print(f"❌ GCP client creation failed: {e}")
        return False

def test_gcp_methods():
    """Test that GCP client has required methods."""
    try:
        from pycloudmesh.pycloudmesh import GCPProvider
        
        # Create a mock client to test methods
        gcp = GCPProvider("dummy_project", "/dummy/path")
        
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
            if hasattr(gcp, method):
                print(f"✅ GCP client has {method} method")
            else:
                print(f"❌ GCP client missing {method} method")
                return False
        
        return True
    except Exception as e:
        print(f"❌ GCP methods test failed: {e}")
        return False

def main():
    """Run GCP tests."""
    print("Testing GCP Functionality")
    print("=" * 30)
    
    tests = [test_gcp_client_creation, test_gcp_methods]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main()) 