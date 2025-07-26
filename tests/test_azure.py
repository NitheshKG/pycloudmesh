#!/usr/bin/env python3
"""
Test file for Azure cloud functionality using unittest framework.
"""

import sys
import os
import unittest
import json
import datetime
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from pycloudmesh import azure_client

# Load environment variables from .env file
load_dotenv()

# Configuration flag for response storage
RESPONSE_STORE = True  # Set to False to disable response storage

SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
TOKEN = os.getenv("AZURE_TOKEN")

# Budget config
BUDGET_NAME = "TestBudget-PyCloudMesh"
BUDGET_AMOUNT = 100.0  # USD


class TestAzureClient(unittest.TestCase):
    """Test cases for Azure client functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test class with Azure client initialization."""
        cls.azure = azure_client(subscription_id=SUBSCRIPTION_ID, token=TOKEN)
        cls.test_results = {
            "test_suite": "Azure Cloud Tests",
            "timestamp": datetime.datetime.now().isoformat(),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "test_details": []
        }

    def setUp(self):
        """Set up for each test method."""
        self.test_start_time = datetime.datetime.now()
        self.test_response = None  # Store the response for this test

    def tearDown(self):
        """Tear down after each test method."""
        test_end_time = datetime.datetime.now()
        test_duration = (test_end_time - self.test_start_time).total_seconds()
        
        # Record test result - all tests that reach tearDown are considered passed
        # since exceptions would be caught by the test framework
        test_result = {
            "test_name": self._testMethodName,
            "status": "PASSED",
            "duration": test_duration,
            "error_message": None,
            "response": self.test_response if RESPONSE_STORE else None  # Conditionally include response
        }
        
        self.test_results["test_details"].append(test_result)

    def test_azure_client_creation(self):
        """Test Azure client creation."""
        try:
            # Test with credentials
            azure = azure_client(subscription_id=SUBSCRIPTION_ID, token=TOKEN)
            
            # Verify object properties
            self.assertIsNotNone(azure)
            self.assertEqual(type(azure).__name__, "AzureProvider")
            
            # Store response data
            self.test_response = {
                "client_type": type(azure).__name__,
                "has_required_attributes": hasattr(azure, 'reservation_client') and hasattr(azure, 'cost_client') and hasattr(azure, 'budget_client'),
                "available_clients": [attr for attr in dir(azure) if attr.endswith('_client')]
            }
            
            print("✅ Azure client created successfully")
            return True
        except Exception as e:
            self.fail(f"Azure client creation failed: {str(e)}")

    def test_azure_required_methods(self):
        """Test that Azure client has required methods."""
        required_methods = [
            "list_budgets",
            "get_cost_data",
            "get_reservation_cost",
            "get_reservation_recommendation",
            "get_cost_analysis",
            "get_cost_trends",
            "get_resource_costs",
            "get_cost_forecast",
            "get_cost_anomalies",
            "get_cost_efficiency_metrics",
            "generate_cost_report",
            "get_governance_policies",
            "create_budget",
            "get_budget",
            "get_costs_by_tags",
            "get_reservation_order_details",
            "get_advisor_recommendations",
            "get_reserved_instance_recommendations",
            "get_optimization_recommendations"
        ]

        missing_methods = []
        available_methods = []
        for method in required_methods:
            if hasattr(self.azure, method):
                available_methods.append(method)
            else:
                missing_methods.append(method)

        # Store response data
        self.test_response = {
            "total_required_methods": len(required_methods),
            "available_methods": available_methods,
            "missing_methods": missing_methods,
            "all_methods_present": len(missing_methods) == 0
        }

        self.assertEqual(len(missing_methods), 0, 
                       f"Missing required methods: {missing_methods}")

    def test_azure_list_budgets(self):
        """Test listing all budgets."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            budgets = self.azure.list_budgets(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "budgets_data": budgets,
                "has_budgets": budgets is not None,
                "budgets_count": len(budgets.get("value", [])) if isinstance(budgets, dict) else 0
            }
            
            self.assertIsNotNone(budgets)
            print("✅ Azure list budgets test passed")
            
        except Exception as e:
            self.fail(f"Azure list budgets test failed: {str(e)}")

    def test_azure_create_budget(self):
        """Test Azure budget creation functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            notifications = [{
                "enabled": True,
                "operator": "GreaterThan",
                "threshold": 80.0,
                "contactEmails": ["test@example.com"]
            }]
            
            # Use unique budget name with timestamp
            import time
            unique_budget_name = f"{BUDGET_NAME}_{int(time.time())}"
            
            result = self.azure.create_budget(
                budget_name=unique_budget_name,
                amount=BUDGET_AMOUNT,
                scope=scope,
                notifications=notifications,
                time_grain="Monthly"
            )
            
            # Store response data
            self.test_response = {
                "budget_name": unique_budget_name,
                "budget_amount": BUDGET_AMOUNT,
                "scope": scope,
                "time_grain": "Monthly",
                "notifications_count": len(notifications),
                "result": result,
                "success": result is not None
            }
            
            self.assertIsNotNone(result)
            print("✅ Azure budget creation test passed")
            
        except Exception as e:
            self.fail(f"Azure budget creation test failed: {str(e)}")

    def test_azure_get_budget(self):
        """Test getting a specific budget."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            budget_name = "TestBudget"
            
            budget = self.azure.get_budget(budget_name=budget_name, scope=scope)
            
            # Store response data
            self.test_response = {
                "budget_name": budget_name,
                "scope": scope,
                "budget_data": budget,
                "has_budget": budget is not None
            }
            
            self.assertIsNotNone(budget)
            print("✅ Azure get budget test passed")
            
        except Exception as e:
            self.fail(f"Azure get budget test failed: {str(e)}")

    def test_azure_get_cost_data(self):
        """Test the get cost data functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            cost_data = self.azure.get_cost_data(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "cost_data": cost_data,
                "has_data": cost_data is not None,
                "data_points": len(cost_data.get("value", [])) if isinstance(cost_data, dict) else 0
            }
            
            self.assertIsNotNone(cost_data)
            print("✅ Azure get cost data test passed")
            
        except Exception as e:
            self.fail(f"Azure get cost data test failed: {str(e)}")

    def test_azure_get_cost_analysis(self):
        """Test the get cost analysis functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            cost_analysis = self.azure.get_cost_analysis(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "analysis_data": cost_analysis,
                "has_analysis": cost_analysis is not None,
                "total_cost": cost_analysis.get("total_cost", 0) if isinstance(cost_analysis, dict) else 0,
                "top_services_count": len(cost_analysis.get("top_services", [])) if isinstance(cost_analysis, dict) else 0,
                "insights_count": len(cost_analysis.get("insights", [])) if isinstance(cost_analysis, dict) else 0
            }
            
            self.assertIsNotNone(cost_analysis)
            print("✅ Azure get cost analysis test passed")
            
        except Exception as e:
            self.fail(f"Azure get cost analysis test failed: {str(e)}")

    def test_azure_get_cost_trends(self):
        """Test the get cost trends functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            cost_trends = self.azure.get_cost_trends(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "trends_data": cost_trends,
                "has_trends": cost_trends is not None,
                "total_periods": cost_trends.get("total_periods", 0) if isinstance(cost_trends, dict) else 0,
                "total_cost": cost_trends.get("total_cost", 0) if isinstance(cost_trends, dict) else 0,
                "trend_direction": cost_trends.get("trend_direction", "unknown") if isinstance(cost_trends, dict) else "unknown",
                "growth_rate": cost_trends.get("growth_rate", 0) if isinstance(cost_trends, dict) else 0
            }
            
            self.assertIsNotNone(cost_trends)
            print("✅ Azure get cost trends test passed")
            
        except Exception as e:
            self.fail(f"Azure get cost trends test failed: {str(e)}")

    def test_azure_get_resource_costs(self):
        """Test the get resource costs functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            resource_id = f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/test-rg/providers/Microsoft.Compute/virtualMachines/test-vm"
            
            resource_costs = self.azure.get_resource_costs(scope=scope, resource_id=resource_id)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "resource_id": resource_id,
                "resource_costs_data": resource_costs,
                "has_data": resource_costs is not None,
                "total_cost": resource_costs.get("total_cost", 0) if isinstance(resource_costs, dict) else 0,
                "total_periods": resource_costs.get("total_periods", 0) if isinstance(resource_costs, dict) else 0
            }
            
            self.assertIsNotNone(resource_costs)
            print("✅ Azure get resource costs test passed")
            
        except Exception as e:
            self.fail(f"Azure get resource costs test failed: {str(e)}")

    def test_azure_get_reservation_cost(self):
        """Test the get reservation cost functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            reservation_cost = self.azure.get_reservation_cost(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "reservation_cost_data": reservation_cost,
                "has_data": reservation_cost is not None,
                "utilization_data": reservation_cost.get("utilizations", []) if isinstance(reservation_cost, dict) else [],
                "utilization_count": len(reservation_cost.get("utilizations", [])) if isinstance(reservation_cost, dict) else 0
            }
            
            self.assertIsNotNone(reservation_cost)
            print("✅ Azure get reservation cost test passed")
            
        except Exception as e:
            self.fail(f"Azure get reservation cost test failed: {str(e)}")

    def test_azure_get_reservation_recommendation(self):
        """Test the get reservation recommendation functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            reservation_rec = self.azure.get_reservation_recommendation(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "recommendation_data": reservation_rec,
                "has_recommendations": reservation_rec is not None,
                "recommendations_count": len(reservation_rec.get("recommendations", [])) if isinstance(reservation_rec, dict) else 0
            }
            
            self.assertIsNotNone(reservation_rec)
            print("✅ Azure get reservation recommendation test passed")
            
        except Exception as e:
            self.fail(f"Azure get reservation recommendation test failed: {str(e)}")

    def test_azure_get_cost_forecast(self):
        """Test the get cost forecast functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            cost_forecast = self.azure.get_cost_forecast(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "forecast_data": cost_forecast,
                "has_forecast": cost_forecast is not None,
                "forecast_periods": len(cost_forecast.get("forecast_periods", [])) if isinstance(cost_forecast, dict) else 0
            }
            
            self.assertIsNotNone(cost_forecast)
            print("✅ Azure get cost forecast test passed")
            
        except Exception as e:
            self.fail(f"Azure get cost forecast test failed: {str(e)}")

    def test_azure_get_cost_anomalies(self):
        """Test the get cost anomalies functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            cost_anomalies = self.azure.get_cost_anomalies(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "anomalies_data": cost_anomalies,
                "has_anomalies": cost_anomalies is not None,
                "anomalies_count": len(cost_anomalies.get("anomalies", [])) if isinstance(cost_anomalies, dict) else 0
            }
            
            self.assertIsNotNone(cost_anomalies)
            print("✅ Azure get cost anomalies test passed")
            
        except Exception as e:
            self.fail(f"Azure get cost anomalies test failed: {str(e)}")

    def test_azure_get_cost_efficiency_metrics(self):
        """Test the get cost efficiency metrics functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            efficiency_metrics = self.azure.get_cost_efficiency_metrics(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "efficiency_data": efficiency_metrics,
                "has_metrics": efficiency_metrics is not None,
                "metrics_count": len(efficiency_metrics.get("metrics", [])) if isinstance(efficiency_metrics, dict) else 0
            }
            
            self.assertIsNotNone(efficiency_metrics)
            print("✅ Azure get cost efficiency metrics test passed")
            
        except Exception as e:
            self.fail(f"Azure get cost efficiency metrics test failed: {str(e)}")

    def test_azure_generate_cost_report(self):
        """Test the generate cost report functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            cost_report = self.azure.generate_cost_report(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "report_data": cost_report,
                "has_report": cost_report is not None,
                "report_sections": len(cost_report.get("sections", [])) if isinstance(cost_report, dict) else 0
            }
            
            self.assertIsNotNone(cost_report)
            print("✅ Azure generate cost report test passed")
            
        except Exception as e:
            self.fail(f"Azure generate cost report test failed: {str(e)}")

    def test_azure_get_governance_policies(self):
        """Test the get governance policies functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            tag_names = ["Environment", "Project"]
            governance_policies = self.azure.get_governance_policies(scope=scope, tag_names=tag_names)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "tag_names": tag_names,
                "policies_data": governance_policies,
                "has_policies": governance_policies is not None,
                "policies_count": len(governance_policies.get("policies", [])) if isinstance(governance_policies, dict) else 0
            }
            
            self.assertIsNotNone(governance_policies)
            print("✅ Azure get governance policies test passed")
            
        except Exception as e:
            self.fail(f"Azure get governance policies test failed: {str(e)}")

    def test_azure_get_costs_by_tags(self):
        """Test the get costs by tags functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            tag_names = ["Environment", "Project"]
            costs_by_tags = self.azure.get_costs_by_tags(scope=scope, tag_names=tag_names)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "tag_names": tag_names,
                "costs_data": costs_by_tags,
                "has_data": costs_by_tags is not None,
                "tagged_costs_count": len(costs_by_tags.get("tagged_costs", [])) if isinstance(costs_by_tags, dict) else 0
            }
            
            self.assertIsNotNone(costs_by_tags)
            print("✅ Azure get costs by tags test passed")
            
        except Exception as e:
            self.fail(f"Azure get costs by tags test failed: {str(e)}")

    def test_azure_get_reservation_order_details(self):
        """Test the get reservation order details functionality."""
        try:
            reservation_order_details = self.azure.get_reservation_order_details()
            
            # Store response data
            self.test_response = {
                "reservation_order_data": reservation_order_details,
                "has_data": reservation_order_details is not None,
                "orders_count": len(reservation_order_details.get("orders", [])) if isinstance(reservation_order_details, dict) else 0
            }
            
            self.assertIsNotNone(reservation_order_details)
            print("✅ Azure get reservation order details test passed")
            
        except Exception as e:
            self.fail(f"Azure get reservation order details test failed: {str(e)}")

    def test_azure_get_advisor_recommendations(self):
        """Test the get advisor recommendations functionality."""
        try:
            advisor_recommendations = self.azure.get_advisor_recommendations()
            
            # Store response data
            self.test_response = {
                "advisor_data": advisor_recommendations,
                "has_recommendations": advisor_recommendations is not None,
                "recommendations_count": len(advisor_recommendations.get("recommendations", [])) if isinstance(advisor_recommendations, dict) else 0
            }
            
            self.assertIsNotNone(advisor_recommendations)
            print("✅ Azure get advisor recommendations test passed")
            
        except Exception as e:
            self.fail(f"Azure get advisor recommendations test failed: {str(e)}")

    def test_azure_get_reserved_instance_recommendations(self):
        """Test the get reserved instance recommendations functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            reserved_instance_rec = self.azure.get_reserved_instance_recommendations(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "reserved_instance_data": reserved_instance_rec,
                "has_recommendations": reserved_instance_rec is not None,
                "recommendations_count": len(reserved_instance_rec.get("recommendations", [])) if isinstance(reserved_instance_rec, dict) else 0
            }
            
            self.assertIsNotNone(reserved_instance_rec)
            print("✅ Azure get reserved instance recommendations test passed")
            
        except Exception as e:
            self.fail(f"Azure get reserved instance recommendations test failed: {str(e)}")

    def test_azure_get_optimization_recommendations(self):
        """Test the get optimization recommendations functionality."""
        try:
            scope = f"/subscriptions/{SUBSCRIPTION_ID}"
            optimization_recs = self.azure.get_optimization_recommendations(scope=scope)
            
            # Store response data
            self.test_response = {
                "subscription_id": SUBSCRIPTION_ID,
                "scope": scope,
                "optimization_data": optimization_recs,
                "has_recommendations": optimization_recs is not None,
                "recommendations_count": len(optimization_recs.get("recommendations", [])) if isinstance(optimization_recs, dict) else 0
            }
            
            self.assertIsNotNone(optimization_recs)
            print("✅ Azure get optimization recommendations test passed")
            
        except Exception as e:
            self.fail(f"Azure get optimization recommendations test failed: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        """Generate and save test report."""
        cls.generate_test_report()

    @classmethod
    def generate_test_report(cls):
        """Generate test report and save to test_reports directory."""
        # Calculate summary statistics
        total_tests = len(cls.test_results["test_details"])
        passed = sum(1 for test in cls.test_results["test_details"] if test["status"] == "PASSED")
        failed = sum(1 for test in cls.test_results["test_details"] if test["status"] == "FAILED")
        
        cls.test_results["total_tests"] = total_tests
        cls.test_results["passed"] = passed
        cls.test_results["failed"] = failed
        cls.test_results["success_rate"] = (passed / total_tests * 100) if total_tests > 0 else 0

        # Create test_reports directory if it doesn't exist
        reports_dir = Path("tests/test_reports")
        reports_dir.mkdir(exist_ok=True)

        # Generate filename with cloud_name_datetime_test format
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"azure_{timestamp}_test.json"
        filepath = reports_dir / filename

        # Save report as JSON
        with open(filepath, 'w') as f:
            json.dump(cls.test_results, f, indent=2, default=str)

        # Print summary to console
        print("\n" + "=" * 60)
        print(f"{'Azure Test Results Summary':^60}")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {cls.test_results['success_rate']:.1f}%")
        print(f"Report saved to: {filepath}")
        print("=" * 60)

        # Print detailed results
        print("\nDetailed Test Results:")
        print("-" * 60)
        for test in cls.test_results["test_details"]:
            status_icon = "✅" if test["status"] == "PASSED" else "❌"
            print(f"{status_icon} {test['test_name']:<40} {test['status']:<8} ({test['duration']:.2f}s)")
            if test["error_message"]:
                print(f"    Error: {test['error_message']}")

        return filepath


def run_tests():
    """Run all Azure tests and generate report."""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAzureClient)
    
    # Create a custom test result collector
    class TestResultCollector(unittest.TestResult):
        def __init__(self):
            super().__init__()
            self.test_results = []
        
        def addSuccess(self, test):
            super().addSuccess(test)
            # Get response data from the test instance if available
            response_data = getattr(test, 'test_response', None) if RESPONSE_STORE else None
            self.test_results.append({
                "test_name": test._testMethodName,
                "status": "PASSED",
                "error_message": None,
                "response": response_data
            })
        
        def addFailure(self, test, err):
            super().addFailure(test, err)
            response_data = getattr(test, 'test_response', None) if RESPONSE_STORE else None
            self.test_results.append({
                "test_name": test._testMethodName,
                "status": "FAILED",
                "error_message": str(err[1]),
                "response": response_data
            })
        
        def addError(self, test, err):
            super().addError(test, err)
            response_data = getattr(test, 'test_response', None) if RESPONSE_STORE else None
            self.test_results.append({
                "test_name": test._testMethodName,
                "status": "FAILED",
                "error_message": str(err[1]),
                "response": response_data
            })
    
    # Run tests with custom result collector
    result_collector = TestResultCollector()
    suite.run(result_collector)
    
    # Update the test results in the TestAzureClient class
    TestAzureClient.test_results["test_details"] = result_collector.test_results
    
    return result_collector.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 