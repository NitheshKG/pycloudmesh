#!/usr/bin/env python3
"""
Test file for AWS cloud functionality.
"""

import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_aws_client_creation():
    """Test AWS client creation."""
    try:
        from pycloudmesh import aws_client
        
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
        from pycloudmesh import aws_client
        
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

def main():
    """Run AWS tests."""
    print("Testing AWS Functionality")
    print("=" * 30)
    
    tests = [test_aws_client_creation, test_aws_methods]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main()) 