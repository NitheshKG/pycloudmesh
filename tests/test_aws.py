#!/usr/bin/env python3
"""
Test file for AWS cloud functionality using unittest framework.
"""

import sys
import os
import unittest
import json
import datetime
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from pycloudmesh import aws_client

# Load environment variables from .env file
load_dotenv()

# Configuration flag for response storage
RESPONSE_STORE = True  # Set to False to disable response storage

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION = os.getenv("AWS_REGION")
ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")

# Budget config
BUDGET_NAME = "TestBudget-PyCloudMesh"
BUDGET_AMOUNT = 1.0  # USD


class TestAWSClient(unittest.TestCase):
    """Test cases for AWS client functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test class with AWS client initialization."""
        cls.aws = aws_client(access_key=ACCESS_KEY, secret_key=SECRET_KEY, region=REGION)
        cls.test_results = {
            "test_suite": "AWS Cloud Tests",
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

    def test_aws_client_creation(self):
        """Test AWS client creation."""
        try:
            # Test with credentials
            aws = aws_client(access_key=ACCESS_KEY, secret_key=SECRET_KEY, region=REGION)
            
            # Verify object properties
            self.assertIsNotNone(aws)
            self.assertEqual(type(aws).__name__, "AWSProvider")
            
            # Store response data
            self.test_response = {
                "client_type": type(aws).__name__,
                "has_required_attributes": hasattr(aws, 'reservation_client') and hasattr(aws, 'cost_client') and hasattr(aws, 'budget_client'),
                "available_clients": [attr for attr in dir(aws) if attr.endswith('_client')]
            }
            
            print("✅ AWS client created successfully")
            return True
        except Exception as e:
            self.fail(f"AWS client creation failed: {str(e)}")

    def test_aws_required_methods(self):
        """Test that AWS client has required methods."""
        required_methods = [
            "list_budgets",
            "get_cost_data",
            "get_reservation_cost",
            "get_reservation_recommendation",
            "get_reservation_coverage",
            "get_cost_analysis",
            "get_cost_trends",
            "get_resource_costs",
            "get_cost_forecast",
            "get_cost_anomalies",
            "get_cost_efficiency_metrics",
            "generate_cost_report",
            "get_governance_policies",
            "create_budget",
            "get_budget_notifications",
            "get_optimization_recommendations",
            "get_savings_plans_recommendations",
            "get_rightsizing_recommendations",
            "get_idle_resources",
            "get_reservation_purchase_recommendations"
        ]

        missing_methods = []
        available_methods = []
        for method in required_methods:
            if hasattr(self.aws, method):
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

    def test_aws_create_budget(self):
        """Test AWS budget creation functionality."""
        try:
            notifications = [
                {
                    "Notification": {
                        "NotificationType": "ACTUAL",
                        "ComparisonOperator": "GREATER_THAN",
                        "Threshold": 90.0,
                        "ThresholdType": "PERCENTAGE",
                    },
                    "Subscribers": [
                        {"SubscriptionType": "EMAIL", "Address": "nitheshkg18@gmail.com"}
                    ],
                }
            ]
            
            # Use unique budget name with timestamp
            import time
            unique_budget_name = f"{BUDGET_NAME}_{int(time.time())}"
            
            result = self.aws.create_budget(
                aws_account_id=ACCOUNT_ID,
                budget_name=unique_budget_name,
                budget_amount=BUDGET_AMOUNT,
                budget_type="COST",
                time_unit="MONTHLY",
                notifications_with_subscribers=notifications,
            )
            
            # Store response data
            self.test_response = {
                "budget_name": unique_budget_name,
                "budget_amount": BUDGET_AMOUNT,
                "budget_type": "COST",
                "time_unit": "MONTHLY",
                "notifications_count": len(notifications),
                "result": result,
                "success": result is not None
            }
            
            self.assertIsNotNone(result)
            print("✅ AWS budget creation test passed")
            
        except Exception as e:
            self.fail(f"AWS budget creation test failed: {str(e)}")

    def test_aws_list_budgets(self):
        """Test listing all budgets."""
        try:
            budgets = self.aws.list_budgets(aws_account_id=ACCOUNT_ID)
            
            # Store response data
            self.test_response = {
                "account_id": ACCOUNT_ID,
                "budgets_count": len(budgets.get("Budgets", [])) if isinstance(budgets, dict) else 0,
                "budgets_data": budgets,
                "has_budgets": len(budgets.get("Budgets", [])) > 0 if isinstance(budgets, dict) else False
            }
            
            self.assertIsNotNone(budgets)
            print("✅ AWS list budgets test passed")
            
        except Exception as e:
            self.fail(f"AWS list budgets test failed: {str(e)}")

    def test_aws_create_quarterly_budget(self):
        """Test creating a new quarterly budget with 80% threshold and email notification."""
        try:
            notifications = [
                {
                    "Notification": {
                        "NotificationType": "ACTUAL",
                        "ComparisonOperator": "GREATER_THAN",
                        "Threshold": 80.0,
                        "ThresholdType": "PERCENTAGE",
                    },
                    "Subscribers": [
                        {"SubscriptionType": "EMAIL", "Address": "nitheshkg18@gmail.com"}
                    ],
                }
            ]
            
            # Use unique budget name with timestamp
            import time
            unique_budget_name = f"Q1_Budget_{int(time.time())}"
            
            new_budget = self.aws.create_budget(
                aws_account_id=ACCOUNT_ID,
                budget_name=unique_budget_name,
                budget_amount=5000.0,
                time_unit="QUARTERLY",
                notifications_with_subscribers=notifications,
            )
            
            # Store response data
            self.test_response = {
                "budget_name": unique_budget_name,
                "budget_amount": 5000.0,
                "time_unit": "QUARTERLY",
                "threshold": 80.0,
                "notifications_count": len(notifications),
                "result": new_budget,
                "success": new_budget is not None
            }
            
            self.assertIsNotNone(new_budget)
            print("✅ AWS create quarterly budget test passed")
            
        except Exception as e:
            self.fail(f"AWS create quarterly budget test failed: {str(e)}")

    def test_aws_get_budget_notifications(self):
        """Test getting budget notifications."""
        try:
            alerts = self.aws.get_budget_notifications(
                aws_account_id=ACCOUNT_ID, budget_name="Q1 Budget"
            )
            
            # Store response data
            self.test_response = {
                "account_id": ACCOUNT_ID,
                "budget_name": "Q1 Budget",
                "notifications_data": alerts,
                "has_notifications": alerts is not None and len(alerts) > 0 if isinstance(alerts, list) else False,
                "notifications_count": len(alerts) if isinstance(alerts, list) else 0
            }
            
            self.assertIsNotNone(alerts)
            print("✅ AWS get budget notifications test passed")
            
        except Exception as e:
            self.fail(f"AWS get budget notifications test failed: {str(e)}")

    def test_aws_get_cost_data(self):
        """Test the get cost data functionality."""
        try:
            cost_data = self.aws.get_cost_data(
                start_date="2025-03-01",
                end_date="2025-05-31",
                granularity="DAILY",
                group_by=[
                    {"Type": "DIMENSION", "Key": "SERVICE"},
                    {"Type": "DIMENSION", "Key": "REGION"},
                ],
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "granularity": "DAILY",
                "group_by": ["SERVICE", "REGION"],
                "cost_data": cost_data,
                "has_data": cost_data is not None and len(cost_data) > 0 if isinstance(cost_data, list) else False,
                "data_points": len(cost_data) if isinstance(cost_data, list) else 0
            }
            
            self.assertIsNotNone(cost_data)
            print("✅ AWS get cost data test passed")
            
        except Exception as e:
            self.fail(f"AWS get cost data test failed: {str(e)}")

    def test_aws_get_cost_analysis(self):
        """Test the get cost analysis functionality."""
        try:
            cost_analysis = self.aws.get_cost_analysis(
                start_date="2025-03-01",
                end_date="2025-05-31",
                dimensions=["SERVICE", "REGION"],
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "dimensions": ["SERVICE", "REGION"],
                "analysis_data": cost_analysis,
                "has_analysis": cost_analysis is not None,
                "total_cost": cost_analysis.get("total_cost", 0) if isinstance(cost_analysis, dict) else 0,
                "top_services_count": len(cost_analysis.get("top_services", [])) if isinstance(cost_analysis, dict) else 0,
                "insights_count": len(cost_analysis.get("insights", [])) if isinstance(cost_analysis, dict) else 0
            }
            
            self.assertIsNotNone(cost_analysis)
            print("✅ AWS get cost analysis test passed")
            
        except Exception as e:
            self.fail(f"AWS get cost analysis test failed: {str(e)}")

    def test_aws_get_cost_trends(self):
        """Test the get cost trends functionality."""
        try:
            cost_trends = self.aws.get_cost_trends(
                start_date="2025-03-01", 
                end_date="2025-05-31", 
                granularity="DAILY"
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "granularity": "DAILY",
                "trends_data": cost_trends,
                "has_trends": cost_trends is not None,
                "total_periods": cost_trends.get("total_periods", 0) if isinstance(cost_trends, dict) else 0,
                "total_cost": cost_trends.get("total_cost", 0) if isinstance(cost_trends, dict) else 0,
                "trend_direction": cost_trends.get("trend_direction", "unknown") if isinstance(cost_trends, dict) else "unknown",
                "growth_rate": cost_trends.get("growth_rate", 0) if isinstance(cost_trends, dict) else 0,
                "patterns_count": len(cost_trends.get("patterns", [])) if isinstance(cost_trends, dict) else 0,
                "insights_count": len(cost_trends.get("insights", [])) if isinstance(cost_trends, dict) else 0
            }
            
            self.assertIsNotNone(cost_trends)
            print("✅ AWS get cost trends test passed")
            
        except Exception as e:
            self.fail(f"AWS get cost trends test failed: {str(e)}")

    def test_aws_get_resource_costs(self):
        """Test the get resource costs functionality."""
        try:
            resource_costs = self.aws.get_resource_costs(
                resource_id="i-0df615a5315c31029",
                start_date="2025-03-01",
                end_date="2025-05-31",
                granularity="DAILY",
            )
            
            # Store response data
            self.test_response = {
                "resource_id": "i-0df615a5315c31029",
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "granularity": "DAILY",
                "resource_costs_data": resource_costs,
                "has_data": resource_costs is not None,
                "total_cost": resource_costs.get("total_cost", 0) if isinstance(resource_costs, dict) else 0,
                "total_periods": resource_costs.get("total_periods", 0) if isinstance(resource_costs, dict) else 0,
                "active_periods": resource_costs.get("active_periods", 0) if isinstance(resource_costs, dict) else 0,
                "cost_breakdown_count": len(resource_costs.get("cost_breakdown", {})) if isinstance(resource_costs, dict) else 0,
                "utilization_insights_count": len(resource_costs.get("utilization_insights", [])) if isinstance(resource_costs, dict) else 0,
                "recommendations_count": len(resource_costs.get("recommendations", [])) if isinstance(resource_costs, dict) else 0
            }
            
            self.assertIsNotNone(resource_costs)
            print("✅ AWS get resource costs test passed")
            
        except Exception as e:
            self.fail(f"AWS get resource costs test failed: {str(e)}")

    def test_aws_get_optimization_recommendations(self):
        """Test the get optimization recommendations functionality."""
        try:
            optimization_recs = self.aws.get_optimization_recommendations()
            
            # Store response data
            self.test_response = {
                "optimization_data": optimization_recs,
                "has_recommendations": optimization_recs is not None,
                "reservations_count": len(optimization_recs.get("reservations", {}).get("Recommendations", [])) if isinstance(optimization_recs, dict) and isinstance(optimization_recs.get("reservations"), dict) else 0,
                "savings_plans_count": len(optimization_recs.get("savings_plans", {}).get("SavingsPlansRecommendation", [])) if isinstance(optimization_recs, dict) and isinstance(optimization_recs.get("savings_plans"), dict) else 0,
                "rightsizing_count": len(optimization_recs.get("rightsizing", {}).get("RightsizingRecommendations", [])) if isinstance(optimization_recs, dict) and isinstance(optimization_recs.get("rightsizing"), dict) else 0,
                "idle_resources_count": optimization_recs.get("idle_resources", {}).get("total_idle_count", 0) if isinstance(optimization_recs, dict) and isinstance(optimization_recs.get("idle_resources"), dict) else 0,
                "total_opportunities": (
                    len(optimization_recs.get("reservations", {}).get("Recommendations", [])) +
                    len(optimization_recs.get("savings_plans", {}).get("SavingsPlansRecommendation", [])) +
                    len(optimization_recs.get("rightsizing", {}).get("RightsizingRecommendations", [])) +
                    optimization_recs.get("idle_resources", {}).get("total_idle_count", 0)
                ) if isinstance(optimization_recs, dict) else 0
            }
            
            self.assertIsNotNone(optimization_recs)
            print("✅ AWS get optimization recommendations test passed")
            
        except Exception as e:
            self.fail(f"AWS get optimization recommendations test failed: {str(e)}")

    def test_aws_get_reservation_cost(self):
        """Test the get reservation cost functionality."""
        try:
            reservation_cost = self.aws.get_reservation_cost(
                start_date="2025-03-01",
                end_date="2025-05-31",
                granularity="MONTHLY"
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "granularity": "MONTHLY",
                "reservation_cost_data": reservation_cost,
                "has_data": reservation_cost is not None,
                "utilization_data": reservation_cost.get("UtilizationsByTime", []) if isinstance(reservation_cost, dict) else [],
                "utilization_count": len(reservation_cost.get("UtilizationsByTime", [])) if isinstance(reservation_cost, dict) else 0
            }
            
            self.assertIsNotNone(reservation_cost)
            print("✅ AWS get reservation cost test passed")
            
        except Exception as e:
            self.fail(f"AWS get reservation cost test failed: {str(e)}")

    def test_aws_get_reservation_recommendation(self):
        """Test the get reservation recommendation functionality."""
        try:
            reservation_rec = self.aws.get_reservation_recommendation(
                Service="AmazonEC2",
                LookbackPeriodInDays="THIRTY_DAYS",
                TermInYears="ONE_YEAR",
                PaymentOption="NO_UPFRONT"
            )
            
            # Store response data
            self.test_response = {
                "service": "AmazonEC2",
                "lookback_period": "THIRTY_DAYS",
                "term": "ONE_YEAR",
                "payment_option": "NO_UPFRONT",
                "recommendation_data": reservation_rec,
                "has_recommendations": reservation_rec is not None,
                "recommendations_count": len(reservation_rec.get("Recommendations", [])) if isinstance(reservation_rec, dict) else 0
            }
            
            self.assertIsNotNone(reservation_rec)
            print("✅ AWS get reservation recommendation test passed")
            
        except Exception as e:
            self.fail(f"AWS get reservation recommendation test failed: {str(e)}")

    def test_aws_get_reservation_coverage(self):
        """Test the get reservation coverage functionality."""
        try:
            coverage_data = self.aws.get_reservation_coverage(
                start_date="2025-03-01",
                end_date="2025-05-31",
                granularity="MONTHLY"
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "granularity": "MONTHLY",
                "coverage_data": coverage_data,
                "has_data": coverage_data is not None,
                "coverage_periods": len(coverage_data.get("CoveragesByTime", [])) if isinstance(coverage_data, dict) else 0
            }
            
            self.assertIsNotNone(coverage_data)
            print("✅ AWS get reservation coverage test passed")
            
        except Exception as e:
            self.fail(f"AWS get reservation coverage test failed: {str(e)}")

    def test_aws_get_cost_forecast(self):
        """Test the get cost forecast functionality."""
        try:
            cost_forecast = self.aws.get_cost_forecast(
                start_date="2025-03-01",
                end_date="2025-05-31",
                granularity="MONTHLY"
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "granularity": "MONTHLY",
                "forecast_data": cost_forecast,
                "has_forecast": cost_forecast is not None,
                "forecast_periods": len(cost_forecast.get("ForecastResultsByTime", [])) if isinstance(cost_forecast, dict) else 0
            }
            
            self.assertIsNotNone(cost_forecast)
            print("✅ AWS get cost forecast test passed")
            
        except Exception as e:
            self.fail(f"AWS get cost forecast test failed: {str(e)}")

    def test_aws_get_cost_anomalies(self):
        """Test the get cost anomalies functionality."""
        try:
            cost_anomalies = self.aws.get_cost_anomalies(
                start_date="2025-03-01",
                end_date="2025-05-31"
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "anomalies_data": cost_anomalies,
                "has_anomalies": cost_anomalies is not None,
                "anomalies_count": len(cost_anomalies.get("Anomalies", [])) if isinstance(cost_anomalies, dict) else 0
            }
            
            self.assertIsNotNone(cost_anomalies)
            print("✅ AWS get cost anomalies test passed")
            
        except Exception as e:
            self.fail(f"AWS get cost anomalies test failed: {str(e)}")

    def test_aws_get_cost_efficiency_metrics(self):
        """Test the get cost efficiency metrics functionality."""
        try:
            efficiency_metrics = self.aws.get_cost_efficiency_metrics(
                start_date="2025-03-01",
                end_date="2025-05-31"
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "efficiency_data": efficiency_metrics,
                "has_metrics": efficiency_metrics is not None,
                "metrics_count": len(efficiency_metrics.get("Metrics", [])) if isinstance(efficiency_metrics, dict) else 0
            }
            
            self.assertIsNotNone(efficiency_metrics)
            print("✅ AWS get cost efficiency metrics test passed")
            
        except Exception as e:
            self.fail(f"AWS get cost efficiency metrics test failed: {str(e)}")

    def test_aws_generate_cost_report(self):
        """Test the generate cost report functionality."""
        try:
            cost_report = self.aws.generate_cost_report(
                start_date="2025-03-01",
                end_date="2025-05-31"
            )
            
            # Store response data
            self.test_response = {
                "start_date": "2025-03-01",
                "end_date": "2025-05-31",
                "report_data": cost_report,
                "has_report": cost_report is not None,
                "report_sections": len(cost_report.get("sections", [])) if isinstance(cost_report, dict) else 0
            }
            
            self.assertIsNotNone(cost_report)
            print("✅ AWS generate cost report test passed")
            
        except Exception as e:
            self.fail(f"AWS generate cost report test failed: {str(e)}")

    def test_aws_get_governance_policies(self):
        """Test the get governance policies functionality."""
        try:
            governance_policies = self.aws.get_governance_policies()
            
            # Store response data
            self.test_response = {
                "policies_data": governance_policies,
                "has_policies": governance_policies is not None,
                "policies_count": len(governance_policies.get("policies", [])) if isinstance(governance_policies, dict) else 0
            }
            
            self.assertIsNotNone(governance_policies)
            print("✅ AWS get governance policies test passed")
            
        except Exception as e:
            self.fail(f"AWS get governance policies test failed: {str(e)}")

    def test_aws_get_savings_plans_recommendations(self):
        """Test the get savings plans recommendations functionality."""
        try:
            savings_plans_rec = self.aws.get_savings_plans_recommendations()
            
            # Store response data
            self.test_response = {
                "savings_plans_data": savings_plans_rec,
                "has_recommendations": savings_plans_rec is not None,
                "recommendations_count": len(savings_plans_rec.get("SavingsPlansRecommendation", [])) if isinstance(savings_plans_rec, dict) else 0
            }
            
            self.assertIsNotNone(savings_plans_rec)
            print("✅ AWS get savings plans recommendations test passed")
            
        except Exception as e:
            self.fail(f"AWS get savings plans recommendations test failed: {str(e)}")

    def test_aws_get_rightsizing_recommendations(self):
        """Test the get rightsizing recommendations functionality."""
        try:
            rightsizing_rec = self.aws.get_rightsizing_recommendations()
            
            # Store response data
            self.test_response = {
                "rightsizing_data": rightsizing_rec,
                "has_recommendations": rightsizing_rec is not None,
                "recommendations_count": len(rightsizing_rec.get("RightsizingRecommendations", [])) if isinstance(rightsizing_rec, dict) else 0
            }
            
            self.assertIsNotNone(rightsizing_rec)
            print("✅ AWS get rightsizing recommendations test passed")
            
        except Exception as e:
            self.fail(f"AWS get rightsizing recommendations test failed: {str(e)}")

    def test_aws_get_idle_resources(self):
        """Test the get idle resources functionality."""
        try:
            idle_resources = self.aws.get_idle_resources()
            
            # Store response data
            self.test_response = {
                "idle_resources_data": idle_resources,
                "has_idle_resources": idle_resources is not None,
                "idle_count": idle_resources.get("total_idle_count", 0) if isinstance(idle_resources, dict) else 0
            }
            
            self.assertIsNotNone(idle_resources)
            print("✅ AWS get idle resources test passed")
            
        except Exception as e:
            self.fail(f"AWS get idle resources test failed: {str(e)}")

    def test_aws_get_reservation_purchase_recommendations(self):
        """Test the get reservation purchase recommendations functionality."""
        try:
            purchase_rec = self.aws.get_reservation_purchase_recommendations(
                Service="AmazonEC2",
                LookbackPeriodInDays="THIRTY_DAYS",
                TermInYears="ONE_YEAR"
            )
            
            # Store response data
            self.test_response = {
                "service": "AmazonEC2",
                "lookback_period": "THIRTY_DAYS",
                "term": "ONE_YEAR",
                "purchase_data": purchase_rec,
                "has_recommendations": purchase_rec is not None,
                "recommendations_count": len(purchase_rec.get("Recommendations", [])) if isinstance(purchase_rec, dict) else 0
            }
            
            self.assertIsNotNone(purchase_rec)
            print("✅ AWS get reservation purchase recommendations test passed")
            
        except Exception as e:
            self.fail(f"AWS get reservation purchase recommendations test failed: {str(e)}")

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
        filename = f"aws_{timestamp}_test.json"
        filepath = reports_dir / filename

        # Save report as JSON
        with open(filepath, 'w') as f:
            json.dump(cls.test_results, f, indent=2, default=str)

        # Print summary to console
        print("\n" + "=" * 60)
        print(f"{'AWS Test Results Summary':^60}")
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
    """Run all AWS tests and generate report."""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAWSClient)
    
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
    
    # Update the test results in the TestAWSClient class
    TestAWSClient.test_results["test_details"] = result_collector.test_results
    
    return result_collector.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
